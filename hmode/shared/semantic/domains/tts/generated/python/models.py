"""
TTS Domain Models - Pydantic
Generated from schema/tts.yaml
Version: 1.2.0
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# -----------------------------
# ENUMS
# -----------------------------

class AudioFormat(str, Enum):
    """Supported audio output formats."""
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"


class VoiceGender(str, Enum):
    """Voice gender classification."""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class VoiceAge(str, Enum):
    """Voice age classification."""
    CHILD = "child"
    YOUNG = "young"
    ADULT = "adult"
    ELDERLY = "elderly"


class TTSProvider(str, Enum):
    """Supported TTS provider backends."""
    ELEVENLABS = "elevenlabs"
    CARTESIA = "cartesia"
    DEEPGRAM = "deepgram"
    OPENAI = "openai"


# -----------------------------
# ENTITIES
# -----------------------------

class VoiceSettings(BaseModel):
    """Fine-grained voice control parameters (provider-specific)."""
    stability: Optional[float] = Field(None, description="Voice consistency (0.0-1.0, ElevenLabs)")
    similarity_boost: Optional[float] = Field(None, description="Voice similarity enhancement (0.0-1.0, ElevenLabs)")
    style: Optional[float] = Field(None, description="Expressiveness/style intensity (0.0-1.0, ElevenLabs)")
    speed: float = Field(1.0, description="Speech rate multiplier (0.5-2.0)")


class Voice(BaseModel):
    """Voice configuration for TTS synthesis."""
    id: str = Field(..., description="Provider-specific voice identifier")
    name: str = Field(..., description="Human-readable voice name")
    provider: Optional[TTSProvider] = Field(None, description="TTS provider for this voice")
    model_id: Optional[str] = Field(None, description="Provider model (eleven_turbo_v2, sonic-3, aura-2)")
    gender: Optional[VoiceGender] = Field(None, description="Voice gender")
    age: Optional[VoiceAge] = Field(None, description="Voice age group")
    language: str = Field("en", description="ISO language code (en, en-US)")
    description: Optional[str] = Field(None, description="Voice description")
    settings: Optional[VoiceSettings] = Field(None, description="Fine-grained voice control")


class Speaker(BaseModel):
    """Named speaker with assigned voice."""
    name: str = Field(..., description="Speaker name (Narrator, Wolf, Pig)")
    voice: Optional[Voice] = Field(None, description="Assigned voice for this speaker")
    voice_id: Optional[str] = Field(None, description="Voice ID (alternative to voice object)")


class Passage(BaseModel):
    """Single segment of text spoken by one speaker."""
    text: str = Field(..., description="Text content to synthesize")
    speaker: Speaker = Field(..., description="Speaker for this passage")
    order: int = Field(0, description="Order in conversation sequence")
    pause_before_ms: int = Field(0, description="Pause before this passage in milliseconds")
    pause_after_ms: int = Field(500, description="Pause after this passage in milliseconds")
    speed: Optional[float] = Field(None, description="Speed override for this passage (0.5-2.0)")


class Conversation(BaseModel):
    """Multi-voice conversation with ordered passages."""
    title: str = Field(..., description="Story/conversation title")
    passages: list[Passage] = Field(..., description="Ordered list of passages")
    speakers: Optional[list[Speaker]] = Field(None, description="All speakers in this conversation")
    output_format: AudioFormat = Field(AudioFormat.MP3, description="Output audio format")
    default_provider: Optional[TTSProvider] = Field(None, description="Default TTS provider for all voices")


class SynthesisRequest(BaseModel):
    """Request to synthesize text (V1 simple)."""
    text: str = Field(..., description="Text to synthesize")
    voice_id: str = Field(..., description="Voice ID to use")
    provider: TTSProvider = Field(TTSProvider.ELEVENLABS, description="TTS provider to use")
    model_id: Optional[str] = Field(None, description="Provider-specific model ID")
    output_format: AudioFormat = Field(AudioFormat.MP3, description="Output format")
    output_path: Optional[str] = Field(None, description="Local path to save audio")
    speed: float = Field(1.0, description="Speech rate (0.5-2.0)")


class SynthesisResult(BaseModel):
    """Result of synthesis."""
    success: bool = Field(..., description="Whether synthesis succeeded")
    audio_path: Optional[str] = Field(None, description="Path to generated audio file")
    duration_ms: Optional[int] = Field(None, description="Audio duration in milliseconds")
    error: Optional[str] = Field(None, description="Error message if failed")
