#!/usr/bin/env python3
"""
Guardrail Supervisor Process

Background process that:
1. Monitors conversation/file operations
2. Detects violations in real-time
3. Sends IPC messages to main AI process with reminders

Architecture:
┌─────────────────┐         IPC          ┌──────────────────┐
│   Supervisor    │◄──────────────────►  │   Main AI        │
│   (background)  │  (Unix socket/pipe)  │   Process        │
└─────────────────┘                      └──────────────────┘
      │
      ├─ Watches file changes
      ├─ Parses conversation logs
      ├─ Detects violations
      └─ Sends reminders

Usage:
  python3 supervisor.py start     # Start supervisor
  python3 supervisor.py stop      # Stop supervisor
  python3 supervisor.py status    # Check status
  python3 supervisor.py read      # Read pending reminders (IPC client)
"""

import argparse
import json
import os
import signal
import socket
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ============================================================================
# Configuration
# ============================================================================

def get_hostname():
    """Get normalized hostname for machine-specific files"""
    import socket
    hostname = socket.gethostname()
    # Normalize: remove .local, hyphens, dots
    return hostname.replace('.local', '').replace('-', '').replace('.', '')

REPO_ROOT = Path(__file__).parent.parent.parent
HOSTNAME = get_hostname()
PID_FILE = REPO_ROOT / ".guardrails" / ".supervisor.pid"
SOCKET_FILE = REPO_ROOT / ".guardrails" / ".supervisor.sock"
LOG_FILE = REPO_ROOT / ".guardrails" / f".supervisor-{HOSTNAME}.log"
REMINDERS_QUEUE = REPO_ROOT / ".guardrails" / ".reminders_queue.json"

PUBLISHABLE_EXTENSIONS = {".html", ".pdf", ".svg", ".zip", ".mp3", ".mp4"}


# ============================================================================
# IPC Protocol
# ============================================================================

@dataclass
class IPCMessage:
    """Message sent via IPC"""
    type: str  # "reminder", "violation", "status"
    severity: str  # "low", "medium", "high", "critical"
    payload: Dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class IPCServer:
    """Unix socket IPC server"""

    def __init__(self, socket_path: Path):
        self.socket_path = socket_path
        self.socket = None
        self.running = False
        self.message_queue = []

    def start(self):
        """Start IPC server"""
        # Remove existing socket
        if self.socket_path.exists():
            self.socket_path.unlink()

        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(str(self.socket_path))
        self.socket.listen(5)
        self.running = True

        # Start listener thread
        listener_thread = threading.Thread(target=self._listen, daemon=True)
        listener_thread.start()

        log(f"IPC server started on {self.socket_path}")

    def stop(self):
        """Stop IPC server"""
        self.running = False
        if self.socket:
            self.socket.close()
        if self.socket_path.exists():
            self.socket_path.unlink()

    def _listen(self):
        """Listen for client connections"""
        while self.running:
            try:
                self.socket.settimeout(1.0)
                conn, addr = self.socket.accept()
                self._handle_client(conn)
            except socket.timeout:
                continue
            except Exception as e:
                log(f"IPC error: {e}")

    def _handle_client(self, conn):
        """Handle client request"""
        try:
            # Client can request pending messages
            request = conn.recv(1024).decode()

            if request == "GET_REMINDERS":
                # Send all pending reminders
                response = json.dumps(self.message_queue)
                conn.sendall(response.encode())

                # Clear queue after sending
                self.message_queue.clear()

            elif request == "STATUS":
                status = {
                    "running": self.running,
                    "queue_size": len(self.message_queue),
                    "timestamp": datetime.now().isoformat()
                }
                conn.sendall(json.dumps(status).encode())

        except Exception as e:
            log(f"Client handler error: {e}")
        finally:
            conn.close()

    def send_reminder(self, reminder: IPCMessage):
        """Add reminder to queue"""
        self.message_queue.append({
            "type": reminder.type,
            "severity": reminder.severity,
            "payload": reminder.payload,
            "timestamp": reminder.timestamp
        })
        log(f"Reminder queued: {reminder.payload.get('message', '')[:50]}")


