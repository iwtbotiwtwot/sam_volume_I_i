# Original mathematical sources

The two PDFs preserve the supplied original action manuscript and centered-clock
refinement note. Their exact source hashes are listed in
[`docs/PROVENANCE.md`](../docs/PROVENANCE.md).

`derivations/` contains unchanged source derivations from the completed research:

- `ORIGINAL_SOURCE_DERIVATION.md`: signed source, characteristic equation,
  capacity normalization and original receiving assignments;
- `RESOLVED_CLOCK_DERIVATION.md` and `HARD_CLOCK_DERIVATION.md`: the retained
  interacting hard branches, full soft remainder and preparation;
- `DERIVATION_DRAFT.md`: lane 01, calibration spectral weights and first uniform
  clock estimates;
- `DOMAIN_SUPPLEMENT.md`: continuum form and continuously differentiable clock;
- `REFERENCE_SUPPLEMENT.md`: exact same-realization hard reference;
- `WEIGHTED_DUHAMEL.md`: achieved propagation bound used in the final all-six result.

These files preserve the state of analysis at their original creation, including
then-pending statements. The final manuscript and retained completed results
identify the achieved outcome; the original derivations are not silently edited.

`native_jobs/` preserves the six original graph-builder programs used for the nine
mathematical jobs. Their imports, absolute source bindings and compiled task route
refer to the qualified external SAM/GEN6 installation. They are source records,
not standalone entry points. The exact operation inputs, outputs, task receipts
and returned values are available through the hash-bound `evidence/` package.

The standalone entry points are `scripts/reproduce.py` and
`scripts/verify_native.py`. Fresh native execution uses the independently
qualified runtime and its dynamically discovered capability menu; these files
do not install or recreate that runtime.
