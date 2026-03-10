"""
Story Audiobook Domain Models
Generated from schema.yaml

Multi-voice audiobook with synchronized diagrams
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# ============================================
# ENUMS
# ============================================

class AudioFormat(Enum):
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    FLAC = "flac"


class DiagramType(Enum):
    MERMAID = "mermaid"
    ASCII = "ascii"
    SVG = "svg"
    IMAGE = "image"
    TEXT = "text"


class AnimationType(Enum):
    NONE = "none"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    SLIDE_IN = "slide_in"
    SLIDE_OUT = "slide_out"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"


class SpeakerRole(Enum):
    NARRATOR = "narrator"
    CHARACTER = "character"
    CHORUS = "chorus"
    SOUND_EFFECT = "sound_effect"


class EventType(Enum):
    SHOW_DIAGRAM = "show_diagram"
    HIDE_DIAGRAM = "hide_diagram"
    START_AUDIO = "start_audio"
    END_AUDIO = "end_audio"
    SCENE_CHANGE = "scene_change"
    PAUSE = "pause"


class EventAction(Enum):
    SHOW = "show"
    HIDE = "hide"
    PLAY = "play"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


# ============================================
# ENTITIES
# ============================================

@dataclass
class Speaker:
    """Who is speaking in an audio segment"""
    id: str
    name: str
    role: SpeakerRole
    voice_id: str
    character_id: Optional[str] = None


@dataclass
class AudioSegment:
    """Single audio file spoken by one voice"""
    id: str
    segment_number: int
    speaker: Speaker
    text: str
    voice_id: str
    created_at: datetime
    updated_at: datetime
    audio_file: Optional[str] = None
    duration: Optional[int] = None  # milliseconds
    start_time: Optional[int] = None  # ms from scene beginning
    end_time: Optional[int] = None  # ms from scene beginning


@dataclass
class Diagram:
    """Visual diagram synchronized with audio timeline"""
    id: str
    title: str
    diagram_type: DiagramType
    content: str
    show_at_time: int  # ms when diagram appears
    created_at: datetime
    updated_at: datetime
    hide_at_time: Optional[int] = None  # ms when diagram disappears
    related_segments: list[str] = field(default_factory=list)
    animation_type: AnimationType = AnimationType.FADE_IN


@dataclass
class Voice:
    """TTS voice configuration for a speaker"""
    id: str
    name: str
    voice_id: str  # ElevenLabs voice ID
    created_at: datetime
    updated_at: datetime
    provider: str = "elevenlabs"
    gender: Optional[Gender] = None
    accent: Optional[str] = None
    description: Optional[str] = None
    character_id: Optional[str] = None


@dataclass
class AudiobookScene:
    """Scene with synchronized audio segments and diagrams"""
    id: str
    scene_id: str  # Reference to story.Scene
    scene_number: int
    audio_segments: list[AudioSegment]
    diagrams: list[Diagram]
    created_at: datetime
    updated_at: datetime
    title: Optional[str] = None
    start_time: Optional[int] = None  # seconds from audiobook beginning
    duration: Optional[int] = None  # seconds


@dataclass
class Audiobook:
    """Complete audiobook with scenes, audio, and visuals"""
    id: str
    story_id: str
    title: str
    scenes: list[AudiobookScene]
    voices: list[Voice]
    created_at: datetime
    updated_at: datetime
    narrator: Optional[str] = None
    total_duration: Optional[int] = None  # seconds
    format: AudioFormat = AudioFormat.MP3


@dataclass
class TimelineEvent:
    """Event that occurs at specific time during playback"""
    id: str
    timestamp: int  # ms
    event_type: EventType
    target_id: str  # Diagram or Segment ID
    action: EventAction
    metadata: Optional[dict] = None


@dataclass
class PlaybackTimeline:
    """Timeline for synchronized playback"""
    id: str
    audiobook_id: str
    total_duration: int  # ms
    events: list[TimelineEvent]
    created_at: datetime
    updated_at: datetime
