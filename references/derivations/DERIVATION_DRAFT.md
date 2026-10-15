# Chapter I worked example: source lane 01 and its correlated clock

Date: 2026-10-15. Status: mathematical manuscript draft for the new Chapter I
successor. This draft records inherited exact identities and new analytical
deductions separately. Native numerical values and receipt bindings are supplied
by the successor's execution record; this document starts no scientific job.

ORIGINATOR / CONCEPTUAL DIRECTOR: Sean Brady.

AI RESEARCH COLLABORATORS: OpenAI ChatGPT and Codex.

The new monotonicity deduction, spectral-weight unpacking, and weighted-form
lemma below are Codex mathematical contributions developed for the authorized
Chapter I worked example. They are not additional requirements attributed to
the project owner.

## 1. Source bindings and conventions

Project-relative source paths are resolved against
`/home/lilhelper/SAM_Research_Overflow/SAM_Research_Project`.

- `GEN4/duck_write_coupling_clock1_20261015/DERIVATION.md`: original signed
  incidence, retained completed response operand, source polynomial, capacity
  normalization, six signed receiving couplings, and initial correlations.
- `GEN4/duck_write_coupling_clock1_20261015/clock/DERIVATION.md`: exact hard
  charge-0/1 coherent preparation, full soft vacuum, branch/gap and matrix-element
  enclosures, and the signed clock identity.
- `GEN4/duck_write_coupling_clock1_20261015/clock/POINTWISE_DERIVATION.md` and
  `clock/r2_pointwise.py`: whole-field energy-form rate bound, sharper preparation
  energy, soft counterterm, and retained endpoint evaluation.
- `GEN4/duck_write_coupling_clock1_20261015/clock/R2_ACTUAL_SUMMARY.json` and
  `RATE_TABLE.md`: retained exact native endpoints and outward-rounded displays.
- `GEN4/duck_write_coupling_clock1_20261015/FOLLOW_UP.md`: selected question of
  signed joint propagation; no installed full-Fock correlator propagator was
  identified in that completed campaign.
- `GEN4/samland_joint_response1/INPUT.json`: retained boundary-radius assignment.
- `/home/lilhelper/Downloads/SAM_Original_Write_Interacting_Action_v1_1_20261015.pdf`:
  receiving action, Sections 2--5 and Appendices A, B, and H.
- `/home/lilhelper/Downloads/SAM_Clock_Refinement_Condition_and_Targets.pdf`:
  centered identity, conditional positivity condition, error budgets, and field
  comparison question.

Use lifted original Write phase `gamma_W`, common phase `chi`, and interacting
lane phase `gamma = -arg(z)` as distinct symbols. All clock quantities below use
the retained normalized model-time chart. A physical inverse-seconds rate carries
the same reference preparation's factor `lambda_ref/t_SW`.

## 2. Inherited four-source and lane identities

The unit-strength receiving source is the exact real symmetric matrix

```text
Q = [[756,104,40,0],
     [104,2100,0,0],
     [40,0,756,40],
     [0,0,40,756]].
```

Its ordered simple roots `q0 < q1 < q2 < q3` are retained as native exact
isolations. With `x=q-756`, the characteristic polynomial is

```text
p(x) = x^4 - 1344*x^3 - 14016*x^2 + 4300800*x + 17305600.
```

The selected original response ledger remains separate from its completed
retained matrix `K`. This example receives `Q=T+K`; it does not create a
replacement original ledger or determine a physical exchange constant.

Let `|q_a>` denote normalized spectral eigenstates. In the ordered lane basis
`(|q0 q1>, |q1 q0>)`, set

```text
d = q0-q1 < 0,
e = q0+q1+q0*q1,
S = sigma_x,
D = d*sigma_z,
C = i*S*D = d*sigma_y,
H_pair = e*I + sigma_x.
```

The signs follow from `sigma_x sigma_z = -i sigma_y`. Direct Pauli algebra gives

