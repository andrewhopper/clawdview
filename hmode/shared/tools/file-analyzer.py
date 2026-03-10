#!/usr/bin/env python3
"""
File Analyzer Tool - Analyze files using Anthropic API

Analyzes text files, images, and PDFs using Claude. Images are automatically
downsampled to 1600x1600 max to reduce token usage.

Usage:
    cd shared/tools
    uv run python file_analyzer.py <file_path> [prompt]
    uv run python file_analyzer.py image.png "Describe what you see"
    uv run python file_analyzer.py document.pdf "Summarize this document"
    uv run python file_analyzer.py code.py  # Uses default prompt

Testing:
    cd shared/tools
    uv run pytest tests/ -v

Environment:
    API key sources (checked in order):
    1. ANTHROPIC_API_KEY environment variable
    2. AWS Secrets Manager (secret: anthropic-api-key)

Dependencies managed via pyproject.toml - use `uv run` to auto-install.
"""

import argparse
import base64
import io
import os
import sys
from pathlib import Path
from typing import Tuple

import anthropic
import boto3
from PIL import Image


# Constants
MAX_IMAGE_SIZE = 1600
DEFAULT_MODEL = "claude-sonnet-4-20250514"
SECRET_ID = "anthropic-api-key"
AWS_REGION = "us-east-1"


def get_api_key() -> str:
    """Retrieve Anthropic API key from env var or AWS Secrets Manager."""
    # First try environment variable
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return api_key

    # Fall back to Secrets Manager
    secrets = boto3.client("secretsmanager", region_name=AWS_REGION)
    response = secrets.get_secret_value(SecretId=SECRET_ID)
    return response["SecretString"]


def prepare_image(path: str, max_size: int = MAX_IMAGE_SIZE) -> Tuple[str, str]:
    """
    Load and optionally downsample an image for API submission.

    Returns:
        Tuple of (base64_data, media_type)
    """
    img = Image.open(path)

    # Downsample if larger than max_size
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size), Image.LANCZOS)

    # Choose format based on transparency
    buf = io.BytesIO()
    fmt = "PNG" if img.mode == "RGBA" else "JPEG"
    img.save(buf, format=fmt, quality=85)

    data = base64.standard_b64encode(buf.getvalue()).decode("utf-8")
    media_type = f"image/{fmt.lower()}"

    return data, media_type


def is_image(path: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}
    return Path(path).suffix.lower() in image_extensions


def is_pdf(path: str) -> bool:
    """Check if file is a PDF."""
    return Path(path).suffix.lower() == ".pdf"


def analyze_text_file(client: anthropic.Anthropic, path: str, prompt: str) -> str:
    """Analyze a text file."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    full_prompt = f"{prompt}\n\nFile: {Path(path).name}\n\n```\n{content}\n```"

    response = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": full_prompt}],
    )

    return response.content[0].text


def analyze_image(client: anthropic.Anthropic, path: str, prompt: str) -> str:
    """Analyze an image file with automatic downsampling."""
    data, media_type = prepare_image(path)

    response = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    return response.content[0].text


def analyze_pdf(client: anthropic.Anthropic, path: str, prompt: str) -> str:
    """Analyze a PDF document."""
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")

    response = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    return response.content[0].text


def analyze(file_path: str, prompt: str | None = None) -> str:
    """
    Analyze a file using the Anthropic API.

    Args:
        file_path: Path to the file to analyze
        prompt: Custom prompt (uses sensible defaults if not provided)

    Returns:
        Analysis result as string
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Default prompts based on file type
    if prompt is None:
        if is_image(file_path):
            prompt = "Analyze this image. Describe what you see in detail."
        elif is_pdf(file_path):
            prompt = "Analyze this document. Provide a summary of its contents."
        else:
            prompt = "Analyze this file. Explain what it does and identify any issues."

    # Get API key and create client
    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    # Route to appropriate analyzer
    if is_image(file_path):
        return analyze_image(client, file_path, prompt)
    elif is_pdf(file_path):
        return analyze_pdf(client, file_path, prompt)
    else:
        return analyze_text_file(client, file_path, prompt)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze files using Anthropic API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s screenshot.png "What errors are shown?"
    %(prog)s report.pdf "Summarize the key findings"
    %(prog)s main.py "Review this code for bugs"
    %(prog)s config.yaml
        """,
    )
    parser.add_argument("file", help="File to analyze")
    parser.add_argument(
        "prompt",
        nargs="?",
        default=None,
        help="Analysis prompt (optional, uses smart defaults)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model to use (default: {DEFAULT_MODEL})",
    )

    args = parser.parse_args()

    try:
        result = analyze(args.file, args.prompt)
        print(result)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
