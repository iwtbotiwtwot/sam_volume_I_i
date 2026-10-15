#!/usr/bin/env python3
"""Verify the portable chapter/source assets against repository-relative hashes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def verify_assets(root: Path = ROOT, manifest_path: Path | None = None) -> dict:
    root = root.resolve()
    manifest_path = manifest_path or root / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('schema') != 'SAM_CHAPTER_I_PORTABLE_ASSETS_V1':
        raise ValueError('Unknown asset manifest schema')
    entries = manifest.get('files', [])
    if not entries:
        raise ValueError('Empty asset manifest')
    seen = set()
    total = 0
    for entry in entries:
        name = entry['path']
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name:
            raise ValueError(f'Unsafe asset path: {name}')
        if name in seen:
            raise ValueError(f'Duplicate asset path: {name}')
        seen.add(name)
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f'Missing or escaped asset: {name}')
        data = path.read_bytes()
        if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError(f'Asset content mismatch: {name}')
        total += len(data)
    return {'status': 'PASS', 'files': len(entries), 'bytes': total,
            'scope': manifest.get('scope', 'Portable assets')}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    try:
        result = verify_assets(manifest_path=args.manifest)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
