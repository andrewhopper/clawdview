# Talking Avatar Domain Model

**Version:** 1.0.0
**Status:** PENDING APPROVAL
**Created:** 2025-11-25

## Overview

Comprehensive domain model for AI-powered talking avatar systems like HeyGen, D-ID, and Synthesia. Supports both async video generation and real-time streaming avatars.

## Research Sources

This domain model is grounded in industry-leading APIs and platforms:

### Provider APIs Analyzed
- **[HeyGen API](https://docs.heygen.com/)**: Avatar video generation, photo avatars, streaming API
- **[D-ID](https://aloa.co/ai/comparisons/ai-video-comparison/d-id-vs-synthesia)**: Affordable talking head generation, instant avatars
- **[Synthesia](https://www.synthesia.io/alternatives/synthesia-vs-d-id)**: 230+ avatars, enterprise features, 120+ languages
- **[API Comparison 2025](https://a2e.ai/top-5-best-avatar-apis-2025/)**: HeyGen, D-ID, Synthesia, Tavus, A2E

### Schema.org
- **[VideoObject](https://schema.org/VideoObject)**: Standard video metadata structure
- **MediaObject**: Base for video/image/audio content
- **Person**: Avatar metadata alignment

### Key Insights
- **Dual Modes**: Async generation (2-10 min) vs real-time streaming (WebRTC)
- **Avatar Types**: Stock CGI, photo-based, custom trained, instant (single photo)
- **Multi-provider**: Each provider has unique strengths (cost, quality, speed)
- **Voice Options**: Native provider voices or external TTS (ElevenLabs, Polly)
- **Workflow Patterns**: Training → generation → delivery

---

## Domain Summary

### 📊 Entities (9 Core + 1 Support)

| Entity | Purpose | Key Features |
|--------|---------|--------------|
| **Avatar** | Digital character | Photo/CGI/custom, gender, style, poses |
| **Voice** | Voice profile | Multi-provider, cloned voices, language/accent |
| **AvatarVideo** | Generated video | Async generation, status tracking, webhooks |
| **Scene** | Background template | Custom backgrounds, positioning, sizing |
| **AvatarTrainingJob** | Custom avatar creation | Photo upload, training status, 10-60 min |
| **StreamingSession** | Real-time interaction | WebRTC, interactive conversations |
| **StreamingMessage** | Chat with avatar | Text, emotion, tasks, interrupts |
| **AvatarEmotion** | Facial expressions | 12 emotions with intensity levels |
| *(Support)* **User** | Owner reference | From auth/core domain |

### 🎯 Actions (20 Operations)

**Avatar Management (5)**
- `ListAvatarsAction`, `GetAvatarAction`, `CreateInstantAvatarAction`
- `StartAvatarTrainingAction`, `CheckTrainingStatusAction`, `CancelTrainingAction`

**Voice Management (3)**
- `ListVoicesAction`, `GetVoiceAction`, `CloneVoiceAction`

**Video Generation (5)**
- `CreateAvatarVideoAction`, `GetVideoStatusAction`, `CancelVideoGenerationAction`
- `ListVideosAction`, `BatchCreateVideosAction`

**Scene Management (2)**
- `ListScenesAction`, `CreateCustomSceneAction`

**Streaming (5)**
- `StartStreamingSessionAction`, `SendStreamingMessageAction`, `EndStreamingSessionAction`
- `GetStreamingSessionStatusAction`

### 🏷️ Enums (17 Categories)

| Enum | Values | Use Case |
|------|--------|----------|
| `AvatarType` | talking_photo, cgi_avatar, custom, instant | Generation method |
| `AvatarProvider` | heygen, d_id, synthesia, tavus, custom | Service routing |
| `AvatarStyle` | realistic, cartoon, anime, professional, casual | Visual aesthetic |
| `VoiceProvider` | heygen, elevenlabs, aws_polly, openai_tts, azure_tts, google_tts | TTS routing |
| `VoiceStyle` | conversational, professional, cheerful, calm, energetic | Delivery tone |
| `VideoStatus` | pending, processing, completed, failed, cancelled | Lifecycle tracking |
| `VideoQuality` | sd, hd, full_hd, 2k, 4k | Resolution |
| `AspectRatio` | 16:9, 9:16, 1:1, 4:5, 4:3, 21:9 | Format (YouTube, TikTok, etc.) |
| `StreamingStatus` | initializing, connecting, active, paused, ended | Session state |
| `AvatarEmotion` | neutral, happy, sad, surprised, angry, excited, etc. | Facial expressions |

*Full enum list: 17 categories, 100+ values*

---

## Use Cases

### 1️⃣ Quick Video Generation (5-10 min)
```
1. List stock avatars (professional female)
2. List voices (en-US, professional)
3. Create video with script
4. Poll until complete
5. Download video URL
```

### 2️⃣ Custom Avatar Video (15-70 min)
```
1. Upload 8 photos → start training
2. Wait for training (10-60 min)
3. Generate video with custom avatar
4. Deliver to customer
```

### 3️⃣ Real-Time Streaming (Interactive)
```
1. Start streaming session (WebRTC)
2. Send text messages to avatar
3. Avatar speaks in real-time
4. End session when done
```

### 4️⃣ Voice Cloning + Video
```
1. Clone voice from audio samples
2. Choose stock avatar
3. Generate video with custom voice
```

### 5️⃣ Batch Content Creation
```
1. Generate 50 videos with different scripts
2. A/B test different avatars/voices
3. Localize to 20 languages
```

---

## Cross-Domain Dependencies

### Core Domain (Required)
- `TimePoint`: Timestamps
- `Duration`: Video/session length
- `MediaObject`: Images, videos, audio files
- `Person`: Avatar metadata

### TTS Domain (Optional)
- `Voice`: Advanced voice synthesis
- `SynthesisRequest`: Custom TTS parameters
- Integration: Can compose `tts.Voice` for enhanced voice control

### Workflow Domain (Optional)
- `WorkflowInstance`: Multi-step video generation with approvals
- Use case: Enterprise content approval workflows

### Auth Domain (Required)
- `User`: Owner of custom avatars, videos, sessions

---

## Provider Feature Matrix

| Feature | HeyGen | D-ID | Synthesia | Tavus |
|---------|--------|------|-----------|-------|
| Stock Avatars | ✅ 100+ | ✅ 30+ | ✅ 230+ | ✅ 50+ |
| Photo Avatar | ✅ | ✅ (instant) | ❌ | ✅ |
| Custom Training | ✅ | ✅ | ✅ | ✅ |
| Streaming (WebRTC) | ✅ | ❌ | ❌ | ✅ |
| Languages | 40+ | 119 | 120+ | 30+ |
| Pricing | $$ | $ | $$$ | $$ |
| Best For | Balance | Speed/Cost | Enterprise | Personalization |

---

## Implementation Examples

### TypeScript Usage
```typescript
import {
  Avatar,
  AvatarVideo,
  Voice,
  CreateAvatarVideoAction
} from '@protoflow/semantic/domains/talking-avatar';

// Create video
const video: AvatarVideo = await CreateAvatarVideoAction({
  avatar_id: 'uuid-of-avatar',
  voice_id: 'uuid-of-voice',
  script_text: 'Hello! Welcome to our product demo.',
  aspect_ratio: '16:9',
  video_quality: 'hd'
});

// Poll for completion
while (video.status === 'processing') {
  await sleep(5000);
  video = await GetVideoStatusAction({ video_id: video.id });
}

console.log(`Video ready: ${video.output_url}`);
```

### Python Usage
```python
from protoflow.semantic.domains.talking_avatar import (
    Avatar,
    AvatarVideo,
    CreateAvatarVideoAction,
)

# Create video
video = CreateAvatarVideoAction(
    avatar_id='uuid-of-avatar',
    voice_id='uuid-of-voice',
    script_text='Hello! Welcome to our product demo.',
    aspect_ratio='16:9',
    video_quality='hd'
)

# Poll for completion
while video.status == 'processing':
    time.sleep(5)
    video = GetVideoStatusAction(video_id=video.id)

print(f"Video ready: {video.output_url}")
```

---

## Data Model Statistics

- **Entities:** 9 core + 1 support (User)
- **Properties:** 150+ typed fields
- **Enums:** 17 categories, 100+ values
- **Actions:** 20 operations
- **Relationships:** 15 defined relationships
- **Workflows:** 4 common patterns
- **Lines of YAML:** ~1,200 lines

---

## Design Decisions

### ✅ Multi-Provider Support
**Decision:** Support HeyGen, D-ID, Synthesia, Tavus, and custom providers
**Rationale:** Each provider has different strengths. Apps should be able to route based on use case.

### ✅ Async + Streaming Modes
**Decision:** Separate entities for `AvatarVideo` (async) and `StreamingSession` (real-time)
**Rationale:** Different use cases with different technical requirements (polling vs WebRTC).

### ✅ Custom Avatars/Voices
**Decision:** Support both stock and user-trained avatars/voices
**Rationale:** HeyGen research shows custom avatars are key differentiator for enterprise.

### ✅ Emotion Support
**Decision:** `AvatarEmotion` entity with 12 emotion types
**Rationale:** D-ID and HeyGen support emotion control. Critical for expressive videos.

### ✅ Scene/Background Flexibility
**Decision:** Separate `Scene` entity with multiple background types
**Rationale:** Professional videos need branded backgrounds (office, studio, custom).

### ✅ TTS Domain Integration
**Decision:** Reference existing `tts` domain rather than duplicate
**Rationale:** Voice synthesis is reusable across domains. Compose, don't duplicate.

---

## Files

```
shared/domain-models/talking-avatar/
├── README.md              # This file
├── models.yaml            # 9 entities, 150+ properties
├── enums.yaml             # 17 enum types, 100+ values
├── relationships.yaml     # 15 relationships + cross-domain
└── actions.yaml           # 20 actions + 4 workflows
```

---

## Next Steps

**After human approval:**

1. ✅ Register in `shared/semantic/domains/registry.yaml`
2. ✅ Generate TypeScript types
3. ✅ Generate Python types
4. ✅ Create provider abstraction layer (route to HeyGen, D-ID, etc.)
5. ✅ Build prototype using this domain

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-25 | Initial proposal |

