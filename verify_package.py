#!/usr/bin/env python3
"""Check the packaged file manifest. This checks integrity, not authorship."""
from pathlib import Path
import hashlib
import re

root = Path(__file__).resolve().parent
seen = set()
for line in (root / 'SHA256SUMS').read_text().splitlines():
    match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
    if not match:
        raise SystemExit('Invalid manifest line')
    expected, relative = match.groups()
    path = (root / relative).resolve(strict=True)
    if relative in seen or not path.is_relative_to(root) or not path.is_file():
        raise SystemExit('Invalid or repeated manifest path: ' + relative)
    seen.add(relative)
    with path.open('rb') as handle:
        if hashlib.file_digest(handle, 'sha256').hexdigest() != expected:
            raise SystemExit('Hash mismatch: ' + relative)
print(f'Verified {len(seen)} listed files. This does not authenticate the author or audit extra files.')
