#!/usr/bin/env python3
"""
S3 Incremental Backup with Merkle Tree Change Detection.

Uses content hashing (Merkle tree) to detect actual changes, not just mtime.
Stores a manifest of hashes and only uploads files that have truly changed.

Usage:
    python s3backup.py                      # Detect changes since last backup
    python s3backup.py --days 7             # Also filter by mtime (faster scan)
    python s3backup.py --dry-run            # Preview only
    python s3backup.py --full               # Force full backup (ignore manifest)
    python s3backup.py --path ./projects    # Backup specific directory
    python s3backup.py --config config.yaml # Use custom config file

Configuration:
    Default config: shared/tools/s3backup-config.yaml

Environment Variables (fallback):
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
    ASSET_DIST_AWS_ACCESS_KEY_ID, ASSET_DIST_AWS_ACCESS_KEY_SECRET
    S3_BACKUP_BUCKET, AWS_REGION
"""

import argparse
import fnmatch
import hashlib
import json
import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('s3backup')

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Config file location (relative to script)
SCRIPT_DIR = Path(__file__).parent
DEFAULT_CONFIG_FILE = SCRIPT_DIR / 's3backup-config.yaml'
MANIFEST_FILE = '.s3backup-manifest.json'

# Default exclusions (can be overridden by config)
DEFAULT_EXCLUDE_PATTERNS = {
    '.git',
    '__pycache__',
    'node_modules',
    '.venv',
    'venv',
    '.mypy_cache',
    '.pytest_cache',
    '.ruff_cache',
    '.DS_Store',
    'Thumbs.db',
    '.sessions',
    'logs/',
    '.s3backup-manifest.json',
    '.env',
    '.env.local',
    'credentials',
    '*.secret',
}

DEFAULT_EXCLUDE_EXTENSIONS = {
    '.exe', '.dll', '.so', '.dylib',
    '.zip', '.tar', '.gz', '.bz2', '.7z',
    '.mp4', '.mov', '.avi', '.mkv',
    '.mp3', '.wav', '.flac',
    '.iso', '.dmg', '.pyc', '.pyo',
}


def load_config(config_path: Optional[Path] = None) -> dict:
    """Load configuration from YAML file."""
    if not HAS_YAML:
        return {}

    path = config_path or DEFAULT_CONFIG_FILE
    if not path.exists():
        return {}

    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.warning(f"Could not load config from {path}: {e}")
        return {}


# Global config (loaded at startup)
CONFIG: dict = {}


@dataclass
class FileNode:
    """Represents a file in the Merkle tree."""
    path: str
    hash: str
    size: int
    mtime: float


@dataclass
class DirNode:
    """Represents a directory in the Merkle tree."""
    path: str
    hash: str
    children: dict = field(default_factory=dict)


def get_exclude_patterns() -> set:
    """Get exclusion patterns from config or defaults."""
    if CONFIG.get('exclude_patterns'):
        return set(CONFIG['exclude_patterns'])
    return DEFAULT_EXCLUDE_PATTERNS


def get_exclude_extensions() -> set:
    """Get exclusion extensions from config or defaults."""
    if CONFIG.get('exclude_extensions'):
        return set(CONFIG['exclude_extensions'])
    return DEFAULT_EXCLUDE_EXTENSIONS


def get_include_patterns() -> list:
    """Get include patterns from config (empty = include all)."""
    return CONFIG.get('include_patterns', [])


def matches_include_pattern(path_str: str, patterns: list) -> bool:
    """
    Check if path matches any include pattern.

    Supports:
    - Glob patterns: *.py, **/*.md, src/**
    - Regex patterns: prefix with 'regex:' e.g. 'regex:.*\\.ya?ml$'

    Returns True if patterns list is empty (include all).
    """
    if not patterns:
        return True  # Empty = include all

    for pattern in patterns:
        if pattern.startswith('regex:'):
            # Regex pattern
            regex = pattern[6:]  # Remove 'regex:' prefix
            try:
                if re.search(regex, path_str):
                    return True
            except re.error:
                logger.warning(f"Invalid regex pattern: {regex}")
        else:
            # Glob pattern - use fnmatch
            # Handle ** for recursive matching
            if '**' in pattern:
                # Convert ** glob to regex for proper matching
                regex_pattern = pattern.replace('.', r'\.').replace('**/', '.*').replace('**', '.*').replace('*', '[^/]*').replace('?', '.')
                try:
                    if re.match(regex_pattern, path_str):
                        return True
                except re.error:
                    pass
            elif fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(Path(path_str).name, pattern):
                return True

    return False


