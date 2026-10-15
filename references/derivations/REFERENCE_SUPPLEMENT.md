# The actual hard reference and a uniform centered field-form bound

Date: 2026-10-15. Status: new analytical supplement. This document identifies the
hard comparison trajectory in the specified continuum realization and derives
an achieved coarse bound for its joint-correlator difference. Native R2 results
are reported in the successor execution record; no R2 numerical outcome is
asserted here before its receipt is returned.

ORIGINATOR / CONCEPTUAL DIRECTOR: Sean Brady.

AI RESEARCH COLLABORATORS: OpenAI ChatGPT and Codex.

This supplement is a Codex mathematical contribution to the authorized Chapter I
successor. The previously bound `DERIVATION_DRAFT.md` and `DOMAIN_SUPPLEMENT.md`
remain unchanged.

## 1. The same field realization and declared preparation

Fix one of the six spectral source lanes. Use its inherited signed
`g=epsilon*(q_a-q_b)`, even source energy `epsilon*e`, bare rate
`Delta=2*epsilon`, and the retained split `lambda=64*Delta`. All quantities use
the same normalized model-time chart.

The one-particle frequency split gives the canonical Fock factorization

```text
F(L2((0,infinity);C^2))
  = F(L2([lambda,infinity);C^2)) tensor F(L2((0,lambda);C^2)).
```

Endpoints of measure zero do not affect this factorization. The two factors
contain the complete hard and soft mode spaces, respectively. Each contains
both polarizations and all photon sectors.

Let

```text
mu_h=integral_lambda^infinity |u_R(omega)|^2/omega d omega,
mu_s=integral_0^lambda |u_R(omega)|^2/omega d omega,
mu=mu_h+mu_s,
c_h=2*g^2*mu_h,
c_s=2*g^2*mu_s.
```

The exact theoretical soft counterterm is the scalar `c_s`. An upper enclosure
for it is used in the native preparation-energy bound; that upper enclosure
does not replace the exact scalar in the Hamiltonian definition. Scalar changes
of reference energy would in any event cancel from the expectations below.

Use the inherited hard Hamiltonian, including its hard counterterm,

```text
H_h=H_(f,h)-g*(sigma_z*phi_(plus,h)+sigma_y*phi_(cross,h))
    +c_h+epsilon*S,
S=sigma_x.
```

The even term is displayed separately. Define the reference Hamiltonian by

```text
H_ref=epsilon*e+H_h+H_(f,s)+c_s.
```

The actual full Hamiltonian is

```text
H=H_ref-g*(sigma_z*phi_(plus,s)+sigma_y*phi_(cross,s)).
```

Both Hamiltonians are forms in the same source and Fock Hilbert space, with the
same form domain `Q(H_f)`. This follows from the weighted-form construction in
`DOMAIN_SUPPLEMENT.md`; removing the soft interaction changes neither domain
nor the field representation.

The inherited exact hard branches `Phi_0,Phi_1` have signed charges 0 and 1,
energies `E_0,E_1`, and true gap `Omega=E_1-E_0`. The exact initial preparation
is

```text
psi_prep=(Phi_0+Phi_1)/sqrt(2) tensor |0_s>.
```

The branch energies and eigenvectors here are the declared retained hard
preparation, rather than Gaussian trial states or midpoint approximations to
native intervals. Their finite hard form energy, together with the soft
vacuum, places this vector in `Q(H_f)`.

Define the actual and comparison trajectories from this same vector:

```text
psi(t)=exp(-itH)*psi_prep,
chi(t)=exp(-itH_ref)*psi_prep.
```

The positive hard frequency split is used in the inherited branch-isolation
argument. There is no positive lower bound imposed on the full continuum,
and no full massless ground-state assertion is needed for this comparison.

## 2. Exact reference source amplitude

Set

```text
Z=sigma_z+i*sigma_y,
z(t)=<Z>_(psi(t)).
```

`Z` lowers the inherited signed hard charge by one. Thus charge selection
eliminates its diagonal branch matrix elements and its reverse transition.
With the declared relative branch phase,

```text
<Phi_0|Z|Phi_1>=2*M,
M>0.
```

The factor two follows from `Z=2*sigma_-` in the source-energy basis; the
retained `M` is the overlap multiplying the equal-superposition source
amplitude. Expanding the comparison trajectory gives

```text
h(t):=<Z>_(chi(t))=M*exp(-i*Omega*t).
```