```text
S^2 = I,
D^2 = C^2 = d^2*I,
[D,C] = -2i*d^2*S,
N_s = (I+S)/2,
H_pair = 2*N_s + (e-1)*I,
[N_s,D+i*C] = -(D+i*C).
```

In particular the even energy `e` is invisible to the current rotation while
remaining present in the energy and action. The generator retained in the
original source decomposition is

```text
G = H_pair/2 = N_s + (e-1)*I/2.
```

## 3. Placement reference, spectral preparation, and clock preparation

Write `|e_j>` for the labelled placement basis of the displayed `Q`. The original
reference product is `|e0 e0>`. Its full source energy expectation is exactly

```text
E_ref = <e0 e0|H_pair|e0 e0>
      = 1 + 2*Q00 + Q00^2
      = 573049.
```

Here `Q00=756` is a placement-basis diagonal entry. Since that row also contains
the nonzero entries `104` and `40`, `|e0>` is not a `Q` eigenstate. Thus this
reference expectation is distinct from the energy of the spectral diagonal
state `|q0 q0>`.

The inherited capacity conversion is

```text
epsilon = (hbar/I_s)*(t_u/t_SW)*lambda_ref/E_ref.
```

Under the retained chart `I_s=hbar` and `t_u=t_SW/lambda_ref`,

```text
epsilon = 1/573049,
Delta = 2*epsilon,
g = epsilon*d < 0.
```

This fixes the chart coefficient using the same placement reference. The
physical capacity assignment, action/time conventions, exchange strength, and
source-sphere/field-boundary incidence retain their independent source roles.

### Exact spectral-weight unpacking: new analytical presentation

Let `P_a` be the spectral projector of the simple eigenvalue `q_a`, and define
`p_a=<e0|P_a|e0>`. These weights can be expressed without selecting eigenvector
signs. Set `x_a=q_a-756`. The `(0,0)` resolvent entry is

```text
<e0|(zI-Q)^(-1)|e0>
 = (z-2100)*((z-756)^2-1600) / det(zI-Q).
```

The numerator is the principal minor obtained by deleting placement row and
column zero: the remaining matrix contains the scalar block `z-2100` and the
two-by-two block with diagonal `z-756` and off-diagonal `-40`. Taking its residue
at a simple root yields

```text
p_a = (x_a-1344)*(x_a^2-1600)/p'(x_a).
```

The derivative is with respect to `x`; `dx/dz=1`, so no scale or sign factor is
introduced. The sign of the residue is fixed by the convention `(zI-Q)^(-1)`.
The spectral theorem gives the exact controls

```text
p_a > 0,
sum_a p_a = 1,
sum_a p_a*q_a = 756,
sum_a p_a*q_a^2 = 583952.
```

Strict positivity follows because `|e0>` has a nonzero component in each simple
eigenspace: an eigenvector with placement coordinate zero would have to satisfy
the remaining diagonal/chain equations together with `104*v1+40*v2=0`, which
forces every coordinate to vanish. Equivalently, the displayed resolvent
numerator shares no zero with the characteristic polynomial.

For `c_a=<q_a|e0>`, the coherent product expansion is

```text
|e0 e0> = sum_a c_a^2 |q_a q_a>
        + sum_(a<b) sqrt(2)*c_a*c_b |a,b;+>,
|a,b;+> = (|q_a q_b>+|q_b q_a>)/sqrt(2).
```

Consequently the four diagonal probabilities are `p_a^2`, and the six lane
probabilities are `2*p_a*p_b`. The amplitudes and their coherences travel with
the state; a list of probabilities alone is not its full reconstruction.
Every occupied lane component in this placement product has `S=+1`. Therefore

```text
sum_a p_a^2*(1+2*q_a+q_a^2)
 + sum_(a<b) 2*p_a*p_b*(q_a+q_b+q_a*q_b+1) = 573049.
```

