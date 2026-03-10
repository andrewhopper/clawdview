---
name: narratize
description: Transform abstract concepts into concrete future narratives with audio and optional microsite
version: 1.0.0
triggers: ["/narratize", "create a future narrative", "write a story about"]
---

# Future Narrative Skill

**Transform abstract concepts into concrete, human-centered stories about the future.**

## Quick Start

```bash
/narratize "AI-to-AI scheduling coordination"
/narratize "adaptive interfaces" --audio
/narratize "cognitive offload for knowledge workers" --full  # story + audio + microsite
```

## Execution Flow

```
1. CONCEPT     → Extract abstract idea from input
2. OUTLINE     → Generate narrative outline (protagonist, setting, mechanism)
3. DRAFT       → Write 75-300 word story with 7 required elements
4. REVIEW      → Quality check against patterns
5. AUDIO       → [optional] Generate TTS via ElevenLabs
6. PUBLISH     → [optional] Upload to S3, generate microsite
7. RETURN      → Display story + URLs
```

## Domain Model Reference

**Location:** `hmode/hmode/shared/semantic/domains/future-narrative/`

| Entity | Description |
|--------|-------------|
| FutureVignette | Complete narrative with all metadata |
| Protagonist | Named character with demographics, occupation, goals |
| Setting | Year, location, context |
| TransformationArc | before_state → transformation → after_state |
| Scene | Concrete moment with dialogue and sensory detail |

## 7 Required Narrative Elements

### 1. THE HOOK (Opening)
Start with the **problem or struggle**. Make the reader feel the friction.

```markdown
BAD:  "Sarah uses an AI assistant."
GOOD: "Sarah's tooth has been bothering her for three days."
```

### 2. THE SOLUTION (Introduction)
Introduce the technology **naturally**, as part of the protagonist's world.

```markdown
BAD:  "The AI scheduling system works by..."
GOOD: "She mentioned it once—out loud, to no one in particular. Her AI heard it."
```

### 3. THE MECHANISM (How It Works)
Show **first principles through action**, not exposition.

```markdown
BAD:  "The AI uses machine learning to understand preferences."
GOOD: "Rox's eyes glow soft amber. But Rox is already scanning—facial micro-expressions,
       pulse rate, respiratory rhythm."
```

### 4. THE MOMENT (Concrete Scene)
A **specific interaction** with dialogue, sensory detail, timestamp.

```markdown
"Tuesday, 7:14 AM. Sam is walking his dog when it hits him..."
"Her watch buzzes at mile two of her morning run."
```

### 5. THE WITNESS (Optional but powerful)
Someone observing the transformation adds credibility.

```markdown
"Ben's mom watches from the doorway. Her son is laughing while learning to read."
"His manager said: 'Andrew, these numbers speak for themselves.'"
```

### 6. THE IMPLICATIONS (What This Means)
Three-part structure:
- For the protagonist
- For a broader group
- For society (include one tradeoff/tension)

### 7. THE SHIFT (Closing Line)
One-sentence thesis that captures the transformation.

```markdown
"Education adapts to the learner. Not the other way around."
"Humans stop feeding machines. Machines start seeing humans."
```

## 5 Narrative Patterns

### Pattern 1: Before/After Contrast
Show friction → show resolution. Works for any transformation.

### Pattern 2: Dual Protagonist
Two users, same system, completely different experiences. Shows adaptivity.

### Pattern 3: Progressive Interaction
Multiple touchpoints over time (notification → refinement → approval). Shows AI learning.

### Pattern 4: Async Validation Loop
Idea captured → AI works in background → human approves/refines → repeat. Shows collaboration.

### Pattern 5: AI-to-AI Coordination
Systems talking to each other, human sets preferences only. Shows automation.

## Implementation

### Audio Generation (ElevenLabs)

```python
import httpx
import os

NARRATOR_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam
MODEL_ID = "eleven_multilingual_v2"
API_KEY = os.getenv('ELEVENLABS_API_KEY')

async def generate_audio(text: str, output_path: str):
    """Generate MP3 from narrative text."""
    # Clean markdown formatting
    clean_text = text
    for pattern in ['# ', '## ', '### ', '**', '*', '---', '```']:
        clean_text = clean_text.replace(pattern, '')

    async with httpx.AsyncClient(
        base_url="https://api.elevenlabs.io/v1",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        timeout=120.0,
    ) as client:
        payload = {
            "text": clean_text,
            "model_id": MODEL_ID,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.4,
                "use_speaker_boost": True,
            }
        }
        response = await client.post(
            f"/text-to-speech/{NARRATOR_VOICE_ID}",
            json=payload
        )
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        return output_path
```

### S3 Publishing

```python
import boto3
import os

