# Original placement generator

`src/sam_chapter1/placements.py` reconstructs the complete signed boundary
incidence **B** and its exact Gram **T = BB*** from the four ordered placement
codes `46501, 46525, 49061, 81829`. It generates **K** from the original signed
source-action table and selected connector ledger recovered from the preserved
source campaign. Python integer and rational arithmetic is used throughout.

Run the complete standalone reconstruction from a clean clone:

```sh
python3 scripts/generate_source.py
```

The same complete JSON is printed and saved to `build/source_generation.json`;
`--output PATH` selects a different artifact path.

Each code encodes seven labelled cube sites as seven base-eight digits, including
the leading zero. The decoded paths, in source order, are:

```text
0 1 3 2 6 4 5
0 1 3 2 6 7 5
0 1 3 7 6 4 5
0 2 3 7 6 4 5
```

Every Write changes one of three bits at one of seven slots. All 21 resulting
targets are forbidden paths. Each retains the sum of the two original parallel
C4-character-zero incidences, with signed weight **−2**. Sorting the union of
ambient target codes supplies 78 columns, without identifying cube rotations,
path reversals, or different target addresses. Each diagonal Gram entry is
21 × 4 = 84; shared target columns give the three off-diagonal entries 8.
The JSON prints every target code and every entry of B, T, and K, as well as
all signed response vectors and transported action witnesses.

These rules were recovered directly from
`SAM_MATTER_LEARNING/generated_bridge.py:check_wiring`,
`SAM_MATTER_LEARNING/native/generated_occupancy.cpp`, and
`GEN4/duck_write_coupling_clock1_20261015/source/build.py:boundary` in the SAM
Research Project. The frozen public account is
[`references/derivations/ORIGINAL_SOURCE_DERIVATION.md`](../references/derivations/ORIGINAL_SOURCE_DERIVATION.md).
The tests independently construct the boundary by distance one in the ambient
21-bit integer address, then compare the contracted result with the chapter T.

## Signed response input

Placement codes alone do not determine K. The additional original rule is

```text
d(s) = sum_connectors J (q_u-q_v) sigma_chi e
K_ij = T_ij dot(d(s_i), d(s_j)) = sum_axis D_axis T D_axis.
```

Here q is +1 for a proton and −1 for a neutron. Each connector retains its
primary FORWARD/REVERSE action choice. At a new placement, that choice selects
the unique source action with the transported endpoint sites. Its signed
octahedral vertex gives e, and its original sigma_chi remains in the response.
All three spatial channels and all reciprocal connectors are retained.

The implementation follows `SAM_MATTER_LEARNING/isotope_interaction.py:wiring`
and `SAM_MATTER_LEARNING/native/isotope_interaction.cpp:construct`. This response
mapping retains its original Codex exploratory receiving-law provenance; it
does not assign physical exchange strength or an energy conversion.

The default operand is packaged as
`src/sam_chapter1/data/placement_response.json`. Its provenance records identify
the immutable archived parent files and the exact extraction. To use a separately
identified original operand or declared control, supply JSON with these keys:

```text
source: {actions: [all 48 original action records], edges: [original edges]}
ledger: {objects: [original role/site/kind records], cycles: [all connectors]}
charges: optional exact override of species charges for declared controls
mode: optional original / reciprocal / flip_primary / erase_sign
```

Then run:

```sh
python3 scripts/generate_source.py --response-input original_response.json
```

The output includes B, T, signed responses, each transported action witness,
K, and the SHA-256 hash of the complete supplied input. Missing actions,
nonreciprocal signs, lost connectors, role mismatches, and floating operands are
rejected. An unavailable ledger is never replaced by a response fitted to K.

## Chapter response provenance

The original selected Li7 construction is the lexicographically first template
ID for inventory Z=3,N=4, as selected in
`SAM_MATTER_LEARNING/program.py:assemblies`:

```text
00828cbc571003430a27ec44758e76bb6c3bb02344a73dec72a0a783a2da567f
```

Its species sequence is `pnnnpnp`, also identified as assignment `046`.
The canonical component 0 has exactly the four chapter placement codes.
The original required records are:

- `SAM_REVIEW/campaigns/GEN3_MATTER_LEARNING3/ASSEMBLIES.json.gz`, stable Li7
  row's `instances[0].transported_ledger`;
- `SAM_REVIEW/campaigns/GEN3_MATTER_LEARNING3/inputs/assemblies.json.gz`,
  the `source` action/edge table;
- equivalently, the exact selected original template body in
  `SAM_REVIEW/campaigns/GEN3_TEMPLATE_GENERATOR4/SEARCH.json.gz`, with the
  original table from that campaign's `INPUT.json` and the documented
  deterministic action transport.

The frozen chapter source records the selected ledger as unavailable at the time
of its creation. That historical statement is preserved. The separately identified
successor packet recovers the actual selected ledger from the retained
`SAM_REVIEW/campaigns/VOLII_PATTERN_SYNTHESIS1/ROSTER.json` record, at JSON
pointer `/rows/5/source_construction/generated_alternative/construction/instances/0/transported_ledger`.
That construction identifies the same selected template and exact source
placement. The source action table is copied from the original
`GEN3_TEMPLATE_GENERATOR4/INPUT.json`. This is a recovery of retained inputs;
it does not infer a ledger by solving for the displayed K.

The recovered ROSTER body is authenticated by its retained shared-source snapshot
in `GEN4/gen6_duck_research_modes1/source_inputs/WEB_EXPORT.json`, record key
`4bafb8ab550253229973a8acb150f7a7e08a472fe04ef4f26517c7b550731569`.
The packet's provenance retains these exact hashes:

| Operand | SHA-256 |
| --- | --- |
| Original `GEN3_TEMPLATE_GENERATOR4/INPUT.json` | `e0ed4de59c5ba930cf379fa63cb61d0ec4cf094b7bd8326c0bd8a1b98daf61c9` |
| Original ROSTER body | `fe9fc9262f003b47df1d372842d8ebf4be660a13c9d1ebf2f669a8ca6d0e07bc` |
| Retained `WEB_EXPORT.json` snapshot | `eb5d82222d864d50c035646017c36914bd652b1e296e55c0efa1ae6079e9ad9d` |
| Bundled successor operand | `9e44bdc8373f88c5348e81b056265bb7dcb1e191772aa1c44772ea0757e40c67` |

The loader rejects changed bundled bytes. Reapplying the original signed
response rule gives, in chapter placement order,

```text
 2  0 -2
 2  2 -4
 2  2  0
 0  2  2
```

Contracting these responses with the generated T reproduces the independently
retained K entry for entry. The tests compare B's independent ambient-bit
definition and the three-channel factorization of K; mirror, reciprocal,
species-erasure, and signed-action controls retain their original roles.

`--boundary-only` is also available and explicitly emits `K: null` and
`response_status: NOT_CONSTRUCTED`. Missing user-supplied response records fail
instead of substituting the chapter's displayed matrix. The small three-slot
ledger in the tests is explicitly synthetic: it separately checks signed
transport, rational operands, and malformed-input failures, and is never
identified as the chapter ledger or a native research result.
