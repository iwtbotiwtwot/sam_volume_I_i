# Reproducing Chapter I

The repository contains the Chapter I manuscript, executable finite-source and
clock-bound calculations, and retained GEN6 Duck evidence. Its offline checks
cover placement generation, compact independent reconstruction, the
second-order diagnostic, and replay of the original independent checker against
preserved native outputs.

## Install and run

From the repository root, use Python 3.11 or later. Python 3.12 is the
recommended environment, and is the version used for the pinned PDF build:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/reproduce.py --precision 150 --output build
python scripts/generate_source.py
python scripts/second_order.py
python scripts/verify_native.py --output build/native_verification.json --precision 160
```

The scientific calculation requires `mpmath` 1.3.0. The test runner is Python's
standard-library `unittest`. The repository configuration records the exact
dependency requirements. The commands run locally and read repository-relative
inputs; they do not contact the original research checkout or start a GEN6
Duck job.

| Command | Main output | Purpose |
|---|---|---|
| `python -m unittest discover -s tests -v` | Terminal test report | Exercise exact source identities, preparation/calibration distinctions, bound calculations, and deliberate failure cases |
| `python scripts/reproduce.py --precision 150 --output build` | `build/reproduction.json`, `build/rates.csv` | Reconstruct source and scalar quantities independently; replay conservative rational interval bounds |
| `python scripts/generate_source.py` | `build/source_generation.json` | Generate B, T and K from placement codes, the original source action table and selected signed connector ledger |
| `python scripts/second_order.py` | `build/second_order.json` | Check the second-order hard-gap coefficient in all six lanes and fourth-order residual scaling in a separate finite-mode model |
| `python scripts/verify_native.py --output build/native_verification.json --precision 160` | `build/native_verification.json` | Resolve retained paths, verify evidence hashes, and replay the original independent checker over native outputs |

Run commands from the repository root. The `build/` directory contains generated
outputs and is excluded from version control. Any failed check exits with a
nonzero status; a successful command prints its summary and output location.

## What each route reconstructs

### Compact source and bound reconstruction

The implementation in [`src/sam_chapter1`](../src/sam_chapter1) consumes the
compact exact packet [`data/chapter1_certificate.json`](../data/chapter1_certificate.json).
That packet identifies its retained native sources by SHA-256 and JSON location.
It generates the source matrices from the [original placement operands](PLACEMENTS.md)
and receives the rational source brackets, radius and hard-branch input
enclosures used by the Chapter I calculation.

The reconstruction has separate arithmetic roles:

1. Exact integer and rational arithmetic generates the 4 by 78 signed boundary
   matrix B, contracts T, transports the original signed connector actions,
   and contracts all three response channels into K. It checks the finite source, source
   moments, calibration denominator, signed lane identities, and retained
   interval relationships.
2. Conservative rational square-root, exponential, and pi bounds propagate
   the weighted Duhamel estimate and centered-rate inequality from the
   inherited hard-branch enclosures. The output records the resulting outer
   bounds and checks the printed table's outward rounding.
3. A separate high-precision `mpmath` route computes numerical eigensystems
   and scalar representatives. Polynomial residuals, source moments, and
   representative containment provide independent numerical cross-checks.

The compact calculation receives the certified hard gap, branch matrix element,
and preparation-energy enclosures. It does not solve the interacting hard
eigenbranch problem afresh. Its arithmetic reconstruction and high-precision
representatives are identified separately in the generated JSON.

The important distinctions are exercised in the code and explained in
[MODEL.md](MODEL.md): the placement calibration expectation is `573049`, the
declared hard-field coherent preparation is a different state, the signed
coupling is negative in every ordered lane, and all phase-action coefficients
use the same actual rate.

The [second-order test](SECOND_ORDER.md) independently derives the weak-coupling
hard-gap shift with both polarizations and both counterterms. Its continuum
coefficient enclosures agree with the retained hard-gap intervals in every
lane. A separately declared finite-mode model checks fourth-order residual
scaling as the coupling halves. The generated report keeps these two checks
distinct from the exact hard preparation and full-field clock certificate.

### Preserved native-output replay

The original H002630 independent checker is retained unchanged under
[`evidence/native/verification`](../evidence/native/verification). The wrapper
[`scripts/verify_native.py`](../scripts/verify_native.py) supplies a relocated,
repository-relative view of the checker inputs. Its evidence mapping preserves
the exact original bytes and original paths as provenance.

The expected scientific-checker summary is:

| Field | Retained result |
|---|---:|
| Independent checks | 23,804 |
| Passing checks | 23,804 |
| Native outputs covered | 300 |
| Matrix readouts covered | 134 |
| Unsupported outputs | 0 |
| Failed checks | 0 |

These counts belong to the original independent checker; wrapper custody checks
are reported separately. The retained native campaign itself executed 300
operations with 1,122 passing native checks, zero failed native returns, and
zero failed native checks. Native engine checks and independent replay checks
are different totals.

The replay reconstructs rational primitives and follows a separate
high-precision spectral/transcendental route. It checks stored inputs and
outputs from the completed campaign. It does not invoke a native engine, run
another scientific campaign, or alter the retained certificates. See
[NATIVE_EVIDENCE.md](NATIVE_EVIDENCE.md) for the evidence bundle's exact scope.

To check the packaged evidence's path mappings and hashes without running the
scientific replay:

```sh
python scripts/verify_native.py --integrity-only
```

## Rebuild the chapter PDF

The checked-in [`manuscript/Chapter_I.pdf`](../manuscript/Chapter_I.pdf) preserves
the reviewed seven-page draft byte for byte. Its editable source is
[`manuscript/chapter_I.md`](../manuscript/chapter_I.md). To produce the
repository edition, use Python 3.12 and the pinned typesetting requirements:

```sh
python -m pip install -r requirements-pdf.lock
python scripts/build_pdf.py --output build/Chapter_I.pdf
python scripts/verify_pdf.py build/Chapter_I.pdf
```

The builder uses bundled fonts, repository-relative assets, and deterministic
metadata. The pinned Python 3.12 environment records the initial repository
build dependencies. The optional `pdf` package extra is also available, while
the lock file pins the complete typesetting dependency set. The preserved
reviewed PDF and rebuilt repository edition have separate provenance: the
retained PDF's original bytes remain unchanged, and the rebuilt edition uses
the same manuscript text. The numerical reproduction commands operate
independently of the PDF build. PDF checks concern page count, text and
typesetting; scientific checks concern the data and equations.

Check the portable repository assets and scientific evidence inventories with:

```sh
python scripts/verify_repository.py
python scripts/verify_native.py --integrity-only
```

## Read the numerical result

The certified interval covers the entire normalized bare cycle
`0 <= tau <= 573049*pi`. The six lanes are six separately prepared evolutions.
The published columns below show `10^6 * nu`; each endpoint is rounded outward
to twelve decimal places from retained rational endpoints.

| Lane | Lower | Upper |
|---|---:|---:|
| 01 | 3.490102929541 | 3.490102934505 |
| 02 | 3.490102893142 | 3.490102914462 |
| 03 | 3.490095588823 | 3.490098892473 |
| 12 | 3.490102927880 | 3.490102933590 |
| 13 | 3.490096147687 | 3.490099200196 |
| 23 | 3.490096722560 | 3.490099516734 |

All lower bounds are positive. All upper bounds are below the bare rate
`Delta = 2/573049`. The phase is a continuous lift of `-arg(z)` and has a
continuously differentiable inverse on its image throughout this time interval.
The coefficient table in the chapter receives each lane's same underlying
rate; its marginal interval images are dependent quantities.

Rates are per normalized model time. The conditional physical conversion is
`nu_phys = (lambda_ref/t_SW) * nu` in the declared chart. No numeric value of
`lambda_ref/t_SW` is assigned here.

## Analytical and computational responsibilities

The continuum construction, form-domain regularity, matched reference, and
weighted Duhamel argument are analytical parts of the model. Their full
assumptions and derivation are recorded in [MODEL.md](MODEL.md), the chapter,
and the retained derivation sources. Computation checks the exact finite
matrices, scalar enclosures, source-dependent positivity margins, inverse
rate images, and displayed numerical consequences.

The original native campaign used the qualified external GEN6 Duck runtime
and retained its execution receipts. A new native scientific campaign requires
that separately qualified installation, its discovered capability contract,
source bindings, resource admission, and custody workflow. This repository
contains the executable Chapter I reproduction layer and frozen evidence;
it does not supply a replacement Duck runtime.

## Changing a calculation

The published result is tied to its retained packet, preparation, and interval.
For an exploratory change, write generated results to a new output directory
and preserve the published packet and evidence. Record the changed source
assignment or parameter, precision, command, output, and comparison to the
published result. Recomputing a new scalar bound from a changed input should
be labeled as that new calculation, with its own provenance.

The tests include failure cases so that lost signs, omitted terms, corrupted
source data, and inward-rounded or invalid intervals can be detected where
covered. Passing tests report the checks implemented here; the separate
analytical derivation carries the continuum argument.