The even source energy and the scalar soft counterterm multiply both hard
branches by the same phase within this lane and cancel in this expectation.
They remain in the complete source energy and action accounts.

## 3. Exact reference joint correlator and zero mismatch

Use the same full field form in both trajectories:

```text
B=S*(phi_cross-i*phi_plus),
w(t)=q_B(psi(t),psi(t)),
w_ref(t)=q_B(chi(t),chi(t)).
```

The comparison state remains a product with the soft vacuum. Each soft field
has zero vacuum form expectation, and therefore its source-field insertion
also has zero comparison expectation. The full reference expectation equals
the hard insertion expectation.

The hard form-Ehrenfest identity, valid on this same domain, is consequently

```text
dot(h)=-i*Delta*h+2*g*w_ref.
```

Since `dot(h)=-i*Omega*h`, the exact result is

```text
w_ref(t)=i*(Delta-Omega)*h(t)/(2*g)=w_h(t).
```

Thus the algebraic reference `w_h` in the centered refinement is realized by
the explicit comparison trajectory, with reference mismatch equal to zero.
In particular,

```text
|w_h(t)|=|Delta-Omega|*M/(2*|g|),
z(0)-h(0)=0,
w(0)-w_h(0)=0.
```

This identification uses the inherited branch preparation, charge selection,
and exact clock equation. It requires neither a field second moment nor an
unweighted `L2` norm of the full smearing. The finite weighted norm `mu` and
the form-domain construction supply the field pairings and Ehrenfest identity.

## 4. Achieved coarse uniform centered bound

For a normalized form-domain actual state, define the two real form expectations

```text
A_cross=<S*phi_cross>,
A_plus=<S*phi_plus>.
```

They are real because the two factors commute and are self-adjoint in the form
pairing. The annihilation energy estimate and `S^2=I` give

```text
|A_a|<=2*sqrt(mu*E_(f,a)).
```

Since `w=A_cross-i*A_plus`, this gives the complete two-polarization bound

```text
|w|^2=A_cross^2+A_plus^2<=4*mu*(E_(f,cross)+E_(f,plus)),
|w|<=2*sqrt(mu*E_f).
```

The uniform full-field energy enclosure from R1 is `E_f(t)<=F_T` for every
`0<=t<=T`, where

```text
F_T=[sqrt(c)+sqrt(K_prep+epsilon*E(T))]^2,
c=2*g^2*mu,
E(T)=exp(4*g^2*v_soft*T^2)-1.
```

The triangle inequality now supplies an achieved uniform centered error bound:

```text
sup_(0<=t<=T) |w(t)-w_h(t)|
 <= W_coarse(T)
 :=2*sqrt(mu*F_T)+|Delta-Omega|*M/(2*|g|).
```

This is an actual analytical bound on the error, evaluated natively using the
retained full-field energy operands. It is distinct from an allowed error
budget. It also discards the exact initial cancellation `w(0)=w_h(0)` and the
later signed correlation structure. A sharper propagated bound remains a
useful next calculation.

## 5. Centered positivity condition and directed outer bounds

Retain `delta_z=z-h`, `delta_w=w-w_h`, and the same true parameters throughout.
The exact centered residual is

```text
r=dot(z)+i*Omega*z
 =-i*(Delta-Omega)*delta_z+2*g*delta_w.
```

If `|delta_z|<=E_T<M`, `|delta_w|<=W_T`, and `Omega>0`, the symmetric
absolute-error sufficient condition is

```text
|Delta-Omega|*E_T+2*|g|*W_T < Omega*(M-E_T).
```

In the inherited source regime `0<Omega<=Delta`, the same true `Omega` on both
sides simplifies this before outer bounding to

```text
2*|g|*W_T+Delta*E_T < Omega*M.
```

The sufficient-test margin is therefore

```text
F=Omega*M-Delta*E_T-2*|g|*W_T.
```

A directed rectangular implementation may use

```text
Omega_lo<=Omega, M_lo<=M<=M_hi,
0<G_lo<=|g|<=G_up,
Delta<=Delta_up, E_T<=E_up,
F_T<=F_up, mu<=mu_up.

W_actual_up=2*sqrt(mu_up*F_up),
W_reference_up=(Delta_up-Omega_lo)*M_hi/(2*G_lo),
W_up=W_actual_up+W_reference_up,
F_lo=Omega_lo*M_lo-Delta_up*E_up-2*G_up*W_up.
```

