"""
TTS Domain Model - Python Types
Auto-generated from ontology.ttl
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# ----------------
# ENUMS
# ----------------

class ProviderType(str, Enum):
    """TTS provider types."""
    ELEVENLABS = "elevenlabs"
    AWS_POLLY = "aws_polly"
    OPENAI = "openai"
    GOOGLE_TTS = "google_tts"
    AZURE = "azure"


class AudioFormat(str, Enum):
    """Supported audio formats."""
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    PCM = "pcm"
    FLAC = "flac"

    @property
    def content_type(self) -> str:
        return {
            AudioFormat.MP3: "audio/mpeg",
            AudioFormat.WAV: "audio/wav",
            AudioFormat.OGG: "audio/ogg",
            AudioFormat.PCM: "audio/pcm",
            AudioFormat.FLAC: "audio/flac",
        }[self]


class SynthesisStatus(str, Enum):
    """Synthesis request status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    STREAMING = "streaming"


class DeliveryMode(str, Enum):
    """Audio delivery mode."""
    FILE_GENERATION = "file_generation"
    REALTIME_STREAM = "realtime_stream"
    WEBSOCKET = "websocket"


class ModelType(str, Enum):
    """TTS model types."""
    MULTILINGUAL_V2 = "eleven_multilingual_v2"
    TURBO_V2 = "eleven_turbo_v2"
    TURBO_V2_5 = "eleven_turbo_v2_5"
    NEURAL = "neural"
    STANDARD = "standard"


# ----------------
# ENTITIES
# ----------------

@dataclass
class VoiceSettings:
    """Fine-tuned voice parameters."""
    stability: float = 0.5
    """Voice stability (0.0-1.0). Higher = more consistent."""
    similarity_boost: float = 0.75
    """Voice clarity (0.0-1.0). Higher = clearer."""
    style: float = 0.0
    """Style exaggeration (0.0-1.0)."""
    use_speaker_boost: bool = True
    """Enhance similarity to original speaker."""
    speed: float = 1.0
    """Speaking rate (0.5-2.0)."""
    pitch: float = 0.0
    """Pitch adjustment (-20 to +20 semitones)."""


@dataclass
class Voice:
    """Voice configuration for TTS synthesis."""
    id: str
    """Provider-specific voice identifier."""
    name: str
    """Human-readable voice name."""
    provider: ProviderType
    """TTS provider for this voice."""
    language: str = "en"
    """ISO language code."""
    description: str = ""
    """Voice description."""
    preview_url: Optional[str] = None
    """URL to voice preview sample."""
    is_cloned: bool = False
    """Whether voice is cloned."""
    gender: Optional[str] = None
    """male, female, neutral."""
    age_group: Optional[str] = None
    """young, middle-aged, old."""
    use_case: Optional[str] = None
    """narration, conversational, etc."""


@dataclass
class Provider:
    """TTS provider configuration."""
    name: str
    """Provider name."""
    type: ProviderType
    """Provider type."""
    api_endpoint: Optional[str] = None
    """API endpoint URL."""
    supports_streaming: bool = True
    """Whether streaming is supported."""
    supports_voice_cloning: bool = False
    """Whether voice cloning is supported."""
    supported_formats: list[AudioFormat] = field(default_factory=lambda: [AudioFormat.MP3])
    """Supported audio formats."""
    supported_languages: list[str] = field(default_factory=lambda: ["en"])
    """Supported languages (ISO codes)."""
    rate_limit: Optional[int] = None
    """Requests per minute."""
    cost_per_char: Optional[float] = None
    """USD cost per character."""