class MerkleTree:
    """
    Merkle tree for file system change detection.

    Directory hash = hash(sorted child hashes)
    File hash = hash(file content)

    If a directory hash differs, something underneath changed.
    """

    def __init__(self, root_path: Path, max_size_mb: float = 50):
        self.root_path = root_path
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.files: dict[str, FileNode] = {}
        self.dirs: dict[str, DirNode] = {}
        self.root_hash: Optional[str] = None
        self.exclude_patterns = get_exclude_patterns()
        self.exclude_extensions = get_exclude_extensions()
        self.include_patterns = get_include_patterns()

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        path_str = str(path)
        for pattern in self.exclude_patterns:
            if pattern in path_str:
                return True
        if path.suffix.lower() in self.exclude_extensions:
            return True
        return False

    def should_include(self, rel_path: str) -> bool:
        """Check if path matches include patterns (if any)."""
        return matches_include_pattern(rel_path, self.include_patterns)

    def hash_file(self, path: Path) -> Optional[str]:
        """Compute SHA-256 hash of file content."""
        try:
            if path.stat().st_size > self.max_size_bytes:
                return None

            sha256 = hashlib.sha256()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()[:16]  # Truncate for efficiency
        except (OSError, PermissionError):
            return None

    def build(self, mtime_filter_days: Optional[int] = None) -> str:
        """
        Build Merkle tree from filesystem.

        Returns root hash.
        """
        cutoff_ts = None
        if mtime_filter_days:
            cutoff = datetime.now() - timedelta(days=mtime_filter_days)
            cutoff_ts = cutoff.timestamp()

        # Collect all files
        for path in self.root_path.rglob('*'):
            if not path.is_file():
                continue
            if self.should_exclude(path):
                continue

            try:
                stat = path.stat()

                # Optional mtime filter for faster scanning
                if cutoff_ts and stat.st_mtime < cutoff_ts:
                    continue

                rel_path = str(path.relative_to(self.root_path))

                # Check include patterns (if configured)
                if not self.should_include(rel_path):
                    continue

                file_hash = self.hash_file(path)
                if file_hash:
                    self.files[rel_path] = FileNode(
                        path=rel_path,
                        hash=file_hash,
                        size=stat.st_size,
                        mtime=stat.st_mtime
                    )
            except (OSError, PermissionError):
                continue

        # Build directory hashes bottom-up
        self._build_dir_hashes()

        return self.root_hash or ''

    def _build_dir_hashes(self):
        """Build directory hashes from file hashes."""
        # Group files by directory
        dir_files: dict[str, list[str]] = {}
        for rel_path in self.files:
            dir_path = str(Path(rel_path).parent)
            if dir_path == '.':
                dir_path = ''
            if dir_path not in dir_files:
                dir_files[dir_path] = []
            dir_files[dir_path].append(rel_path)

        # Compute hash for each directory
        for dir_path, file_paths in sorted(dir_files.items(), key=lambda x: -x[0].count('/')):
            child_hashes = []
            for fp in sorted(file_paths):
                child_hashes.append(self.files[fp].hash)

            # Include subdirectory hashes
            for subdir, node in self.dirs.items():
                if subdir.startswith(dir_path + '/') if dir_path else '/' not in subdir:
                    # Direct child
                    parent = str(Path(subdir).parent)
                    if parent == '.' :
                        parent = ''
                    if parent == dir_path:
                        child_hashes.append(node.hash)

            dir_hash = hashlib.sha256(''.join(sorted(child_hashes)).encode()).hexdigest()[:16]
            self.dirs[dir_path] = DirNode(path=dir_path, hash=dir_hash)

        # Root hash
        if self.dirs:
            root_children = [n.hash for p, n in self.dirs.items() if '/' not in p and p != '']
            root_children.extend(self.files[f].hash for f in self.files if '/' not in f)
            self.root_hash = hashlib.sha256(''.join(sorted(root_children)).encode()).hexdigest()[:16]
        elif self.files:
            self.root_hash = hashlib.sha256(''.join(sorted(f.hash for f in self.files.values())).encode()).hexdigest()[:16]

    def to_manifest(self) -> dict:
        """Export tree as manifest dict."""
        return {
            'root_hash': self.root_hash,
            'timestamp': datetime.now().isoformat(),
            'patterns': {
                'include': list(self.include_patterns),
                'exclude': list(self.exclude_patterns),
                'exclude_extensions': list(self.exclude_extensions),
            },
            'files': {
                path: {
                    'hash': node.hash,
                    'size': node.size,
                    'mtime': node.mtime
                }
                for path, node in self.files.items()
            }
        }

    def patterns_match(self, manifest: dict) -> bool:
        """Check if current patterns match manifest patterns."""
        manifest_patterns = manifest.get('patterns', {})
        if not manifest_patterns:
            return True  # Old manifest without patterns - assume match

        return (
            set(manifest_patterns.get('include', [])) == set(self.include_patterns) and
            set(manifest_patterns.get('exclude', [])) == set(self.exclude_patterns) and
            set(manifest_patterns.get('exclude_extensions', [])) == set(self.exclude_extensions)
        )

    @classmethod
    def from_manifest(cls, manifest: dict, root_path: Path) -> 'MerkleTree':
        """Load tree from manifest."""
        tree = cls(root_path)
        tree.root_hash = manifest.get('root_hash')
        for path, data in manifest.get('files', {}).items():
            tree.files[path] = FileNode(
                path=path,
                hash=data['hash'],
                size=data['size'],
                mtime=data['mtime']
            )
        return tree

    def diff(self, other: 'MerkleTree') -> tuple[list[str], list[str], list[str]]:
        """
        Compare with another tree.

        Returns: (added, modified, deleted)
        """
        added = []
        modified = []
        deleted = []

        current_paths = set(self.files.keys())
        other_paths = set(other.files.keys())

        # Added files
        for path in current_paths - other_paths:
            added.append(path)

        # Deleted files
        for path in other_paths - current_paths:
            deleted.append(path)

        # Modified files (hash changed)
        for path in current_paths & other_paths:
            if self.files[path].hash != other.files[path].hash:
                modified.append(path)

        return added, modified, deleted


