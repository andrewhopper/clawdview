# Create Interactive Audiobook

Create a complete multi-voice interactive audiobook with SVG illustrations and publish to S3.

## Workflow

**Step 1: Generate Story**
First, invoke the `/kids-story` slash command to generate the story. After the story is generated, this command will continue automatically.

**Step 2: Story Selection**
If multi-variant mode was used, ask:
```
Which variant(s) to convert to audiobook?
[1] Variant A only
[2] Variant B only
[3] Variant C only
[4] All variants
```

**Step 3: Character Voice Mapping**
Display detected characters from the story and ask for voice assignments:
```
Detected characters: [list from story]

Available AWS Polly voices:
- Joanna (female, professional narrator)
- Kevin (male, young boy)
- Justin (male, energetic young man)
- Ivy (female, young girl)
- Matthew (male, adult)
- [list all available voices from AWS Polly API]

Assign voices:
Character 1 → [voice]
Character 2 → [voice]
...

Or use defaults? [Y/n]
```

Default voice mapping:
```python
VOICES = {
    "Narrator": "Joanna",
    "Jack": "Kevin",
    "Ben": "Justin",
    "James": "Ivy",
    "Mom": "Joanna",
    "Dad": "Matthew",
    "Grammy": "Joanna",
    "Papa": "Matthew",
    "Baba": "Joanna",
}
```

**Step 4: SVG Illustrations**
Ask: **Generate SVG illustrations?**
```
[1] Auto-generate 6 SVGs per story (recommended)
[2] Use existing SVGs (provide directory)
[3] Skip illustrations (audio only)
```

If [1], analyze story and generate 6 key scene illustrations:
- Opening scene (typically travel/arrival)
- Character introduction
- Conflict/mystery introduction
- Climax/turning point
- Resolution
- Celebration/ending

**Step 5: Audio Synthesis**
```
Synthesizing audio with AWS Polly...
- Parsing [N] passages from story
- Voice mapping: [show character → voice assignments]
- Synthesizing with retry logic (handles rate limiting)
- Stitching segments with 400ms gaps
- Total duration: [X]:[XX]

✅ Audio complete: [filename].mp3
```

**Step 6: Build Interactive HTML**
```
Building interactive audiobook...
- Embedding audio as base64
- Embedding [N] SVG illustrations as base64
- Creating synchronized captions
- Adding click-to-seek functionality

✅ Audiobook complete: [filename]_audiobook.html
Size: [X.X] MB
```

**Step 7: S3 Publishing**
Ask: **Publish to S3?**
```
[1] Yes, with 30-day links (720 hours)
[2] Yes, with custom expiry (specify hours)
[3] Yes, permanent/public
[4] No, keep local only
```

If publishing multiple variants, ask:
```
Create index page linking all variants? [Y/n]
```

If yes, build and publish index.html with:
- Thumbnails (first SVG from each story)
- Titles and descriptions
- Metadata (duration, passage count, genre)
- Character lists
- Click-to-play links

**Step 8: Output**
Display final URLs and summary:
```
✅ Audiobook(s) Created!

📚 Main Index: [URL if created]

🎧 Audiobooks:
- [Story Title]: [URL] (duration, passages)
- [Story Title]: [URL] (duration, passages)

📁 Local Files:
- Story: [path]
- Audio: [path]
- HTML: [path]
- SVGs: [directory]

🔑 Project saved to: [directory]
```

## Domain Models

**Use shared TTS domain models:**
```python
from shared.domain_models.tts.generated.python.models import (
    Conversation,
    Passage,
    Speaker,
    Voice,
    VoiceSettings,
    AudioFormat,
    TTSProvider,
    VoiceGender,
    VoiceAge,
    SynthesisRequest,
    SynthesisResult
)
```

**Location:** `/home/user/protoflow/shared/domain-models/tts/`
- **Schema:** `schema/tts.yaml` (source of truth)
- **Python Models:** `generated/python/models.py` (Pydantic)

**Story Structure:**
- `Conversation` = complete audiobook with title and passages
- `Passage` = single text segment with speaker and timing
- `Speaker` = character with assigned voice
- `Voice` = ElevenLabs voice configuration with settings

## Environment Requirements

**AWS Credentials:**
- Check for AWS credentials (profile, IAM role, or environment variables)
- If not found, prompt: "AWS credentials not found. Configure AWS credentials or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
- Region: Use `us-east-1` by default or `AWS_REGION` environment variable

**S3 Environment:**
- `ASSET_DIST_AWS_ACCESS_KEY_ID`
- `ASSET_DIST_AWS_ACCESS_KEY_SECRET`
- `ASSET_DIST_AWS_BUCKET`
- `ASSET_DIST_AWS_REGION`

**Dependencies:**
- Shared domain models: `/home/user/protoflow/shared/domain-models/tts/`
- TTS service: `/home/user/protoflow/shared/services/tts/`
- S3 publisher: `/home/user/protoflow/hmode/shared/tools/s3publish.py`
- Python packages: boto3, pydub, ffmpeg

## Technical Implementation