The same symmetry gives `<D>=<C>=0` within each occupied symmetric lane, hence
`z=0` for that lane preparation. The capacity reference itself is therefore
distinct from the interacting clock preparation below, whose `z(0)=M>0`.

## 4. Complete lane energy and action

In the receiving field realization, retain both real polarizations, all continuum
modes, and all photon sectors. Let

```text
mu = integral_0^infinity |u_R(omega)|^2/omega d omega = 1/(4R),
|u_R(omega)|^2 = 2*omega*j2(omega*R)^2/(kappa*pi),
kappa = 4/5.
```

The lane Hamiltonian is

```text
H = epsilon*e*I + epsilon*sigma_x + H_free
    - g*(sigma_z*phi_plus + sigma_y*phi_cross)
    + g^2/(2R)*I.
```

Each polarization contributes `g^2*mu=g^2/(4R)` to the counterterm; their sum is
`2*g^2*mu=g^2/(2R)`. The two square completions retain the cross commutator of
the shifted fields because the source currents do not commute. They do not
select a simultaneous shifted vacuum.

The joint variational action retains its Berry term and the full Hamiltonian,
for example in normalized quantum form

```text
S_joint = I_s * integral [i<psi|dot(psi)> - <psi|H|psi>] d tau.
```

On a segment with a positive actual rate `nu=d gamma/d tau`, the same reciprocal
`1/nu` receives every energy contribution. A field kinetic term expressed using
`partial_gamma(phi)` acquires its additional velocity factor as in the supplied
action manuscript. Common source energy, both counterterms, field energy,
interaction, and joint Berry term remain accounted for.

The original scalar Write one-form is `hbar*(d gamma_W+3*d chi)`. Matching an
occupied source orbit generated by `G` requires a stated path/preparation map
satisfying `I_s*<G>*dot(gamma_W)=hbar*(dot(gamma_W)+3*dot(chi))`. The present lane
example retains that compatibility question and does not identify independent
lifted phases by notation alone.

## 5. Inherited coherent clock and signed initial correlation

Receive the equal coherent exact hard charge-0/1 branches with full soft vacuum,
at the retained split `lambda=64*Delta`. Let `Omega` be their true hard gap and
`M` their retained positive source-current matrix element. Define

```text
Z = (D+i*C)/d = sigma_z+i*sigma_y,
z(t) = <Z>_t,
gamma(t) = -arg(z(t)), continued from gamma(0)=0,
B = S*(phi_cross-i*phi_plus),
w(t) = <B>_t.
```

The exact supplied clock identity is

```text
dot(z) = -i*Delta*z + 2*g*w,
nu = -Im(dot(z)/z), where z != 0.
```

At the retained initial preparation,

```text
z(0)=M>0,
dot(z)(0)=-i*Omega*M,
nu(0)=Omega,
<S*phi_cross>_0 = 0,
<S*phi_plus>_0 = -(Delta-Omega)*M/(2*g).
```

For lane 01, `g<0` and the retained `0<Omega<Delta` make the last real correlation
positive. This sign provides a useful transcription control. Substituting the
two real correlations into the exact identity returns `-i*Omega*M` directly.
They are joint expectations, rather than products of marginal expectations.

## 6. New uniform whole-cycle consequence of the retained coarse bound

This deduction uses the completed whole-field energy method. It is separate
from the new centered signed-correlator propagation question.

### Hypotheses

Use one fixed admissible lane parameter set throughout. For every `0<=t<=T`,
assume the inherited analytical bounds hold:

```text
E(t) = exp(alpha*t^2)-1, alpha=4*g^2*v_soft >= 0,
|z(t)-M*exp(-i*Omega*t)| <= E(t),
M >= M_lo > 0,
K(t) <= K_prep + epsilon*E(t),
E_free(t) <= [sqrt(c)+sqrt(K_prep+epsilon*E(t))]^2,
c=2*g^2*mu >= 0,
K_prep >= 0,
|nu(t)-Delta| <= 4*|g|*sqrt(mu*E_free(t))/|z(t)|.
```

