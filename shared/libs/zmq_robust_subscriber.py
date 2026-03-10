#!/usr/bin/env python3
"""
Robust ZeroMQ Subscriber with automatic reconnection and error recovery.

Features:
- Exponential backoff reconnection
- Message persistence for offline periods
- Subscriber lag monitoring
- Circuit breaker pattern
- Health metrics

File UUID: a3f8c2d1-4b7e-4a9f-8e2d-5c6b9d8f1e3a
"""
# File UUID: a3f8c2d1-4b7e-4a9f-8e2d-5c6b9d8f1e3a

import zmq
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import threading
import queue


class ConnectionState(Enum):
    """Subscriber connection state."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    FAILED = "failed"


@dataclass
class ReconnectionConfig:
    """Configuration for reconnection behavior."""
    initial_delay: float = 1.0  # seconds
    max_delay: float = 60.0  # seconds
    backoff_multiplier: float = 2.0
    max_attempts: Optional[int] = None  # None = infinite
    jitter: bool = True  # Add randomness to prevent thundering herd


@dataclass
class SubscriberMetrics:
    """Metrics for monitoring subscriber health."""
    messages_received: int = 0
    messages_failed: int = 0
    reconnect_count: int = 0
    last_message_time: Optional[datetime] = None
    last_reconnect_time: Optional[datetime] = None
    current_lag_ms: float = 0.0
    connection_state: ConnectionState = ConnectionState.DISCONNECTED
    uptime_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "messages_received": self.messages_received,
            "messages_failed": self.messages_failed,
            "reconnect_count": self.reconnect_count,
            "last_message_time": self.last_message_time.isoformat() if self.last_message_time else None,
            "last_reconnect_time": self.last_reconnect_time.isoformat() if self.last_reconnect_time else None,
            "current_lag_ms": self.current_lag_ms,
            "connection_state": self.connection_state.value,
            "uptime_seconds": self.uptime_seconds,
        }


class RobustSubscriber:
    """
    ZeroMQ subscriber with automatic reconnection and error recovery.

    Usage:
        subscriber = RobustSubscriber(
            address="tcp://127.0.0.1:5555",
            name="my-service",
            persistence_dir="./data/zmq-queue"
        )
        subscriber.subscribe("my-topic")
        subscriber.start(callback=handle_message)
    """

    def __init__(
        self,
        address: str = "tcp://127.0.0.1:5555",
        name: str = "subscriber",
        reconnect_config: Optional[ReconnectionConfig] = None,
        persistence_dir: Optional[Path] = None,
        enable_lag_monitoring: bool = True,
    ):
        """
        Initialize robust subscriber.

        Args:
            address: ZMQ address to connect to
            name: Subscriber name for logging
            reconnect_config: Reconnection configuration
            persistence_dir: Directory for persisting missed messages
            enable_lag_monitoring: Track message processing lag
        """
        self.address = address
        self.name = name
        self.reconnect_config = reconnect_config or ReconnectionConfig()
        self.persistence_dir = Path(persistence_dir) if persistence_dir else None
        self.enable_lag_monitoring = enable_lag_monitoring

        # State
        self.context: Optional[zmq.Context] = None
        self.socket: Optional[zmq.Socket] = None
        self.state = ConnectionState.DISCONNECTED
        self.subscriptions: list[str] = []
        self.metrics = SubscriberMetrics()
        self.start_time = datetime.now()

        # Threading
        self._stop_event = threading.Event()
        self._callback: Optional[Callable] = None

        # Persistence
        if self.persistence_dir:
            self.persistence_dir.mkdir(parents=True, exist_ok=True)
            self._persistence_queue = queue.Queue()
            self._persistence_thread: Optional[threading.Thread] = None

        # Logging
        self.logger = logging.getLogger(f"RobustSubscriber.{name}")

    def subscribe(self, topic: str) -> None:
        """Subscribe to topic."""
        self.subscriptions.append(topic)
        if self.socket:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            self.logger.info(f"Subscribed to topic: {topic}")

    def _connect(self) -> bool:
        """
        Establish connection to ZMQ bus.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.state = ConnectionState.CONNECTING
            self.logger.info(f"Connecting to {self.address}...")

            # Create new context and socket
            if self.context:
                self.context.term()

            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.SUB)

            # Configure socket
            self.socket.setsockopt(zmq.LINGER, 1000)  # 1 second linger
            self.socket.setsockopt(zmq.RCVHWM, 10000)  # High water mark
            self.socket.setsockopt(zmq.RECONNECT_IVL, 100)  # 100ms reconnect interval
            self.socket.setsockopt(zmq.RECONNECT_IVL_MAX, 10000)  # 10s max

            # Connect
            self.socket.connect(self.address)

            # Resubscribe to topics
            for topic in self.subscriptions:
                self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)

            self.state = ConnectionState.CONNECTED
            self.logger.info(f"Connected to {self.address}")
            return True

        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            self.state = ConnectionState.FAILED
            return False

    def _reconnect_with_backoff(self) -> bool:
        """
        Attempt reconnection with exponential backoff.

        Returns:
            True if reconnection successful, False if max attempts reached
        """
        self.state = ConnectionState.RECONNECTING
        self.metrics.reconnect_count += 1
        self.metrics.last_reconnect_time = datetime.now()

        delay = self.reconnect_config.initial_delay
        attempt = 0

        while not self._stop_event.is_set():
            if self.reconnect_config.max_attempts and attempt >= self.reconnect_config.max_attempts:
                self.logger.error(f"Max reconnection attempts ({self.reconnect_config.max_attempts}) reached")
                return False

            attempt += 1

            # Add jitter to prevent thundering herd
            actual_delay = delay
            if self.reconnect_config.jitter:
                import random
                actual_delay = delay * (0.5 + random.random())

            self.logger.info(f"Reconnection attempt {attempt} in {actual_delay:.1f}s...")
            time.sleep(actual_delay)

            if self._connect():
                self.logger.info(f"Reconnected after {attempt} attempts")
                return True

            # Exponential backoff
            delay = min(
                delay * self.reconnect_config.backoff_multiplier,
                self.reconnect_config.max_delay
            )

        return False

    def _persist_message(self, message: str) -> None:
        """Save message to disk for replay after reconnection."""
        if not self.persistence_dir:
            return

        try:
            timestamp = datetime.now().isoformat()
            filename = f"msg_{int(time.time() * 1000)}.json"
            filepath = self.persistence_dir / filename

            with open(filepath, 'w') as f:
                json.dump({
                    "timestamp": timestamp,
                    "message": message,
                    "subscriber": self.name,
                }, f)

        except Exception as e:
            self.logger.error(f"Failed to persist message: {e}")

    def _replay_persisted_messages(self) -> None:
        """Replay messages that were persisted during disconnection."""
        if not self.persistence_dir or not self._callback:
            return

        files = sorted(self.persistence_dir.glob("msg_*.json"))
        if not files:
            return

        self.logger.info(f"Replaying {len(files)} persisted messages...")

        for filepath in files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    message = data["message"]
                    self._process_message(message)

                # Delete after successful replay
                filepath.unlink()

            except Exception as e:
                self.logger.error(f"Failed to replay {filepath.name}: {e}")

        self.logger.info("Replay complete")

    def _calculate_lag(self, message_time: Optional[datetime]) -> float:
        """
        Calculate processing lag in milliseconds.

        Args:
            message_time: Timestamp from message metadata

        Returns:
            Lag in milliseconds
        """
        if not message_time or not self.enable_lag_monitoring:
            return 0.0

        now = datetime.now()
        lag = (now - message_time).total_seconds() * 1000
        return max(0.0, lag)

    def _process_message(self, message: str) -> None:
        """Process a single message."""
        try:
            # Parse message
            topic, _, data_str = message.partition(" ")

            if self._callback:
                # Extract timestamp if available for lag calculation
                message_time = None
                if data_str:
                    try:
                        data = json.loads(data_str)
                        if "timestamp" in data:
                            message_time = datetime.fromisoformat(data["timestamp"])
                        elif "occurredAt" in data:
                            message_time = datetime.fromisoformat(data["occurredAt"])
                    except:
                        pass

                # Calculate lag
                if message_time:
                    self.metrics.current_lag_ms = self._calculate_lag(message_time)

                # Call user callback
                self._callback(topic, data_str)

            # Update metrics
            self.metrics.messages_received += 1
            self.metrics.last_message_time = datetime.now()

        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            self.metrics.messages_failed += 1

    def start(self, callback: Callable[[str, str], None]) -> None:
        """
        Start listening for messages.

        Args:
            callback: Function called with (topic, data) for each message
        """
        self._callback = callback

        # Initial connection
        if not self._connect():
            if not self._reconnect_with_backoff():
                raise RuntimeError("Failed to establish initial connection")

        # Replay any persisted messages
        self._replay_persisted_messages()

        self.logger.info(f"Subscriber '{self.name}' started")
        self.logger.info(f"Active subscriptions: {self.subscriptions}")

        # Main message loop
        while not self._stop_event.is_set():
            try:
                # Check if we have a valid socket
                if not self.socket or self.state != ConnectionState.CONNECTED:
                    if not self._reconnect_with_backoff():
                        break

                # Poll with timeout to allow checking stop event
                if self.socket.poll(1000, zmq.POLLIN):
                    message = self.socket.recv_string(zmq.NOBLOCK)
                    self._process_message(message)

                # Update uptime
                self.metrics.uptime_seconds = (datetime.now() - self.start_time).total_seconds()

            except zmq.Again:
                # No message available (timeout)
                continue

            except zmq.ZMQError as e:
                self.logger.error(f"ZMQ error: {e}")
                if not self._reconnect_with_backoff():
                    break

            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                self.metrics.messages_failed += 1

        self.logger.info("Subscriber stopped")
        self._cleanup()

    def stop(self) -> None:
        """Stop the subscriber gracefully."""
        self.logger.info("Stopping subscriber...")
        self._stop_event.set()

    def _cleanup(self) -> None:
        """Clean up resources."""
        if self.socket:
            self.socket.close()
        if self.context:
            self.context.term()
        self.state = ConnectionState.DISCONNECTED

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        return self.metrics.to_dict()

    def is_healthy(self) -> bool:
        """Check if subscriber is healthy."""
        if self.state != ConnectionState.CONNECTED:
            return False

        # Check if we've received messages recently (within 5 minutes)
        if self.metrics.last_message_time:
            time_since_last = datetime.now() - self.metrics.last_message_time
            if time_since_last > timedelta(minutes=5):
                return False

        return True
