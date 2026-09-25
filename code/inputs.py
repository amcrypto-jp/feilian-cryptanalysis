"""Identify the original review target before reading or compiling its files."""
from pathlib import Path
import hashlib
import json

PACKAGE = Path(__file__).resolve().parents[1]


def verify_submission(root):
    root = Path(root).expanduser().resolve(strict=True)
    manifest = json.loads((PACKAGE / 'data/input_manifest.json').read_text())
    for relative, expected in manifest.items():
        path = (root / relative).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f'Not a submission file: {relative}')
        if path.stat().st_size != expected['bytes']:
            raise ValueError(f'Size mismatch: {relative}')
        with path.open('rb') as handle:
            actual = hashlib.file_digest(handle, 'sha256').hexdigest()
        if actual != expected['sha256']:
            raise ValueError(f'SHA-256 mismatch: {relative}')
    return root, len(manifest)