@dataclass
class SynthesisRequest:
    """Request to synthesize text to speech."""
    id: str
    """Unique request identifier."""
    text: str
    """Text to convert to speech."""
    output_format: AudioFormat = AudioFormat.MP3
    """Output audio format."""
    delivery_mode: DeliveryMode = DeliveryMode.FILE_GENERATION
    """Delivery mode (file or stream)."""
    voice: Optional[Voice] = None
    """Voice to use."""
    voice_id: Optional[str] = None
    """Voice ID (alternative to voice object)."""
    provider: Optional[ProviderType] = None
    """Provider to use."""
    model: Optional[ModelType] = None
    """Model for synthesis."""
    voice_settings: Optional[VoiceSettings] = None
    """Fine-tuned voice settings."""
    requested_at: datetime = field(default_factory=datetime.utcnow)
    """Request timestamp."""
    callback_url: Optional[str] = None
    """Async completion callback."""


@dataclass
class AudioFile:
    """Generated audio file."""
    format: AudioFormat
    """Audio format."""
    size_bytes: int
    """File size in bytes."""
    duration_ms: int
    """Duration in milliseconds."""
    sample_rate: int = 44100
    """Sample rate in Hz."""
    channels: int = 1
    """Audio channels (1=mono, 2=stereo)."""
    file_path: Optional[str] = None
    """Local file path."""
    file_url: Optional[str] = None
    """Remote URL (S3, CDN)."""
    presigned_url: Optional[str] = None
    """Time-limited access URL."""
    expires_at: Optional[datetime] = None
    """When presigned URL expires."""
    bitrate: Optional[int] = None
    """Bitrate in kbps."""
    content_hash: Optional[str] = None
    """SHA256 hash for deduplication."""


@dataclass
class UsageMetrics:
    """Synthesis usage metrics."""
    character_count: int
    """Characters processed."""
    estimated_cost: float
    """Estimated cost in USD."""
    provider_used: ProviderType
    """Provider used."""
    model_used: Optional[ModelType] = None
    """Model used."""
    voice_used: Optional[Voice] = None
    """Voice used."""


@dataclass
class SynthesisResult:
    """Result of TTS synthesis."""
    request_id: str
    """Reference to original request."""
    status: SynthesisStatus
    """Synthesis status."""
    processing_time_ms: int
    """Processing time in milliseconds."""
    audio_file: Optional[AudioFile] = None
    """Generated audio file."""
    audio_data: Optional[bytes] = None
    """Raw audio bytes."""
    error_message: Optional[str] = None
    """Error message if failed."""
    completed_at: Optional[datetime] = None
    """Completion timestamp."""
    usage_metrics: Optional[UsageMetrics] = None
    """Usage metrics."""


@dataclass
class StreamChunk:
    """Audio data chunk for streaming."""
    data: bytes
    """Audio data chunk."""
    index: int
    """Chunk index in sequence."""
    is_last: bool = False
    """Whether this is the last chunk."""


# ----------------
# CONVERSATION ENTITIES (V1.5 Diarization)
# ----------------

@dataclass
class Speaker:
    """Named speaker in a conversation with assigned voice."""
    name: str
    """Speaker name (e.g., 'Narrator', 'Wolf', 'Pig')."""
    voice: Optional[Voice] = None
    """Assigned voice for this speaker."""


@dataclass
class Passage:
    """Single segment of text spoken by one speaker."""
    text: str
    """Text content of this passage."""
    speaker: Speaker
    """Speaker for this passage."""
    order: int = 0
    """Order in conversation sequence."""


@dataclass
class Conversation:
    """Multi-voice conversation with ordered passages."""
    title: str
    """Conversation/story title."""
    passages: list[Passage]
    """Ordered list of passages."""
    speakers: list[Speaker] = field(default_factory=list)
    """All speakers in this conversation."""


# ----------------
# DEFAULTS
# ----------------

DEFAULT_VOICE_SETTINGS = VoiceSettings()
DEFAULT_AUDIO_FORMAT = AudioFormat.MP3
DEFAULT_DELIVERY_MODE = DeliveryMode.FILE_GENERATION
DEFAULT_MODEL = ModelType.MULTILINGUAL_V2