These expressions require the retained `Omega<=Delta`, a positive coupling
magnitude lower bound, and directed outward arithmetic. The exact identities
retain the shared true parameters; independent endpoint choices above form a
safe outer set. A positive `F_lo`, together with the positive uniform amplitude
margin, certifies the centered condition on the entire segment.

The corresponding uniform allowed budget is

```text
B_T=(Omega_lo*M_lo-Delta_up*E_up)/(2*G_up).
```

Its positivity by itself is an accuracy target. The achieved bound passes the
sufficient test only when its certified upper endpoint is strictly below a
certified lower endpoint of `B_T`. Equality supplies at most a nonnegative
margin; an inconclusive interval remains inconclusive.

The weighted-form lemma gives a separate target
`B_T/sqrt(2*mu)` for an appropriate weighted trace distance. That distance has
not been propagated or evaluated merely by evaluating this target.

## 6. Relation to the direct coarse clock result

For exact parameters in the regime `Omega<=Delta`, inserting `W_coarse` into
the centered condition yields

```text
4*|g|*sqrt(mu*F_T)+Delta*E_T < (2*Omega-Delta)*M.
```

The direct whole-field rate condition from R1 is

```text
4*|g|*sqrt(mu*F_T)+Delta*E_T < Delta*M.
```

Thus this triangle-bound centered test is more demanding than the direct
coarse test. It does not supply the cancellation gain sought from a signed
propagator. Its contributions are the explicit zero-mismatch reference,
an achieved uniform correlator-error enclosure, and a concrete comparison with
the sharper error budget. A positive centered margin is still a valid uniform
result wherever its returned native interval supplies that sign.

At preparation time the true centered error vanishes; the triangle bound pays
the two magnitudes separately. Exploiting that initial cancellation and its
subsequent joint dynamics is the natural route to a sharper `W` or direct
residual enclosure.

## 7. Numerical status and remaining lanes

R1's uniformly positive lanes are 01, 02, and 12. Its coarse whole-cycle rate
intervals for 03, 13, and 23 contain zero. The centered R2 task retains all six
lanes and computes its margins and budget ratios using the achieved coarse
`W` above. Until its actual receipts return, this supplement assigns no
additional centered pass/fail outcomes. The numerical results belong to the
R2 result table and final campaign report.

A zero-containing bound is not an observed clock reversal. For any lane whose
centered test remains unresolved, the next estimate should propagate the
signed difference `w-w_h`, a suitable weighted state difference, or the direct
residual `r`, retaining the same field domain and common parameters. Full
continuum and numerical error payments remain part of that successor result.

## 8. Source and execution pointers

All project-relative paths below resolve against
`/home/lilhelper/SAM_Research_Overflow/SAM_Research_Project`.

- `GEN4/samland_resolved_clock1/DERIVATION.md`, Sections 1--5: original hard
  split, exact charge branches, coherent preparation, and all-time energy law.
- `GEN4/duck_write_coupling_clock1_20261015/DERIVATION.md` and
  `clock/DERIVATION.md`: source-derived signed couplings and the retained exact
  initial correlation.
- `GEN4/duck_write_coupling_clock1_20261015/clock/POINTWISE_DERIVATION.md`: the
  whole-field joint-form bound and sharper preparation energy.
- `GEN4/duck_chapter1_lane1_20261015/derivation/DERIVATION_DRAFT.md`: lane
  operators, reference distinction, and uniform monotonicity theorem.
- `GEN4/duck_chapter1_lane1_20261015/derivation/DOMAIN_SUPPLEMENT.md`: complete
  weighted continuum form, self-adjoint Hamiltonian, and exact `C1` clock.
- `GEN4/duck_chapter1_lane1_20261015/ops/r2_clocks.py`: native centered budget,
  achieved coarse-error enclosure, and inverse/action coefficient graph.
- `GEN4/duck_gen6_local/runs/chapter1-lane01-20261015-01/workers/G6_03/tasks/r1_uniform_whole_cycle_clocks/RESULT.json`:
  actual R1 uniform full-field energy and rate outputs.
- `GEN4/duck_gen6_local/runs/chapter1-lane01-20261015-01/workers/G6_07/tasks/r2_centered_uniform_budgets/RESULT.json`:
  R2 centered outputs when returned; this path is an execution pointer, not a
  claim that a result has already returned at this supplement's creation.
