# Text-to-Speech Command

Convert text to audio using AWS Polly and publish to S3 with a presigned URL.

## Arguments
- $ARGUMENTS: Text to convert OR path to text file

## Instructions

1. Determine if the argument is a file path or raw text:
   - If it's a path that exists, read the file content
   - Otherwise, treat it as raw text

2. Generate audio using AWS Polly via boto3:
   ```python
   import boto3
   from pathlib import Path

   polly = boto3.client('polly', region_name='us-east-1')

   response = polly.synthesize_speech(
       Text=text,
       VoiceId='Joanna',  # or other voice
       OutputFormat='mp3',
       Engine='neural'
   )

   audio_data = response['AudioStream'].read()
   output_path = Path('/tmp/tts_output.mp3')
   output_path.write_bytes(audio_data)
   ```

3. Publish to S3 with a presigned URL (24 hours):
   ```bash
   python3 hmode/shared/tools/s3publish.py /tmp/tts_output.mp3 --prefix tts-audio --temp 24 --yes
   ```

4. Return the presigned URL to the user

## Voice Options (AWS Polly Neural)
- Joanna (default): American female, news anchor, professional
- Matthew: American male, news anchor, authoritative
- Amy: British female, friendly, conversational
- Brian: British male, narrator, warm
- Emma: British female, soft, pleasant
- Olivia: Australian female, friendly
- Ivy: American female, young, child-like
- Kevin: American male, young boy, child-like
- Joey: American male, casual
- Justin: American male, young, friendly

Use different VoiceId to change the voice.

## Example Usage
```
/tts Once upon a time, there were three little pigs.
/tts story.txt
/tts "Hello world" with voice Matthew
```