# ============================================================================
# File System Monitor
# ============================================================================

class GuardrailFileHandler(FileSystemEventHandler):
    """Watches for file changes and detects violations"""

    def __init__(self, ipc_server: IPCServer):
        self.ipc_server = ipc_server

    def on_created(self, event):
        """Handle file creation"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        self._check_file(file_path, "created")

    def on_modified(self, event):
        """Handle file modification"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        self._check_file(file_path, "modified")

    def _check_file(self, file_path: Path, operation: str):
        """Check file for violations"""
        # Skip hidden files and system files
        if file_path.name.startswith('.'):
            return

        # Check S3 publishing
        if file_path.suffix in PUBLISHABLE_EXTENSIONS:
            if not self._has_s3_evidence(file_path):
                reminder = IPCMessage(
                    type="reminder",
                    severity="medium",
                    payload={
                        "rule": "s3_publish_missing",
                        "file": str(file_path),
                        "message": f"⚠️ File '{file_path.name}' is publishable but not published to S3. Prompt user: 'Publish {file_path.name} to S3? [1] Public [2] Temp [3] Private [4] Skip'"
                    }
                )
                self.ipc_server.send_reminder(reminder)
                log(f"S3 publish reminder for: {file_path.name}")

        # Check shared models (TypeScript)
        if file_path.suffix == ".ts":
            violations = self._check_shared_models(file_path)
            for violation in violations:
                reminder = IPCMessage(
                    type="violation",
                    severity="high",
                    payload=violation
                )
                self.ipc_server.send_reminder(reminder)

    def _has_s3_evidence(self, file_path: Path) -> bool:
        """Check for S3 publish evidence"""
        skip_markers = [".s3-skip", ".no-publish", f"{file_path.name}.s3-published"]
        return any((file_path.parent / marker).exists() for marker in skip_markers)

    def _check_shared_models(self, file_path: Path) -> List[Dict]:
        """Check for shared model violations"""
        violations = []

        try:
            import re
            with open(file_path) as f:
                content = f.read()

            # Find local type definitions
            local_types = re.findall(r'(?:interface|type|class)\s+([A-Z][a-zA-Z0-9]*)', content)

            # Load registry and check
            registry = self._load_registry()
            for type_name in local_types:
                domain = self._find_domain_for_type(type_name, registry)
                if domain:
                    violations.append({
                        "rule": "shared_model_not_used",
                        "file": str(file_path),
                        "type_name": type_name,
                        "domain": domain,
                        "message": f"🚨 Type '{type_name}' defined locally but exists in shared/semantic/domains/{domain}/. Use shared model."
                    })

        except Exception:
            pass

        return violations

    def _load_registry(self) -> Dict:
        """Load domain registry"""
        registry_path = REPO_ROOT / "shared" / "semantic" / "domains" / "registry.yaml"
        if not registry_path.exists():
            return {}

        try:
            import yaml
            with open(registry_path) as f:
                data = yaml.safe_load(f)
                registry = {}
                for domain in data.get("domains", []):
                    domain_name = domain.get("name")
                    entities = domain.get("entities", [])
                    if domain_name:
                        registry[domain_name] = entities
                return registry
        except Exception:
            return {}

    def _find_domain_for_type(self, type_name: str, registry: Dict) -> Optional[str]:
        """Find domain containing type"""
        for domain, entities in registry.items():
            if type_name in entities:
                return domain
        return None


# ============================================================================
# Supervisor Process
# ============================================================================

