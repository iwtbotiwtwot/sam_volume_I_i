#!/usr/bin/env python3
"""Check the rebuilt chapter's structure and text against the reviewed draft.

This complements page-image review. It does not claim pixel comparison or
mathematical verification from text extraction; display equations are vectors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def words(reader: PdfReader) -> list[str]:
    return ' '.join(page.extract_text() for page in reader.pages).split()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--reference', type=Path, default=ROOT/'manuscript/Chapter_I.pdf')
    args = parser.parse_args()
    try:
        candidate = PdfReader(args.pdf)
        reference = PdfReader(args.reference)
        assert not candidate.is_encrypted, 'PDF is encrypted'
        assert len(candidate.pages) == 7, 'Chapter I must have seven pages'
        assert all(tuple(map(float, p.mediabox)) == (0, 0, 612, 792)
                   for p in candidate.pages), 'Unexpected page dimensions'
        assert words(candidate) == words(reference), 'Rebuilt manuscript text differs from reviewed draft'
        assert all('\ufffd' not in p.extract_text() for p in candidate.pages), 'Missing text glyph'
        digest = hashlib.sha256(args.pdf.read_bytes()).hexdigest()
        print(json.dumps({'status': 'PASS', 'pages': 7, 'sha256': digest,
                          'text_matches_reviewed_draft': True,
                          'scope': 'Structure and extracted text; vector equations also require visual review'}, indent=2))
        return 0
    except (OSError, AssertionError, ValueError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