def publish_to_s3(file_path: str, key_prefix: str = "future-narratives") -> str:
    """Upload file to S3 and return public URL."""
    access_key = os.getenv('ASSET_DIST_AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('ASSET_DIST_AWS_ACCESS_KEY_SECRET')
    bucket = os.getenv('ASSET_DIST_AWS_BUCKET')

    s3 = boto3.client('s3',
        region_name='us-east-1',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    filename = os.path.basename(file_path)
    key = f"{key_prefix}/{filename}"

    content_type = 'audio/mpeg' if file_path.endswith('.mp3') else 'text/html'

    s3.upload_file(
        file_path, bucket, key,
        ExtraArgs={'ContentType': content_type}
    )

    return f"https://{bucket}.s3.amazonaws.com/{key}"
```

### Microsite Generation

```python
def generate_microsite_html(narratives: list[dict]) -> str:
    """Generate HTML microsite with audio players for narratives."""
    # See: projects/personal/active/motifs-microsite/index.html
    # Template includes:
    # - Dark theme with Playfair Display headers
    # - Audio player for each story
    # - Transformation type tags
    # - "The Shift" thesis callout
    pass
```

## Quality Checklist

Before finalizing any narrative:

- [ ] Named protagonist (never "a user" or "someone")
- [ ] Specific year and location
- [ ] Hook shows friction/problem first
- [ ] Mechanism shown through action, not explained
- [ ] At least one line of dialogue
- [ ] Sensory detail (what they see, hear, feel)
- [ ] 75-300 words (30 sec - 2 min read)
- [ ] "The Shift" is one clear sentence
- [ ] Implications include a tension/tradeoff

## Transformation Types

| Type | Description | Example Story |
|------|-------------|---------------|
| `operator_to_approver` | Human shifts from doing to judging | Marcus Approves |
| `interface_evolution` | UI adapts to user, not reverse | The Interface That Knows You |
| `ai_to_ai_coordination` | Systems talk, humans set preferences | Sarah's Last Hold Music |
| `personalization` | One-size-fits-one experiences | Ben's Learning Game |
| `cognitive_offload` | AI handles mental load | The System That Sees Your Work |
| `time_compression` | Weeks become days/hours | The Idea That Built Itself |
| `proactive_ai` | AI anticipates needs | The Pitch That Wrote Itself |

## Examples

**Location:** `hmode/hmode/shared/semantic/domains/future-narrative/examples/`

| File | Transformation | Read Time |
|------|----------------|-----------|
| 01-bens-learning-game.md | personalization | 2 min |
| 02-sarahs-last-hold-music.md | ai_to_ai_coordination | 2 min |
| 03-marcus-approves.md | operator_to_approver | 1 min |
| 04-the-pitch-that-wrote-itself.md | proactive_ai | 3 min |
| 05-the-notification-that-set-her-free.md | interface_evolution | 1 min |
| 06-the-interface-that-knows-you.md | interface_evolution | 2 min |
| 07-the-system-that-sees-your-work.md | cognitive_offload | 3 min |
| 08-the-idea-that-built-itself.md | time_compression | 3 min |
| 09-five-clicks-from-code.md | accessibility | 2 min |

## Dependencies

| Dependency | Purpose |
|------------|---------|
| ElevenLabs API | Text-to-speech generation |
| AWS S3 | Audio/microsite hosting |
| boto3 | S3 uploads |
| httpx | Async HTTP for ElevenLabs |

## Environment Variables

```bash
ELEVENLABS_API_KEY=sk_...
ASSET_DIST_AWS_ACCESS_KEY_ID=...
ASSET_DIST_AWS_ACCESS_KEY_SECRET=...
ASSET_DIST_AWS_BUCKET=asset-distribution-bucket-1762910336
```

## Error Handling

| Error | Resolution |
|-------|------------|
| ElevenLabs 401 | Check API key or quota |
| ElevenLabs quota exceeded | Add credits at elevenlabs.io |
| S3 SignatureDoesNotMatch | Verify AWS credentials |
| Story too short | Expand scene with more sensory detail |
| Story too long | Cut exposition, show don't tell |

## Related

- **Command:** `/narratize` - Entry point
- **Domain:** `hmode/hmode/shared/semantic/domains/future-narrative/`
- **Template:** `NARRATIVE_OUTLINE_TEMPLATE.md`
- **Microsite:** `projects/personal/active/motifs-microsite/`
- **Live site:** https://motifs.b.lfg.new