class GuardrailSupervisor:
    """Main supervisor process"""

    def __init__(self):
        self.ipc_server = IPCServer(SOCKET_FILE)
        self.observer = None
        self.running = False

    def start(self):
        """Start supervisor"""
        log("Starting Guardrail Supervisor...")

        # Check if already running
        if PID_FILE.exists():
            try:
                with open(PID_FILE) as f:
                    pid = int(f.read().strip())
                    os.kill(pid, 0)  # Check if process exists
                    log(f"Supervisor already running (PID {pid})")
                    return
            except (OSError, ValueError):
                # Process not running, remove stale PID file
                PID_FILE.unlink()

        # Write PID file
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))

        # Start IPC server
        self.ipc_server.start()

        # Start file system observer
        self.observer = Observer()
        event_handler = GuardrailFileHandler(self.ipc_server)

        # Watch key directories
        watch_dirs = [
            REPO_ROOT / "prototypes",
            REPO_ROOT / "project-management" / "ideas",
        ]

        for watch_dir in watch_dirs:
            if watch_dir.exists():
                self.observer.schedule(event_handler, str(watch_dir), recursive=True)
                log(f"Watching: {watch_dir}")

        self.observer.start()
        self.running = True

        log("Supervisor started successfully")
        log(f"PID: {os.getpid()}")
        log(f"Socket: {SOCKET_FILE}")

        # Run forever
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop supervisor"""
        log("Stopping Guardrail Supervisor...")

        self.running = False

        if self.observer:
            self.observer.stop()
            self.observer.join()

        self.ipc_server.stop()

        if PID_FILE.exists():
            PID_FILE.unlink()

        log("Supervisor stopped")

    def status(self):
        """Check supervisor status"""
        if not PID_FILE.exists():
            print("Supervisor not running")
            return False

        try:
            with open(PID_FILE) as f:
                pid = int(f.read().strip())

            os.kill(pid, 0)  # Check if process exists
            print(f"Supervisor running (PID {pid})")
            print(f"Socket: {SOCKET_FILE}")
            print(f"Log: {LOG_FILE}")
            return True

        except (OSError, ValueError):
            print("Supervisor not running (stale PID file)")
            PID_FILE.unlink()
            return False


# ============================================================================
# IPC Client
# ============================================================================

class IPCClient:
    """Client to read reminders from supervisor"""

    def __init__(self, socket_path: Path):
        self.socket_path = socket_path

    def get_reminders(self) -> List[Dict]:
        """Get pending reminders from supervisor"""
        if not self.socket_path.exists():
            return []

        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(str(self.socket_path))
            client.sendall(b"GET_REMINDERS")

            response = client.recv(4096).decode()
            client.close()

            return json.loads(response)

        except Exception as e:
            log(f"IPC client error: {e}")
            return []

    def get_status(self) -> Optional[Dict]:
        """Get supervisor status"""
        if not self.socket_path.exists():
            return None

        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(str(self.socket_path))
            client.sendall(b"STATUS")

            response = client.recv(4096).decode()
            client.close()

            return json.loads(response)

        except Exception:
            return None


# ============================================================================
# Utilities
# ============================================================================

def log(message: str):
    """Write to log file"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Guardrail supervisor process")
    parser.add_argument("command", choices=["start", "stop", "status", "read", "daemon"],
                       help="Command to execute")

    args = parser.parse_args()

    supervisor = GuardrailSupervisor()

    if args.command == "start":
        supervisor.start()

    elif args.command == "daemon":
        # Start as daemon (background process)
        pid = os.fork()
        if pid > 0:
            print(f"Supervisor started as daemon (PID {pid})")
            sys.exit(0)

        # Child process
        os.setsid()
        supervisor.start()

    elif args.command == "stop":
        if not PID_FILE.exists():
            print("Supervisor not running")
            return

        with open(PID_FILE) as f:
            pid = int(f.read().strip())

        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Stopped supervisor (PID {pid})")
        except OSError:
            print("Supervisor not running (stale PID)")
            PID_FILE.unlink()

    elif args.command == "status":
        supervisor.status()

    elif args.command == "read":
        # Read pending reminders (IPC client)
        client = IPCClient(SOCKET_FILE)
        reminders = client.get_reminders()

        if not reminders:
            print("No pending reminders")
            return

        print("🤖 ACTIVE GUARDRAIL REMINDERS:")
        for i, reminder in enumerate(reminders, 1):
            print(f"\n{i}. [{reminder['severity'].upper()}] {reminder['type']}")
            print(f"   {reminder['payload'].get('message', '')}")


if __name__ == "__main__":
    main()