Here `K_prep` is the retained preparation upper bound including the full soft
vacuum counterterm, and the free energy sums both polarizations. The exact
current identity is valid on the propagated form domain. It suffices for `z`
to be absolutely continuous and for the rate identity to hold almost
everywhere; an everywhere classical rate uses the corresponding regularity of
the retained state evolution.

### Uniform estimate and derivation

Since `E(t)<=E(T)` for `0<=t<=T`, define

```text
m_T = M_lo-E(T),
K_T = K_prep+epsilon*E(T),
F_T = [sqrt(c)+sqrt(K_T)]^2,
Q_T = 4*|g|*sqrt(mu*F_T)/m_T.
```

If `m_T>0`, the amplitude remains nonzero throughout the segment. The numerator
of the retained rate bound is bounded above using `F_T`, and its denominator
is bounded below using `m_T`. Hence

```text
Delta-Q_T <= nu(t) <= Delta+Q_T   for every rate time in [0,T].
```

If the native enclosure supplies a strictly positive common lower margin for
`Delta-Q_T`, it certifies positive rate throughout the segment. For an absolutely
continuous phase, this also gives

```text
gamma(t2)-gamma(t1) >= (Delta-Q_T)*(t2-t1), 0<=t1<t2<=T,
```

and an increasing inverse with Lipschitz constant at most `1/(Delta-Q_T)`.
The retained cycle endpoint is `T=2*pi/Delta=573049*pi`. Exact native endpoint
cells and receipt values belong in the successor results, rather than being
reconstructed from the old displayed decimals.

This argument establishes a uniform bound by applying the all-time form
inequality to monotone upper envelopes. It does not differentiate an
accumulated-phase envelope. It also does not calculate the signed later
correlator or change the interpretation of retained zero-containing endpoint
intervals in other lanes.

For interval implementation, an outer rectangular enclosure with positive
denominator is sufficient; a dependent enclosure may be sharper. Preserve the
same true lane parameters in the analytical statement and report the actual
native outer margin. These controls concern transcription and use of the
inherited inequality, not a rerun of its completed scientific campaign.

## 7. New weighted-field form lemma for centered propagation

The next signed-correlator question needs an unbounded-field comparison. The
following form estimate supplies an explicit constant for that development.

### Assumptions and statement

Work in the retained bosonic Fock realization with two independent real
polarizations and `H_f=dGamma(omega)` summed over them. The field convention is
`phi_a=a_a(u)+a_a^*(u)` as a quadratic form. Assume

```text
mu = integral |u(omega)|^2/omega d omega < infinity.
```

The source operator `S` is a self-adjoint unitary acting on the finite source
factor and commutes with `H_f`. In the dimensionless normalized chart set
`A=I+H_f`. Then `B=S*(phi_cross-i*phi_plus)` has a continuous form on
`Q(H_f)=D(H_f^(1/2))`, and

```text
||A^(-1/2)*B*A^(-1/2)|| <= sqrt(2*mu) = 1/sqrt(2R).
```

The displayed object is the bounded operator representing the weighted form;
an unweighted field operator on the entire Hilbert space is not assumed.

### Derivation

First use bounded-frequency smearings on a common finite-particle core. The
annihilation part of `phi_cross-i*phi_plus` combines two polarization
coefficients whose squared energy-weighted norm is `2*mu`. Its creation part
has a coefficient vector of the same weighted norm. The standard annihilation
energy inequality, which follows from Cauchy--Schwarz in the one-particle
frequency integral, gives for form-domain vectors `eta,xi`

```text
|<eta,B xi>|
 <= sqrt(2*mu) *
    [||eta||*||H_f^(1/2) xi|| + ||H_f^(1/2) eta||*||xi||]
 <= sqrt(2*mu)*||A^(1/2) eta||*||A^(1/2) xi||.
```

