# SAM Volume I, Chapter I

**Original Write histories and an interacting source-field action**

This repository accompanies the seven-page Chapter I final draft of 15 October
2026. It contains the manuscript, derivations, exact retained certificates,
independent reconstruction code, tests, and the evidence required to rerun the
original independent verifier without a SAM installation.

**[Read Chapter I](manuscript/Chapter_I.pdf)** ·
[Editable manuscript](manuscript/chapter_I.md) ·
[Model and derivation](docs/MODEL.md) ·
[Reproduction guide](docs/REPRODUCIBILITY.md) ·
[Evidence provenance](docs/PROVENANCE.md)

Sean Brady is the originator and conceptual director. OpenAI ChatGPT and Codex
are AI research collaborators and co-authors.

## What Chapter I establishes

A source derived from four retained Write components gives six driven spectral
lanes and four unforced states. For the declared coherent hard charge-0/1
preparation with the full soft vacuum in each lane, a weighted continuum
comparison bounds the actual source-field correlator. All six instantaneous
phase rates remain positive and strictly below the bare gap over
`0 <= tau <= 573049*pi`. The complete joint action can use this phase coordinate,
retaining its even source energy, both polarization counterterms, and Berry
one-form.

**The test result suggests strong contact with the concept.**

The time coordinate is capacity-normalized model time. The radius, source
strength chart and preparation travel with the result. Physical source/time
assignments and the original Write/occupied quantum-action interface are
identified explicitly in the chapter and [model documentation](docs/MODEL.md).

## Quick start

Python 3.11 or 3.12 is sufficient for the scientific checks. After cloning:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/reproduce.py
python scripts/verify_native.py --output build/native_verification.json --precision 160
```

The core package needs only `mpmath==1.3.0`. After installation, the scientific
reproduction and evidence checks operate offline and use repository-relative
paths. Run them from the repository root. The native-evidence command checks
retained results; it starts no GEN6 worker.

## Three distinct forms of reproduction

| Route | What runs | Output |
|---|---|---|
| Scalar and source reconstruction | Exact rational certificate consequences and a separate high-precision finite-source reconstruction | `build/reproduction.json`, `build/rates.csv` |
| Original independent verification | Original checker over all bundled native trace inputs/outputs | `build/native_verification.json`; expected 23,804 passing checks, 300 outputs, 134 matrix readouts |
| Manuscript typesetting | Portable renderer, editable text/TeX equations and bundled fonts | `build/Chapter_I.pdf` |

The retained native intervals carry their original certification provenance.
Independent numerical reconstruction checks their consequences; the continuum
form, reference-state and Duhamel arguments are analytical and are presented in
the manuscript and documentation. The [evidence guide](docs/NATIVE_EVIDENCE.md)
explains exactly which original files are bundled. A fresh scientific GEN6 run
uses the separately qualified runtime; this repository supplies the reproducible
paper package and retained-evidence verification.

## Rebuild the PDF

Use Python 3.12 for the pinned typesetting environment:

```bash
python -m pip install -r requirements-pdf.lock
python scripts/build_pdf.py --output build/Chapter_I.pdf
python scripts/verify_pdf.py build/Chapter_I.pdf
```

The Noto fonts and their notices are bundled, so no system font installation or
absolute workspace path is needed. The renderer uses vector equations and
deterministic PDF metadata. `manuscript/Chapter_I.pdf` preserves the original
reviewed draft byte for byte; rebuilding produces a deterministic repository
edition with the same manuscript text. A PDF viewer can inspect the result;
Poppler is optional for page-image review.

## Repository map

| Location | Contents |
|---|---|
| `manuscript/` | Reviewed Chapter I PDF and editable Markdown/TeX |
| `src/sam_chapter1/` | Independent mathematical reference implementation |
| `data/` | Compact exact certificate operands with upstream bindings |
| `evidence/` | Original checker, receipts, trace files, manifests and relocation map |
| `scripts/` | Reproduction, evidence verification, integrity and PDF commands |
| `tests/` | Scientific identities, certificate rejection and evidence-integrity tests |
| `docs/` | Model, proof detail, provenance and reproduction boundaries |
| `references/` | Original action manuscript and centered-clock refinement note |
| `assets/fonts/` | Unmodified Noto fonts and upstream copyright/license notices |

`MANIFEST.json` authenticates the portable manuscript, compact data and assets;
`evidence/MANIFEST.json` authenticates the frozen upstream evidence. Check both:

```bash
python scripts/verify_repository.py
python scripts/verify_native.py --integrity-only
```

[GitHub Actions](https://github.com/iwtbotiwtwot/sam_volume_I_i/actions) runs the
scientific tests/reproduction and original verifier, and builds/checks the PDF.
Generated reports stay in `build/` and CI artifacts. See
[validation](docs/VALIDATION.md) for the recorded initial results and
[contributing](CONTRIBUTING.md) for evidence-preserving changes.

## Attribution

The source lineage is H002628 (original source/capacity/hard clocks), H002630
(weighted propagation and six uniform actual clocks), and H002631 (final draft).
The weighted-form/reference/Duhamel construction is the Codex contribution within
this collaboration. Citation metadata is in [CITATION.cff](CITATION.cff).
Third-party font notices apply to `assets/fonts/`; no additional software or
manuscript license has been selected in this repository.
