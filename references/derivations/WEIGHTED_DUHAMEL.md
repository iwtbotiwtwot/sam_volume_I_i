# A propagated weighted difference for the actual and hard-reference clocks

Date: 2026-10-15. Status: new analytical derivation for the Chapter I successor.
This argument supplies a propagated centered-correlator bound using the declared
hard-branch preparation and complete soft field. Numerical satisfaction of the
resulting condition belongs to the actual native execution receipts.

ORIGINATOR / CONCEPTUAL DIRECTOR: Sean Brady.

AI RESEARCH COLLABORATORS: OpenAI ChatGPT and Codex.

This is a Codex mathematical contribution developed during the successor's
second-round analysis. The previously bound derivation files remain unchanged.

## 1. Fixed lane, common Hamiltonian phases, and assumptions

Work in one fixed spectral lane in the normalized model-time chart. Use the
same full two-polarization Fock realization and closed forms as
`DOMAIN_SUPPLEMENT.md`. Write

```text
H=epsilon*e+H_red,
H_red=epsilon*S+K,
S=sigma_x,
K=H_f-g*(sigma_z*phi_plus+sigma_y*phi_cross)+c,
c=2*g^2*mu,
mu=integral_0^infinity |u_R(omega)|^2/omega d omega,
A=I+H_f.
```

The positive field block `K` and the full closed form have domain `Q(H_f)`.
The signed coupling `g`, `epsilon>0`, and the lane even energy remain fixed.
The field is not truncated in photon number or frequency.

Let `H_ref` be the hard Hamiltonian plus the full free soft Hamiltonian, the
same lane even scalar, and the exact soft counterterm, as constructed in
`REFERENCE_SUPPLEMENT.md`. Then

```text
H=H_ref+V_s,
V_s=-g*(sigma_z*phi_(plus,s)+sigma_y*phi_(cross,s)).
```

Both evolutions begin at the identical declared vector

```text
psi_prep=(Phi_0+Phi_1)/sqrt(2) tensor |0_s>,
psi(t)=exp(-itH)*psi_prep,
chi(t)=exp(-itH_ref)*psi_prep.
```

The exact normalized hard eigenbranches `Phi_0,Phi_1` and their relative phase
are inherited. They have finite hard free form energy. The reference includes
the same exact scalar counterterm as the actual Hamiltonian; a numerical upper
ceiling for that scalar is used only for bounding energy. Independent changes
of the actual and reference global phases would change the vector distance
and are not made here.

Let the soft frequency range be `0<omega<lambda`, with

```text
v_s=integral_0^lambda |u_R(omega)|^2 d omega,
m_(1,s)=integral_0^lambda omega*|u_R(omega)|^2 d omega.
```

Both are finite for the retained kernel, and `m_(1,s)<=lambda*v_s`. The native
upper enclosure `v_soft` may replace the exact `v_s` in all upper bounds below.

Assume the inherited uniform free-energy estimate is `E_f(t)<=F_T` for the
actual trajectory over `0<=t<=T`, with

```text
F_T=[sqrt(c)+sqrt(K_prep+epsilon*E(T))]^2,
E(T)=exp(4*g^2*v_soft*T^2)-1.
```

Also check the elementary dimensionless shift condition

```text
2*epsilon+3*c+1/2 <= 2.
```

An upper enclosure for its left side is sufficient for native certification.
Section 2 gives a version without this convenient numerical condition.

## 2. Uniform propagation in the free-energy form norm

The positive square form defining `K` is the norm square of the full energy
annihilation map minus the two source shifts. The squared norm of the source
shift is `c` on a normalized fixed-lane state. The triangle inequality in that
direct-integral Hilbert space therefore gives both form inequalities

```text
H_f <= 2*K+2*c*I,
K <= 2*H_f+2*c*I.
```

Define the positive shifted generator

```text
B_0=H_red+(epsilon+c+1/2)*I.
```

Because `S+I>=0`, the first inequality gives

```text
A=I+H_f <= 2*B_0.
```

The second and `S<=I` give

```text
B_0 <= 2*H_f+(2*epsilon+3*c+1/2)*I <= 2*A.
```

