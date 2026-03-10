#!/usr/bin/env python3
"""
Generate audio narrations for future vignettes using ElevenLabs TTS.
"""

import asyncio
import os
import sys
from pathlib import Path

import httpx


# Voice for narration - warm, engaging narrator
NARRATOR_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam - American male, deep, narrator
MODEL_ID = "eleven_multilingual_v2"


def clean_text_for_tts(markdown_text: str) -> str:
    """
    Clean markdown text for TTS synthesis.
    """
    lines = []
    for line in markdown_text.split("\n"):
        # Skip headers
        if line.startswith("#"):
            continue
        # Skip horizontal rules
        if line.strip().startswith("---"):
            continue
        # Skip metadata lines like **2030 · ...**
        if line.startswith("**") and "·" in line:
            setting = line.strip("*").strip()
            lines.append(setting.replace("·", ",") + ".")
            continue
        # Handle closing principle in italics
        if line.startswith("*") and not line.startswith("**"):
            clean = line.strip("*").strip()
            if clean:
                lines.append(clean)
            continue
        # Remove bold markers
        line = line.replace("**", "")
        line = line.replace("*", "")

        if line.strip():
            lines.append(line.strip())

    return "\n\n".join(lines)


async def generate_audio(
    client: httpx.AsyncClient,
    text: str,
    output_path: Path,
) -> Path:
    """Generate audio for text using ElevenLabs API."""

    payload = {
        "text": text,
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
        json=payload,
        params={"output_format": "mp3_44100_128"},
    )
    response.raise_for_status()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)

    return output_path


async def main():
    """Generate audio for all vignettes."""

    # Check for API key
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ ELEVENLABS_API_KEY environment variable not set")
        sys.exit(1)

    # Paths
    examples_dir = Path(__file__).parent
    output_dir = examples_dir / "audio"
    output_dir.mkdir(exist_ok=True)

    # Find all vignette markdown files
    vignettes = sorted(examples_dir.glob("*.md"))
    if not vignettes:
        print("❌ No vignette files found")
        sys.exit(1)

    print("=" * 60)
    print("Future Vignettes - Audio Generation")
    print("=" * 60)
    print(f"Voice: Adam (deep narrator)")
    print(f"Found {len(vignettes)} vignettes")
    print()

    # Create HTTP client with API key
    async with httpx.AsyncClient(
        base_url="https://api.elevenlabs.io/v1",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        },
        timeout=60.0,
    ) as client:

        audio_files = []

        for i, vignette_path in enumerate(vignettes, 1):
            print(f"🎙️  [{i}/{len(vignettes)}] {vignette_path.name}...")

            try:
                # Read and clean text
                raw_text = vignette_path.read_text()
                clean_text = clean_text_for_tts(raw_text)

                # Output path
                output_path = output_dir / f"{vignette_path.stem}.mp3"

                await generate_audio(client, clean_text, output_path)
                audio_files.append(output_path)
                print(f"   ✅ Generated: {output_path.name}")

                # Rate limiting
                await asyncio.sleep(1.0)

            except Exception as e:
                print(f"   ❌ Error: {e}")
                raise

    print()
    print("=" * 60)
    print("✅ Audio generation complete!")
    print("=" * 60)
    print(f"\nGenerated {len(audio_files)} audio files:")
    for f in audio_files:
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.1f} KB)")

    print(f"\n📁 Output directory: {output_dir}")

    return audio_files


if __name__ == "__main__":
    asyncio.run(main())
