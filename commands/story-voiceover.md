# Story Voiceover Command

Convert a story script with multiple characters into an audiobook narration using multi-voice TTS.

## Arguments
- $ARGUMENTS: Path to story script file (markdown or text)

## Script Format

The script should use this format:

```markdown
# Story Title

[Narrator]: Once upon a time, in a land far away...

[Wolf]: Little pig, little pig, let me come in!

[Pig]: Not by the hair on my chinny chin chin!

[Narrator]: And so the wolf huffed and puffed...
```

## Execution Flow

### Step 1: Parse the Script

Read the script file and extract:
- Title from first heading
- Speaker labels in `[Speaker]:` format
- Dialogue/narration text

### Step 2: Map Speakers to Voices

| Speaker Pattern | Voice | Description |
|-----------------|-------|-------------|
| Narrator | Sarah | Default narrator |
| Wolf, Giant, Villain | Brian | Deep male |
| Pig, Mouse, Hero | Charlie | Young male |
| Princess, Girl, Mother | Lily | Female character |
| King, Father, Old Man | Adam | Adult male |
| Default | Sarah | Fallback |

### Step 3: Generate Conversation YAML

Create a Conversation structure:

```yaml
title: "Story Title"
passages:
  - speaker: "Narrator"
    voice_id: "EXAVITQu4vr4xnSDxMaL"
    text: "Once upon a time..."
    pause_after_ms: 500
  - speaker: "Wolf"
    voice_id: "nPczCjzI2devNBz1zQrb"
    text: "Little pig, little pig..."
    pause_after_ms: 300
```

### Step 4: Synthesize Each Passage

```bash
export ELEVENLABS_API_KEY=sk_0d79fb089f759099f234a6768707b2374b36940d372453ed

# For each passage, generate audio segment
python -m tts.cli synthesize "$TEXT" -o /tmp/segment_001.mp3 -v $VOICE
```

### Step 5: Stitch Audio Segments

Use pydub to combine segments with pauses:

```python
from pydub import AudioSegment

combined = AudioSegment.empty()
for segment_file in sorted(segment_files):
    combined += AudioSegment.from_mp3(segment_file)
    combined += AudioSegment.silent(duration=500)  # pause between

combined.export("/tmp/story_audiobook.mp3", format="mp3")
```

### Step 6: Publish to S3

```bash
python3 projects/unspecified/active/tool-s3-publish-cli-vayfd/s3_publish.py \
    /tmp/story_audiobook.mp3 \
    --prefix audiobooks \
    --temp 24 \
    --yes
```

### Step 7: Return Results

Provide:
- Presigned URL to audiobook
- Duration
- Speaker breakdown

## Example

Input: `three-little-pigs.md`
```markdown
# The Three Little Pigs

[Narrator]: Once upon a time, there were three little pigs who left home to seek their fortune.

[Pig 1]: I'll build my house of straw! It's quick and easy.

[Pig 2]: I'll build my house of sticks! A bit stronger.

[Pig 3]: I'll build my house of bricks. It will take longer, but it will be the strongest.

[Narrator]: Soon, a big bad wolf came along.

[Wolf]: Little pig, little pig, let me come in!

[Pig 1]: Not by the hair on my chinny chin chin!

[Wolf]: Then I'll huff, and I'll puff, and I'll blow your house in!
```

Output:
```
Story parsed: "The Three Little Pigs"
Speakers found: Narrator, Pig 1, Pig 2, Pig 3, Wolf
Passages: 9

Synthesizing...
  [1/9] Narrator: "Once upon a time..." (Sarah)
  [2/9] Pig 1: "I'll build my house..." (Charlie)
  ...

Stitching audio segments...
Total duration: 2:34

Published to S3:
https://bucket.s3.amazonaws.com/audiobooks/three-little-pigs.mp3?...
```

## Voice Mapping Rules

Override default mapping with YAML frontmatter:

```yaml
---
voices:
  Narrator: Sarah
  Wolf: Brian
  Pig 1: Charlie
  Pig 2: Adam
  Pig 3: Lily
---
# The Three Little Pigs
...
```
