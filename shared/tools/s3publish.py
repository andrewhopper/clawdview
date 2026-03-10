#!/usr/bin/env python3
# File UUID: 9b9e169e-dec7-48f7-b311-84727a4a7206
"""
S3 Publish Tool - Upload files to S3 with public URLs

Usage:
    python3 s3publish.py <local_file> <s3_key>
    python3 s3publish.py <local_file>  # Uses filename as key

Environment variables required:
    ASSET_DIST_AWS_ACCESS_KEY_ID
    ASSET_DIST_AWS_ACCESS_KEY_SECRET
    ASSET_DIST_AWS_BUCKET
    ASSET_DIST_AWS_REGION (optional, defaults to us-east-1)
"""

import boto3
import os
import sys
import mimetypes
from pathlib import Path


def get_content_type(file_path: str) -> str:
    """Determine content type from file extension."""
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or 'application/octet-stream'


def publish(local_file: str, s3_key: str | None = None) -> str:
    """Upload a file to S3 and return the public URL."""

    # Validate environment
    required_vars = [
        'ASSET_DIST_AWS_ACCESS_KEY_ID',
        'ASSET_DIST_AWS_ACCESS_KEY_SECRET',
        'ASSET_DIST_AWS_BUCKET'
    ]

    missing = [v for v in required_vars if not os.environ.get(v)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    # Validate file exists
    if not os.path.isfile(local_file):
        raise FileNotFoundError(f"File not found: {local_file}")

    # Default s3_key to filename
    if s3_key is None:
        s3_key = Path(local_file).name

    # Create S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['ASSET_DIST_AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['ASSET_DIST_AWS_ACCESS_KEY_SECRET'],
        region_name=os.environ.get('ASSET_DIST_AWS_REGION', 'us-east-1')
    )

    bucket = os.environ['ASSET_DIST_AWS_BUCKET']
    content_type = get_content_type(local_file)

    # Upload file (no ACL - bucket doesn't allow it)
    with open(local_file, 'rb') as f:
        s3.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=f.read(),
            ContentType=content_type
        )

    region = os.environ.get('ASSET_DIST_AWS_REGION', 'us-east-1')
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{s3_key}"

    return url


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    local_file = sys.argv[1]
    s3_key = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        url = publish(local_file, s3_key)
        print(url)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