def get_region() -> str:
    """Get AWS region from config or environment."""
    # Config takes precedence, then env vars
    if CONFIG.get('aws', {}).get('region'):
        return CONFIG['aws']['region']
    return os.environ.get('AWS_REGION') or os.environ.get('ASSET_DIST_AWS_REGION', 'us-east-1')


def get_s3_client(bucket_override: Optional[str] = None):
    """
    Create S3 client. Tries credentials in order:
    1. Standard AWS_* env vars (with optional AWS_SESSION_TOKEN)
    2. ASSET_DIST_AWS_* env vars (Claude Code Web)
    3. Default boto3 credential chain (profiles, IAM roles, etc.)
    """
    region = get_region()

    # Try standard AWS credentials first
    if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
        session_token = os.environ.get('AWS_SESSION_TOKEN')
        return boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            aws_session_token=session_token,
            region_name=region
        )

    # Try ASSET_DIST credentials (Claude Code Web)
    if os.environ.get('ASSET_DIST_AWS_ACCESS_KEY_ID') and os.environ.get('ASSET_DIST_AWS_ACCESS_KEY_SECRET'):
        return boto3.client(
            's3',
            aws_access_key_id=os.environ['ASSET_DIST_AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['ASSET_DIST_AWS_ACCESS_KEY_SECRET'],
            region_name=region
        )

    # Fall back to default credential chain
    return boto3.client('s3', region_name=region)


def get_bucket(bucket_override: Optional[str] = None) -> str:
    """Get bucket name from argument, config, or environment."""
    if bucket_override:
        return bucket_override
    # Try config first
    if CONFIG.get('backup', {}).get('bucket'):
        return CONFIG['backup']['bucket']
    # Then environment variables
    bucket = os.environ.get('S3_BACKUP_BUCKET') or os.environ.get('ASSET_DIST_AWS_BUCKET')
    if not bucket:
        logger.error("No bucket specified. Use --bucket, config file, or set S3_BACKUP_BUCKET env var")
        sys.exit(1)
    return bucket


def get_default_prefix() -> str:
    """Get default S3 prefix from config."""
    return CONFIG.get('backup', {}).get('prefix', 'backups/protoflow')


def get_max_size_mb() -> float:
    """Get max file size from config."""
    return CONFIG.get('backup', {}).get('max_size_mb', 50)


def get_content_type(path: Path) -> str:
    """Get content type based on file extension."""
    ext_map = {
        '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript',
        '.json': 'application/json', '.md': 'text/markdown', '.txt': 'text/plain',
        '.py': 'text/x-python', '.yaml': 'text/yaml', '.yml': 'text/yaml',
        '.xml': 'application/xml', '.svg': 'image/svg+xml', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif',
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }
    return ext_map.get(path.suffix.lower(), 'application/octet-stream')


def upload_file(s3_client, bucket: str, local_path: Path, s3_key: str) -> bool:
    """Upload a single file to S3 with multipart support."""
    try:
        content_type = get_content_type(local_path)
        file_size = local_path.stat().st_size
        
        # Use multipart upload for files > 100MB
        if file_size > 100 * 1024 * 1024:
            return upload_multipart(s3_client, bucket, local_path, s3_key, content_type)
        
        # Stream upload for smaller files
        with open(local_path, 'rb') as f:
            s3_client.upload_fileobj(
                f,
                bucket,
                s3_key,
                ExtraArgs={'ContentType': content_type}
            )
        return True
    except (ClientError, OSError) as e:
        logger.error(f"Upload failed: {e}")
        return False


def upload_multipart(s3_client, bucket: str, local_path: Path, s3_key: str, content_type: str) -> bool:
    """Upload large file using multipart upload."""
    try:
        s3_client.upload_file(
            str(local_path),
            bucket,
            s3_key,
            ExtraArgs={'ContentType': content_type},
            Config=boto3.s3.transfer.TransferConfig(
                multipart_threshold=1024 * 25,  # 25MB
                max_concurrency=10,
                multipart_chunksize=1024 * 25,
                use_threads=True
            )
        )
        return True
    except (ClientError, OSError) as e:
        logger.error(f"Multipart upload failed: {e}")
        return False


def load_manifest(path: Path) -> Optional[dict]:
    """Load existing manifest."""
    manifest_path = path / MANIFEST_FILE
    if manifest_path.exists():
        try:
            with open(manifest_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return None


def save_manifest(path: Path, manifest: dict):
    """Save manifest to disk."""
    manifest_path = path / MANIFEST_FILE
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)


def get_log_path() -> Optional[Path]:
    """Get log file path from config."""
    logging_config = CONFIG.get('logging', {})
    log_dir = logging_config.get('log_dir', '/tmp')
    log_file = logging_config.get('log_file', 's3backup.log')
    if log_dir and log_file:
        return Path(log_dir) / log_file
    return None


def main():
    global CONFIG

    parser = argparse.ArgumentParser(description='S3 backup with Merkle tree change detection')
    parser.add_argument('--config', '-c', type=str, help='Config file path (default: s3backup-config.yaml)')
    parser.add_argument('--days', '-d', type=int, help='Only backup files modified in last N days')
    parser.add_argument('--path', '-p', type=str, default='.', help='Root path to backup')
    parser.add_argument('--bucket', '-b', type=str, help='S3 bucket name')
    parser.add_argument('--prefix', '-P', type=str, help='S3 key prefix')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Preview only')
    parser.add_argument('--full', '-f', action='store_true', help='Force full backup')
    parser.add_argument('--max-size', type=float, help='Max file size in MB')
    parser.add_argument('--show-tree', action='store_true', help='Show directory tree with change status')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose/debug logging')
    parser.add_argument('--log-file', type=str, help='Write logs to file (overrides config)')
    parser.add_argument('--log-dir', type=str, help='Log directory (overrides config)')

    args = parser.parse_args()

    # Load config first (needed for log path)
    config_path = Path(args.config) if args.config else None
    CONFIG = load_config(config_path)

    # Configure logging - CLI args override config
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Determine log file path: CLI > config > None
    log_file_path = None
    if args.log_file:
        log_file_path = Path(args.log_file)
    elif args.log_dir:
        log_file = CONFIG.get('logging', {}).get('log_file', 's3backup.log')
        log_file_path = Path(args.log_dir) / log_file
    else:
        log_file_path = get_log_path()

    if log_file_path:
        # Ensure log directory exists
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

    # Apply defaults from config
    prefix = args.prefix or get_default_prefix()
    max_size = args.max_size or get_max_size_mb()

    root_path = Path(args.path).resolve()

    if not root_path.exists():
        logger.error(f"Path does not exist: {root_path}")
        sys.exit(1)

    logger.info("S3 Merkle Tree Backup")
    if CONFIG:
        logger.info(f"Config:    {config_path or DEFAULT_CONFIG_FILE}")
    logger.info(f"Source:    {root_path}")
    logger.info(f"S3 Prefix: {prefix}")
    logger.info(f"Region:    {get_region()}")
    if args.days:
        logger.info(f"Filter:    Files modified in last {args.days} day(s)")

    # Build current tree
    logger.info("Building Merkle tree (hashing files)...")
    start = time.time()
    current_tree = MerkleTree(root_path, max_size)
    current_tree.build(args.days)
    logger.info(f"Found {len(current_tree.files)} files in {time.time() - start:.1f}s")
    logger.info(f"Root hash: {current_tree.root_hash}")

    # Load previous manifest
    previous_manifest = None if args.full else load_manifest(root_path)

    # Check if patterns have changed since last backup
    if previous_manifest and not current_tree.patterns_match(previous_manifest):
        logger.warning("Include/exclude patterns have changed since last backup")
        logger.warning("Forcing full backup to ensure consistency")
        previous_manifest = None  # Force full backup

    if previous_manifest and not args.days:
        # Use manifest for incremental backup (content-based)
        logger.info(f"Previous backup: {previous_manifest.get('timestamp', 'unknown')}")
        previous_tree = MerkleTree.from_manifest(previous_manifest, root_path)

        if previous_tree.root_hash == current_tree.root_hash:
            logger.info("No changes detected (root hash unchanged)")
            return

        added, modified, deleted = current_tree.diff(previous_tree)
        logger.info(f"Changes: +{len(added)} added, ~{len(modified)} modified, -{len(deleted)} deleted")

        files_to_upload = added + modified
    elif args.days:
        # Time-based filter - upload all files matching mtime
        logger.info(f"Uploading all files modified in last {args.days} day(s)")
        files_to_upload = list(current_tree.files.keys())
    else:
        logger.info("No previous manifest - full backup")
        files_to_upload = list(current_tree.files.keys())

    if not files_to_upload:
        logger.info("Nothing to upload.")
        return

    # Calculate size
    total_size = sum(current_tree.files[f].size for f in files_to_upload if f in current_tree.files)
    logger.info(f"Files to upload: {len(files_to_upload)} ({total_size / 1024 / 1024:.2f}MB)")

    if args.show_tree or args.dry_run:
        logger.info("Changed files:")
        for f in sorted(files_to_upload)[:50]:  # Limit display
            node = current_tree.files.get(f)
            if node:
                size_kb = node.size / 1024
                logger.debug(f"  {f} ({size_kb:.1f}KB)")
        if len(files_to_upload) > 50:
            logger.info(f"  ... and {len(files_to_upload) - 50} more")

    if args.dry_run:
        logger.info("DRY RUN - no files uploaded")
        return

    # Upload
    s3_client = get_s3_client()
    bucket = get_bucket(args.bucket)

    logger.info(f"Uploading to s3://{bucket}/{prefix}/")

    success = 0
    failed = 0
    start = time.time()
    
    # Get max workers from config
    max_workers = CONFIG.get('backup', {}).get('max_workers', 4)
    
    # Parallel upload with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all upload tasks
        future_to_path = {}
        for i, rel_path in enumerate(files_to_upload, 1):
            local_path = root_path / rel_path
            s3_key = f"{prefix}/{rel_path}"
            future = executor.submit(upload_file, s3_client, bucket, local_path, s3_key)
            future_to_path[future] = (rel_path, i)
        
        # Process completed uploads
        for future in as_completed(future_to_path):
            rel_path, i = future_to_path[future]
            try:
                if future.result():
                    success += 1
                    logger.info(f"[{i}/{len(files_to_upload)}] ✓ {rel_path}")
                else:
                    failed += 1
                    logger.error(f"[{i}/{len(files_to_upload)}] ✗ {rel_path}")
            except Exception as e:
                failed += 1
                logger.error(f"[{i}/{len(files_to_upload)}] ✗ {rel_path}: {e}")

    elapsed = time.time() - start
    logger.info(f"Complete in {elapsed:.1f}s - Uploaded: {success}, Failed: {failed}")

    # Save manifest
    if success > 0 and failed == 0:
        save_manifest(root_path, current_tree.to_manifest())
        logger.info(f"Manifest saved: {MANIFEST_FILE}")

    region = get_region()
    logger.info(f"Browse: https://{bucket}.s3.{region}.amazonaws.com/{prefix}/")


if __name__ == '__main__':
    main()