### Story Parsing with Domain Models
```python
from shared.domain_models.tts.generated.python.models import (
    Conversation, Passage, Speaker, Voice, TTSProvider
)

# Parse story with [Speaker]: text format
pattern = r'\[(\w+(?:\s+\w+)?)\]:\s*(.+?)(?=\n\[|$)'
matches = re.findall(pattern, story_text, re.DOTALL)

# Build domain model
speakers_dict = {}
passages = []

for i, (speaker_name, text) in enumerate(matches):
    # Create or get speaker
    if speaker_name not in speakers_dict:
        voice = Voice(
            id=voice_mapping[speaker_name],
            name=voice_mapping[speaker_name],
            provider=TTSProvider.POLLY,
            model_id="neural"
        )
        speaker = Speaker(name=speaker_name, voice=voice)
        speakers_dict[speaker_name] = speaker

    # Create passage with timing
    passage = Passage(
        text=text.strip(),
        speaker=speakers_dict[speaker_name],
        order=i,
        pause_after_ms=400  # 400ms between passages
    )
    passages.append(passage)

# Create conversation
conversation = Conversation(
    title=story_title,
    passages=passages,
    speakers=list(speakers_dict.values()),
    output_format=AudioFormat.MP3,
    default_provider=TTSProvider.POLLY
)
```

### Audio Synthesis with Domain Models
```python
from shared.domain_models.tts.generated.python.models import (
    SynthesisRequest, SynthesisResult
)

# Synthesize each passage
for passage in conversation.passages:
    request = SynthesisRequest(
        text=passage.text,
        voice_id=passage.speaker.voice.id,
        provider=TTSProvider.POLLY,
        model_id="neural",
        output_format=AudioFormat.MP3,
        output_path=f"segment_{passage.order:03d}.mp3",
        speed=passage.speed or 1.0
    )

    # Retry logic for rate limiting
    result = retry_with_backoff(
        synthesize_with_request(request),
        max_retries=3,
        backoff=[5, 10, 20]
    )

    if not result.success:
        handle_error(result.error)

    time.sleep(0.5)  # Avoid rate limits

# Stitch with pydub using passage timing
combined = AudioSegment.empty()
for passage in conversation.passages:
    segment_path = f"segment_{passage.order:03d}.mp3"
    audio = AudioSegment.from_mp3(segment_path)

    # Add pause before (if specified)
    if passage.pause_before_ms > 0:
        combined += AudioSegment.silent(duration=passage.pause_before_ms)

    combined += audio

    # Add pause after
    combined += AudioSegment.silent(duration=passage.pause_after_ms)

combined.export(output_path, format="mp3")
```

### SVG Generation
Generate SVGs based on story analysis:
```python
# Extract key scenes from story structure
scenes = analyze_story_structure(story_text)
for scene in scenes:
    svg = generate_svg_from_scene(
        scene.description,
        scene.characters,
        scene.setting,
        style="children_book"
    )
    save_svg(svg, f"{output_dir}/scene_{i}.svg")
```

### HTML Audiobook
```python
# Embed all assets as base64
audio_data = base64.b64encode(audio_bytes).decode()
svg_data = [base64.b64encode(svg).decode() for svg in svgs]

# Build interactive HTML with:
# - Embedded audio player
# - Synchronized captions (speaker colors)
# - Click-to-seek on passages
# - Auto-scrolling active caption
# - Image chapters (change SVG per section)
```

### Index Page
```python
# Build landing page with:
# - Gradient background
# - Book cards (grid layout)
# - Thumbnails (first SVG from each story)
# - Metadata tags
# - Character lists
# - Play buttons linking to audiobooks
```

## File Organization

```
output_directory/
├── [story-name]/
│   ├── story.md                    # Original story text
│   ├── audio.mp3                   # Synthesized audio
│   ├── audiobook.html              # Interactive HTML
│   ├── svgs/
│   │   ├── scene_1.svg
│   │   ├── scene_2.svg
│   │   ├── ...
│   │   └── scene_6.svg
│   └── metadata.json               # Story metadata
└── index.html                      # Index page (if multiple)
```

## Error Handling

**Rate Limiting:**
- Detect throttling errors from AWS Polly
- Implement exponential backoff (5s, 10s, 20s)
- Prompt user if AWS quotas need adjustment
- Continue from last successful passage

**Missing Dependencies:**
- Check for ffmpeg, install if needed
- Verify Python packages installed
- Test AWS Polly connectivity with boto3

**S3 Upload Failures:**
- Retry with exponential backoff
- Provide local file paths as fallback
- Allow manual upload option

## Usage Examples

**Example 1: Single Story with Defaults**
```
/create-audiobook
→ Invokes /kids-story
→ User generates single story
→ Use default voice mapping? Y
→ Generate SVGs? [1] Auto-generate
→ Publish to S3? [1] 30-day links
✅ Complete!
```

**Example 2: Multi-Variant with Custom Voices**
```
/create-audiobook
→ Invokes /kids-story
→ User generates 3 variants
→ Convert which? [4] All variants
→ Custom voice mapping for each character
→ Auto-generate 6 SVGs per variant (18 total)
→ Publish with index page
✅ Complete with index linking all 3!
```

**Example 3: Audio Only**
```
/create-audiobook
→ Invokes /kids-story
→ User generates story
→ Skip illustrations [3]
→ Keep local only [4]
✅ Audio file created locally
```

## Notes

- Always use `/kids-story` generator for consistent format
- Story must use `[Speaker]: text` format for parsing
- Estimate ~3 seconds per passage for audio duration
- SVG generation uses story content analysis
- Self-contained HTML (no external dependencies)
- 30-day S3 links = 720 hours
- Supports retry logic for all network operations
- Creates project summary automatically

## Integration with Existing Tools

**Leverages:**
- `/kids-story` - Story generation (already exists)
- `shared/services/tts/` - TTS synthesis with AWS Polly
- `hmode/shared/tools/s3publish.py` - S3 publishing
- Base64 encoding for self-contained files
- pydub + ffmpeg for audio processing

**Extends:**
- Adds automated SVG generation
- Adds HTML audiobook builder
- Adds index page generator
- Adds voice mapping UI
- Adds error handling & retries