The actual evolution commutes with `B_0` and preserves its form norm; the
removed even scalar changes only a common phase. Consequently

```text
||A^(1/2)*exp(-itH)*xi|| <= 2*||A^(1/2)*xi||
```

for every `xi in Q(H_f)` and every real `t`. This evolution is strongly
continuous in the `A^(1/2)` norm by its equivalence to the `B_0^(1/2)` norm.

More generally set `b=max(2,2*epsilon+3*c+1/2)`. The same calculation gives
`B_0<=b*A` and an evolution bound `C_U=sqrt(2*b)` instead of 2. The convenient
shift condition selects `C_U=2`; it is not a premise about physical units or
a restriction introduced into the receiving law.

## 3. A forcing term in the full free-energy form domain

Write the reference as a hard vector `chi_h(t)` times the soft vacuum, with
its common scalar phases retained. Since soft annihilation operators kill the
vacuum,

```text
V_s*chi(t)
 =-g*[sigma_z*chi_h(t) tensor a_(plus,s)^*(u_s)|0_s>
      +sigma_y*chi_h(t) tensor a_(cross,s)^*(u_s)|0_s>].
```

The two soft one-photon vectors are orthogonal, including in the soft-energy
form pairing. Each source Pauli operator is unitary and commutes with the hard
free-field Hamiltonian. Thus, with `E_(h,ref)(t)=<H_(f,h)>_(chi_h(t))`,

```text
||A^(1/2)*V_s*chi(t)||^2
 =2*g^2*[v_s*(1+E_(h,ref)(t))+m_(1,s)]
 <=2*g^2*v_s*(1+E_(h,ref)(t)+lambda).
```

In particular the forcing vector lies in `Q(H_f)`. This argument uses the
finite soft smearing norm and its first energy moment; it needs no full-field
equal-time second moment and no unweighted ultraviolet norm of the hard
smearing.

The hard charge selection rule makes the reference expectation of `S`
constant: `S=2*N_s-I` preserves charge, so its off-diagonal matrix element
between the charge-0/1 branches vanishes. The reference energy is also constant.
The expectation of the full positive block `K` in the reference is therefore
its initial value, at most `K_prep`. The soft interaction expectation is zero,
and its exact counterterm remains included. The full square-form inequality
then gives

```text
E_(h,ref)(t)=E_(f,ref)(t)
 <=[sqrt(c)+sqrt(K_prep)]^2 <= F_T.
```

It follows that both trajectories obey

```text
||A^(1/2)*psi(t)|| <= sqrt(1+F_T),
||A^(1/2)*chi(t)|| <= sqrt(1+F_T),
||A^(1/2)*V_s*chi(t)||
 <=sqrt(2*g^2*v_s*(1+F_T+lambda)).
```

## 4. Duhamel identity as a form-domain Bochner integral

The reference is a finite superposition of exact hard eigenvectors times the
free soft vacuum. Hence `chi(t) in D(H_ref)` and its Hilbert-space derivative
exists continuously. Section 3 supplies `V_s chi(t) in Q(H_f)`, continuously in
that form norm because the hard reference spans two fixed form-domain vectors
with continuously varying scalar phases.

The operator representation of the full form now also puts `chi(t)` in
`D(H)`: for every form test vector, its full form pairing is represented by
the Hilbert vector `H_ref chi(t)+V_s chi(t)`. Thus the usual Hilbert-space
variation-of-constants identity applies without assuming that `V_s` maps the
entire form domain into itself:

```text
psi(t)-chi(t)=-i*integral_0^t exp(-i*(t-s)*H)*V_s*chi(s) ds.
```

Its integrand is also a continuous `Q(H_f)`-valued function. The uniform
propagation bound from Section 2 makes the integral a Bochner integral in the
`A^(1/2)` norm. Its image in the Hilbert space equals the same Duhamel integral,
so the identity holds in the form domain itself. Therefore

```text
delta_A(t):=||A^(1/2)*(psi(t)-chi(t))||
 <=2*t*sqrt(2*g^2*v_s*(1+F_T+lambda))
```

