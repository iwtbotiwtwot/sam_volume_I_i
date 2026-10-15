# Initial repository validation

Validated on 15 October 2026 with a fresh repository-local Python 3.12 virtual
environment and the documented pinned dependencies.

| Check | Observed result |
|---|---|
| `python -m unittest discover -s tests -v` | 46 tests pass: 31 scientific, 9 native-evidence and 6 portable-asset tests |
| `python scripts/reproduce.py` | PASS: 88 exact source bindings, four Sturm-isolated roots and all six conditional scalar clock certificates; separate 150-digit reconstruction |
| `python scripts/verify_native.py --output build/native_verification.json --precision 160` | Original checker PASS: 23,804 checks, 300 trace outputs, 134 matrix readouts, zero failed or unsupported checks |
| `python scripts/verify_native.py --integrity-only` | 615 unchanged artifacts, 18,677,823 bytes |
| `python scripts/verify_repository.py` | 27 portable asset bindings pass |
| `python scripts/verify_pdf.py build/Chapter_I.pdf` | Seven pages; extracted text matches the reviewed original |
| Two PDF builds followed by `cmp` | Byte-identical deterministic builds |
| Seven rendered rebuilt/original page comparisons | All seven pixel-identical to the previously visually reviewed draft |
| `python -m pip check` | No broken requirements |

The independent evidence wrapper also passed from a relocated temporary checkout
under isolated Python with the working directory outside the repository. All
600 trace input/output paths and the exact source-input path resolved inside
that checkout. Unregistered host paths, path traversal, symlink escapes,
missing evidence and altered bytes are rejected.

An independent code review identified a coupling-enclosure check that accepted
overlap where full containment was required. It was corrected before the initial
publication, and a regression test rejects an inward coupling enclosure. The
final interval arithmetic, source signs and centered-rate consequences passed
the review.

The reviewed original PDF has SHA-256
`c9a3c916dd85de3951d04564554e1d1aaf966da7be0b9d5fac2715f714127bb5`.
The deterministic repository rebuild has SHA-256
`f6654243328025174245a1e23ccb931463f33f1a123f065164add669e2b7eff6`.
Their metadata differs; their rendered pages and extracted manuscript text agree.

These are observed local validation results. GitHub Actions performs the same
checks from a clean checkout on Python 3.11/3.12, with the PDF job on 3.12.
Its current outcome is available in the repository's Actions tab.

The 46 repository tests and 23,804 independent evidence checks are distinct from
the original 1,122 native checks. The analytical continuum/domain/reference/
Duhamel hypotheses retain their derivations and source provenance. No new native
scientific campaign was launched to populate this repository.
