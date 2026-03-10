---
name: tts
description: Convert text to audio using AWS Polly and publish to S3 with presigned URL
version: 2.0.0
---

# Text-to-Speech Skill

**Convert text or text files to audio using AWS Polly, publish to S3, return presigned URL**

## Execution Flow

1. **Parse input** → text string or file path
2. **Read content** → if file path, read file content
3. **Synthesize audio** → call AWS Polly with boto3
4. **Publish to S3** → upload MP3, get presigned URL (24h)
5. **Return URL** → display clickable link to user

## Usage

Invoke with `/tts` slash command or trigger this skill directly.

```
/tts Once upon a time, there were three little pigs.
/tts path/to/story.txt
/tts "Hello world" with voice Matthew
```

## Implementation

### Step 1: Determine Input Type

```python
from pathlib import Path

input_path = Path(input_text)
if input_path.exists() and input_path.is_file():
    text = input_path.read_text()
else:
    text = input_text
```

### Step 2: Synthesize Audio

```python
import boto3
from pathlib import Path
from datetime import datetime

# Create Polly client
polly = boto3.client('polly', region_name='us-east-1')

# Synthesize speech
response = polly.synthesize_speech(
    Text=text,
    VoiceId='Joanna',  # or user-specified voice
    OutputFormat='mp3',
    Engine='neural'
)

# Save audio
audio_data = response['AudioStream'].read()
timestamp = int(datetime.now().timestamp())
output_path = Path(f'/tmp/tts_{timestamp}.mp3')
output_path.write_bytes(audio_data)
```

### Step 3: Publish to S3

```bash
python3 hmode/shared/tools/s3publish.py \
    "$OUTPUT" \
    --prefix tts-audio \
    --temp 24 \
    --yes
```

### Step 4: Return URL

Extract and display the presigned URL from the publish output.

## Voice Options (AWS Polly Neural)

| Voice | Description | Use Case |
|-------|-------------|----------|
| Joanna | American female, professional | Narrator (default) |
| Matthew | American male, authoritative | Male narrator |
| Amy | British female, friendly | Female character |
| Brian | British male, warm | Male narrator |
| Emma | British female, soft | Female character |
| Ivy | American female, child-like | Young girl |
| Kevin | American male, child-like | Young boy |
| Joey | American male, casual | Male character |
| Justin | American male, young | Young male |
| Olivia | Australian female | Female narrator |

## Dependencies

- `boto3` - AWS SDK for Python
- `hmode/shared/tools/s3publish.py` - S3 publish tool
- AWS credentials configured (profile, IAM role, or env vars)

## Error Handling

| Error | Action |
|-------|--------|
| No AWS credentials | Prompt user to configure AWS credentials |
| File not found | Treat input as raw text |
| Synthesis failed | Show error, suggest checking voice name |
| S3 upload failed | Show error, provide local file path |

## Example Output

```
Synthesizing with voice: Joanna...
Saved to: /tmp/tts_1700123456.mp3

Uploading to S3...
Presigned URL (24h): https://bucket.s3.amazonaws.com/tts-audio/tts_1700123456.mp3?...
```