for `0<=t<=T` under the checked shift condition. The corresponding general
bound replaces the initial factor 2 by `C_U`.

## 5. Propagated centered joint-correlator error

The bounded weighted form for
`B=S*(phi_cross-i*phi_plus)` has constant `sqrt(2*mu)`. Expansion of the two
expectations gives

```text
|<B>_(psi(t))-<B>_(chi(t))|
 <=sqrt(2*mu)*delta_A(t)
   *[||A^(1/2)*psi(t)||+||A^(1/2)*chi(t)||].
```

The exact reference identification is

```text
<B>_(chi(t))=w_h(t)=i*(Delta-Omega)*M*exp(-i*Omega*t)/(2*g).
```

Combining the preceding estimates yields the achieved uniform bound

```text
sup_(0<=t<=T)|w(t)-w_h(t)| <= W_D(T),
W_D(T)=8*|g|*T*sqrt(mu*v_s*(1+F_T)*(1+F_T+lambda)).
```

It is safe to replace every upper-bound operand by a certified conservative
upper enclosure, including `v_s<=v_soft`. The general evolution factor gives
`W_D(T)=4*C_U*|g|*T*sqrt(mu*v_s*(1+F_T)*(1+F_T+lambda))`.

This estimate propagates the exact initial centered cancellation and vanishes
at `T=0`. It retains the complete hard Hilbert space through its finite-energy
reference branches and the whole soft Hilbert space through Duhamel evolution
under the full Hamiltonian. The one-soft-photon vector appears only in the
reference forcing term; the actual evolved state is not restricted to that
sector.

## 6. Uniform centered clock condition and native result boundary

In the inherited `0<Omega<=Delta` regime, retain the same true parameters in
the centered sufficient condition:

```text
2*|g|*W_D(T)+Delta*E(T) < Omega*M,
M-E(T)>0.
```

An outer native enclosure can use lower endpoints for `Omega,M`, upper endpoints
for `|g|,Delta,E(T),F_T,mu,v_s,lambda,T`, and the checked shift condition. A
strictly positive lower endpoint of

```text
Omega*M-Delta*E(T)-2*|g|*W_D(T)
```

together with the positive amplitude margin supplies uniform positive rate.
The form-Ehrenfest and phase construction in `DOMAIN_SUPPLEMENT.md` give its
pointwise interpretation and the corresponding instantaneous phase inverse.

This is a new achieved analytical propagation bound, distinct from the
triangle bound in `REFERENCE_SUPPLEMENT.md` and from a budget alone. Its native
evaluation and the resulting signs for all six lanes must be reported from
actual execution receipts. Before those values return, this derivation assigns
no numerical pass outcome to lanes 03, 13, or 23. Any returned inconclusive
lane remains explicitly retained.

## 7. Source pointers

Project-relative paths resolve against
`/home/lilhelper/SAM_Research_Overflow/SAM_Research_Project`.

- `GEN4/samland_resolved_clock1/DERIVATION.md`, Sections 1--5: exact hard
  preparation, conserved charge, complete soft split, and all-time energy law.
- `GEN4/duck_write_coupling_clock1_20261015/clock/DERIVATION.md`: inherited
  source-derived signed receiving scales and hard clock inputs.
- `GEN4/duck_write_coupling_clock1_20261015/clock/POINTWISE_DERIVATION.md`:
  sharper preparation energy and whole-field energy form.
- `GEN4/duck_chapter1_lane1_20261015/derivation/DOMAIN_SUPPLEMENT.md`: weighted
  continuum construction, full closed form, and exact continuously
  differentiable clock.
- `GEN4/duck_chapter1_lane1_20261015/derivation/REFERENCE_SUPPLEMENT.md`: the
  actual hard comparison trajectory and its zero reference mismatch.
- `GEN4/duck_chapter1_lane1_20261015/derivation/DERIVATION_DRAFT.md`: lane
  source/action construction and uniform monotonicity result.

All mathematical inequalities above concern the given fixed receiving law.
They do not assign physical SI units, select a new preparation mechanism,
replace the original source ledger, or alter a completed artifact.
