# TTS Domain Model

Multi-provider text-to-speech abstraction layer supporting ElevenLabs, AWS Polly, OpenAI TTS, and more.

## 1.0 Overview

**Purpose:** Canonical domain model for TTS operations enabling provider-agnostic audio synthesis.

**Use Cases:**
- Neuro-adaptive layer auditory modality
- Voice assistants and conversational AI
- Audiobook and podcast generation
- Accessibility tools (screen readers)
- E-learning narrated content

## 2.0 Entities

| Entity | Description |
|--------|-------------|
| `SynthesisRequest` | Request to synthesize text with voice, format, and delivery options |
| `SynthesisResult` | Result containing audio data/URL, status, and metrics |
| `Voice` | Voice configuration with provider, language, and characteristics |
| `Provider` | TTS provider (ElevenLabs, Polly, OpenAI) with capabilities |
| `AudioFile` | Generated audio with format, duration, and storage location |
| `VoiceSettings` | Fine-tuned voice parameters (stability, similarity, style) |
| `StreamChunk` | Audio data chunk for streaming playback |
| `UsageMetrics` | Character count, cost, and usage statistics |

## 3.0 Enums

| Enum | Values |
|------|--------|
| `ProviderType` | ElevenLabs, AWSPolly, OpenAI, GoogleTTS, Azure |
| `AudioFormat` | MP3, WAV, OGG, PCM, FLAC |
| `SynthesisStatus` | Pending, Processing, Completed, Failed, Streaming |
| `DeliveryMode` | FileGeneration, RealTimeStream, WebSocket |
| `ModelType` | MultilingualV2, TurboV2, TurboV2_5, Neural, Standard |

## 4.0 Provider Comparison

```
┌─────────────┬──────────┬───────────┬──────────────┬─────────┐
│   Provider  │  Quality │  Latency  │ Voice Clone  │   Cost  │
├─────────────┼──────────┼───────────┼──────────────┼─────────┤
│ ElevenLabs  │  ★★★★★   │   Medium  │      Yes     │  $$$    │
│ AWS Polly   │  ★★★★    │    Low    │      No      │  $$     │
│ OpenAI TTS  │  ★★★★    │    Low    │      No      │  $      │
│ Google TTS  │  ★★★★    │    Low    │      No      │  $$     │
└─────────────┴──────────┴───────────┴──────────────┴─────────┘
```

## 5.0 Implementation

**Service Location:** `shared/services/tts/`

```python
from shared.services.tts import TTSService, ElevenLabsProvider, TTSConfig

# Initialize with ElevenLabs
provider = ElevenLabsProvider(api_key="sk_...")
tts = TTSService(provider)

# Synthesize to file
audio = await tts.synthesize(
    "Hello world",
    config=TTSConfig(voice_id="21m00Tcm4TlvDq8ikWAM"),
    output_path="output.mp3"
)

# Stream for low-latency
async for chunk in tts.stream("Hello world"):
    await websocket.send(chunk)
```

## 6.0 Voice Settings

| Parameter | Range | Description |
|-----------|-------|-------------|
| `stability` | 0.0-1.0 | Consistency vs expressiveness |
| `similarityBoost` | 0.0-1.0 | Clarity and original voice similarity |
| `style` | 0.0-1.0 | Style exaggeration |
| `speed` | 0.5-2.0 | Speaking rate |
| `pitch` | -20 to +20 | Semitone adjustment |

## 7.0 Files

```
shared/domain-models/tts/
├── ontology.ttl              # W3C RDF/OWL (canonical source)
├── rules.shacl.ttl           # SHACL validation constraints
├── version.json              # Semantic version
├── README.md                 # This file
└── generated/
    ├── typescript/tts.types.ts
    └── python/tts.py
```

## 8.0 Related

- **Service Implementation:** `shared/services/tts/`
- **Prototype:** `prototypes/proto-tts-service-*`
- **Neuro-Adaptive Layer:** `project-management/ideas/proto-neuro-adaptive-layer-*`
- **Tech Preferences:** `.guardrails/tech-preferences/ai-ml.json`