The last line is Cauchy--Schwarz for the two real vectors
`(||eta||,||H_f^(1/2)eta||)` and
`(||H_f^(1/2)xi||,||xi||)`. Moving `S` to the first vector changes neither norm,
because it is unitary and commutes with `H_f`.

Frequency-cutoff smearings converge in the `u/sqrt(omega)` norm. Applying the
same estimate to their differences makes their weighted forms Cauchy in
bounded-operator norm. The limit supplies the displayed form and constant on
`Q(H_f)`. Thus finite `mu`, rather than an unweighted `L2` norm of `u`, is the
ingredient used here. The logarithmically divergent unweighted ultraviolet
norm noted in the refinement manuscript does not enter this estimate.

For normalized `psi,chi` in `Q(H_f)`, expansion of their expectation difference
therefore gives

```text
|<B>_psi-<B>_chi|
 <= sqrt(2*mu)*||A^(1/2)(psi-chi)|| *
    [||A^(1/2)psi||+||A^(1/2)chi||].
```

Equivalently, if `A^(1/2)(rho-sigma)A^(1/2)` is well-defined and trace class,
the bound is `sqrt(2*mu)*||A^(1/2)(rho-sigma)A^(1/2)||_1`. These are form-domain
comparison statements. Propagating their right-hand sides is the next task.

## 8. Reference identification and the remaining signed-propagation result

The centered refinement defines

```text
h(t)=M*exp(-i*Omega*t),
w_h(t)=i*(Delta-Omega)*h(t)/(2*g),
r=dot(z)+i*Omega*z
 = -i*(Delta-Omega)*(z-h)+2*g*(w-w_h).
```

One explicit comparison construction is available once the retained hard
branches are carried into the same continuum form realization. Let `psi_0`
and `psi_1` be the exact hard charge-0/1 eigenbranches with energy difference
`Omega`, and orient the source lowering matrix element so that
`<psi_0|Z|psi_1>=2*M`. Charge selection eliminates the diagonal and reverse
matrix elements. Evolve their equal coherent superposition under the hard
Hamiltonian plus free soft Hamiltonian, with the soft vacuum and its scalar
counterterm retained. Call this comparison trajectory `chi(t)`.

Its source expectation is `h(t)`. Its soft field expectation vanishes. Applying
the same hard-field current identity to `chi(t)` then gives the full form
expectation `w_h(t)`. This identifies the algebraic reference when those branch,
domain, and realization hypotheses are fulfilled. Any alternative comparison
state with a different expectation carries an explicit mismatch payment.

Combining this identification with the weighted lemma would give

```text
W(t) <= sqrt(2*mu)*||A^(1/2)(psi(t)-chi(t))|| *
        [||A^(1/2)psi(t)||+||A^(1/2)chi(t)||]
        + reference_mismatch(t).
```

For `0<Omega<=Delta`, the retained centered sufficient condition is

```text
2*|g|*W(t)+Delta*E(t) < Omega*M.
```

The shared `Omega` and signed `g` remain in the exact identity before outer
bounding. A direct residual bound can retain still more cancellation.

The new work still needed is a rigorous propagated weighted distance or direct
signed-correlator/residual enclosure, with continuum and numerical error
payments, over a common time interval. The form lemma supplies its constant;
the coarse uniform theorem supplies an immediate lane-01 phase result. Neither
is an achieved later centered `W` calculation. The unresolved later signed
propagation for lanes 03, 13, and 23 remains the selected successor question.

## 9. Suggested Chapter I insertion

The worked example can be presented in six connected paragraphs: the placement
reference and chart normalization; the exact spectral lane; the complete lane
energy and action; the coherent hard-clock preparation; its signed initial
correlation; and the new uniform whole-cycle rate certificate with its native
margin. The spectral-weight controls and weighted-form derivation can remain
in the technical companion or appendix.

Keep the original Write/quantum action compatibility and the later centered
correlator propagation as explicit next derivations. The numerical successor
should report the exact source bindings and what actually executed through the
GEN6 Duck plugin, with its native receipts, separately from this mathematical
draft.
