# Retained native evidence and independent replay

The Chapter I successor campaign completed on 15 October 2026. Its original
retained evidence records **9 tasks, 300 native operations, 1,122 passing native
checks, zero failed native checks**, and the independent checker returned
**23,804 passing checks across 134 matrix readouts and all 300 native trace
outputs**. The campaign classification is: **The test result suggests strong
contact with the concept.**

This repository includes the exact scientific files needed to repeat that
independent numerical check. Running the commands below performs ordinary
Python independent verification of retained results; it does not start Duck or
replace the native interval certification with newly generated intervals.

## Run the replay

After installing the pinned project dependencies, run from the repository root:

```bash
python scripts/verify_native.py --integrity-only
python scripts/verify_native.py --output build/native_verification.json --precision 160
```

The first command validates the complete portable package: **615 artifacts,
18,677,823 bytes**. The second executes the original checker and writes its full
report. A successful replay returns exit code 0, `status: PASS`, `checks: 23804`,
`passed_checks: 23804`, `receipt_count: 9`, `trace_outputs: 300`, and
`verified_matrix_readouts: 134`, with no failures or unsupported readouts.
The checker uses exact `fractions.Fraction` arithmetic and `mpmath==1.3.0` at
160 decimal digits. A minimum of 100 decimal digits is accepted by its original
interface; 160 repeats the retained verification setting.

The report records the current checkout's resolved paths, so its JSON bytes
differ from the historical report after relocation. Its mathematical checks,
task scope, source input hash, and passing counts reproduce the original.

## What is preserved

| Repository path | Role |
| --- | --- |
| `evidence/MANIFEST.json` | Complete inventory of this portable export, with original-to-local paths, byte counts, SHA-256 hashes, task index, and expected verification scope. |
| `evidence/native/sources/EXACT_INPUTS.json` | Unchanged exact extraction of the predecessor source and clock operands used by the successor campaign. SHA-256: `77ab5aa2a22f2c3961484f447a30aa21a83596f4fe04204d57509851f7d6dabd`. |
| `evidence/native/sources/SOURCE_MANIFEST.json` | Unchanged upstream extraction provenance, including the original source PDFs, four predecessor receipts, and 529 predecessor native trace outputs. |
| `evidence/native/RESULTS.json` | Unchanged original successor result summary, including exact six-lane rate intervals and positive margins. |
| `evidence/native/run/workers/*/tasks/*/RESULT.json` | All nine unchanged successor task receipts, including native checks and returned matrix readouts. |
| `evidence/native/run/workers/*/tasks/*/gen6/` | All 300 native input/output pairs, unchanged and individually hash-bound in their task receipts. |
| `evidence/native/verification/independent.py` | Original independent checker, byte-for-byte unchanged. |
| `evidence/native/verification/ORIGINAL_VERIFICATION.json` | Original complete passing checker report. SHA-256: `32a8a74ef1f40b286b96cffc151c9ad014f3f7d240140ffb850cd221d129272a`. |
| `evidence/native/provenance/EXECUTION_CUSTODY.json` | Unchanged full upstream custody record covering 1,203 source/new files; its inventory extends beyond this portable export. |

The portable package has 600 trace files, nine task receipts, and six other
scientific/provenance files. `evidence/MANIFEST.json` is the inventory of the
available files. The retained upstream source and custody manifests describe
a larger historical record: this export does not include every file named by
those historical manifests or revalidate the predecessor campaign. The
predecessor operands are retained exactly in `EXACT_INPUTS.json` for the
successor's reproducible calculations.

## Relocation and failure behavior

Historical absolute paths remain in the original scientific bytes as
provenance. The thin adapter in `scripts/verify_native.py` validates every
bundled file before invoking the checker, then substitutes only the checker's
`Path` constructor with a manifest-bound resolver. It does not edit the
checker, task receipts, formulas, intervals, or trace files.

Each historical trace root is mapped to a repository directory only after
every member's SHA-256 and receipt binding has been checked. Historical paths
without an explicit verified mapping fail. The wrapper never reads missing
inputs from an original SAM checkout or another host location. Missing or
changed artifacts, unsafe paths, symbolic links, unexpected evidence files,
unregistered receipts, and incomplete trace inventories fail before numerical
replay. Output reports must be inside the checkout and outside `evidence/`.

The native evidence tests cover integrity, missing/changed files, path
traversal, symbolic-link escapes, and refusal of an existing host file without
a hash-bound relocation. The full numerical replay is a separate command so
the ordinary unit suite does not silently duplicate scientific calculations.

## Scope of the independent checks

The unchanged checker independently evaluates finite-source matrix algebra,
the original-Q eigensystem and resolvent-cofactor preparation weights,
population energy and variance, common-rate phase-action coefficients, and
the uniform/centered weighted soft-Duhamel formulas. It also checks every
retained native primitive output using the resolved local operands. Rational
representatives of interval inputs are used where the original checker
specifies them; high-precision numerical containment checks retain their
original status as independent checks of the authoritative native enclosures.

The analytical form-domain, reference-state, and Duhamel arguments are given
in the manuscript and model documentation. Numerical replay evaluates their
specified scalar consequences. Marginal coefficient intervals use the same
underlying clock rate; they are not independently variable physical inputs.
