# Form realization and the exact continuously differentiable lane clock

Date: 2026-10-15. Status: new analytical supplement to
`DERIVATION_DRAFT.md`. The draft is preserved byte for byte because an executed
native job binds its hash. This supplement develops the receiving Hamiltonian's
form realization and the regularity needed by the uniform clock statement. It
introduces no numerical scientific result and starts no job.

ORIGINATOR / CONCEPTUAL DIRECTOR: Sean Brady.

AI RESEARCH COLLABORATORS: OpenAI ChatGPT and Codex.

The arguments here are Codex mathematical contributions for the authorized
Chapter I successor. They concern the specified receiving law and its declared
initial preparation. A propagated centered-correlator error is a separate
remaining calculation.

## 1. The full sixteen-state source and continuum form

Let `h_s=C^4 tensor C^4` be the complete source space and `F` the bosonic Fock
space over the two-polarization one-particle space
`L2((0,infinity),d omega; C^2)`. On `H=h_s tensor F`, let

```text
Q_L=Q tensor I,  Q_R=I tensor Q,
S=Swap,
H_pair=S+Q_L+Q_R+Q_L*Q_R,
D=Q_L-Q_R,
C=i*S*D,
H_f=I_source tensor dGamma(omega),
A=I+H_f,
Q_f=D(H_f^(1/2)).
```

Here `I_source` denotes the identity on the source factor. All source matrices are finite dimensional;
`H_pair,D,C` are bounded and self-adjoint. The form domain `Q_f` includes every
source sector, every field frequency, and every photon sector.

For each real polarization use the receiving convention
`phi_a=a_a(u_R)+a_a^*(u_R)` as a form. The needed source-kernel norm is

```text
mu=integral_0^infinity |u_R(omega)|^2/omega d omega < infinity.
```

For the retained quadrupole kernel this is the inherited `mu=1/(4R)`. An
unweighted `L2` norm of `u_R` is not assumed. The full Hamiltonian is defined
by the following symmetric sesquilinear form on `Q_f`:

```text
q_H = q_f + epsilon*H_pair
      - epsilon*(D*phi_plus+C*phi_cross)
      + epsilon^2*mu*(D^2+C^2).
```

Finite source terms in this notation denote their bounded forms. On a lane
`a<b`, the source restrictions are

```text
S=sigma_x, D=d_ab*sigma_z, C=d_ab*sigma_y,
H_pair=e_ab*I+sigma_x,
d_ab=q_a-q_b, e_ab=q_a+q_b+q_a*q_b,
g_ab=epsilon*d_ab.
```

Thus the counterterm restricts to `2*g_ab^2*mu` and the form restricts to the
complete lane Hamiltonian in the draft. On each spectral diagonal state
`|q_a q_a>`, both currents vanish and the retained source energy is
`epsilon*(1+2*q_a+q_a^2)`.

The six lane projectors and four diagonal projectors commute with these source
operators and with the full form. A coherent placement preparation may retain
cross-sector coherences; its spectral weights do not replace those coherences.
The commuting even source operator is scalar within a lane, but is not one
global scalar over all sixteen source states. It remains distinct from the
independent original lifted common phase `chi`.

## 2. Weighted annihilation construction over the complete kernel

For a regular compact-frequency smearing `f`, Cauchy--Schwarz in the annihilation
integral and summation over the symmetric Fock sectors give

```text
||a_a(f) psi||^2
 <= [integral |f(omega)|^2/omega d omega]
    *||H_(f,a)^(1/2) psi||^2.
```

One direct derivation on the finite-particle core is to insert the factors
`f/sqrt(omega)` and `sqrt(omega)*psi_n` in the annihilation integral. The factor
`n` in its squared norm becomes the sum of the `n` identical frequency-energy
integrals by permutation symmetry. Summing those integrals gives the displayed
field energy. No positive lower bound on `omega` enters this calculation.

Choose nested frequency cutoffs
`u_n=u_R*1_[1/n,n]`. Each `u_n` is unweighted `L2`, because
`integral_[1/n,n]|u_R|^2 <= n*mu`. Moreover,

```text
integral |u_n-u_R|^2/omega -> 0.
```

The annihilation estimate therefore makes `a_a(u_n)` Cauchy as continuous maps
from `Q_f`, with its `A^(1/2)` norm, into `H`. Its limit defines `a_a(u_R)` on
that form domain and retains the sharper energy estimate

```text
||a_a(u_R) psi|| <= sqrt(mu)*||H_(f,a)^(1/2) psi||.
```

Define the creation term by the adjoint pairing from `H` to the form dual
`Q_f^*`. The field pairing on `Q_f` is then the sum of annihilation and creation
pairings. This construction does not assert an ordinary creation operator
`a^*(u_R):H->H` for a non-normalizable smearing.

For bounded self-adjoint source `J` commuting with the field, the diagonal form
estimate is

```text
|q_(J phi_a)(psi,psi)|
 <= 2*sqrt(mu)*||J psi||*||H_(f,a)^(1/2) psi||.
```

The estimate follows by moving `J` to the first vector and combining the two
adjoint pairings. It extends from the regular cutoff core to `Q_f` by the
weighted convergence just constructed.

## 3. Closed semibounded full Hamiltonian

Let

```text
L=|epsilon|*sqrt(mu*(||D||^2+||C||^2)).
```

The two-polarization interaction form obeys

```text
|q_V(psi,psi)|
 <= 2*L*||psi||*||H_f^(1/2)psi||
 <= eta*q_f(psi,psi)+(L^2/eta)*||psi||^2
```

for every `eta>0`. The first inequality uses Cauchy--Schwarz over the two
polarizations. The second is the elementary inequality `2ab<=eta*a^2+b^2/eta`.
Thus the interaction is infinitesimally bounded relative to the free-field
form. The source Hamiltonian and the counterterm are bounded forms.

Applying the KLMN form-sum theorem with any chosen `eta<1` gives a closed,
semibounded form `q_H` on precisely `Q_f`. Its representation theorem defines
a unique semibounded self-adjoint Hamiltonian `H` for this receiving law. In
particular, for a sufficiently large finite shift `beta`,

```text
H+beta >= I,
D((H+beta)^(1/2))=Q_f,
|| (H+beta)^(1/2) psi || and || A^(1/2) psi ||
are equivalent norms on Q_f.
```

The relative bound is zero, so this argument does not require a small-coupling
restriction. It does not identify the operator domain `D(H)` with `D(H_f)`;
the form domain is the one used below.

The same weighted-kernel convergence makes the cutoff interaction forms
converge in the norm of continuous forms on `Q_f`. The cutoff counterterms
converge to `epsilon^2*mu*(D^2+C^2)` because their scalar weighted norms converge
to `mu`. This specifies the continuum form directly; the cutoffs are a
construction of its limit rather than a photon cutoff or a modified receiving
law.

The positive square completion for the field/interaction/counterterm block
can also be read in this form sense. In each polarization it is the squared
norm of the direct-integral annihilation map shifted by
`epsilon*J_a*u_R^*/sqrt(omega)`. Both maps act from `Q_f` to that energy-weighted
direct-integral Hilbert space. The resulting block is nonnegative and retains
both counterterms. No commutativity of `D` and `C`, or simultaneous shifted
vacuum, is used.

## 4. Form Ehrenfest identity for bounded source observables

Let `Z` be a bounded operator acting only on the finite source factor. It and
`Z^*` preserve `Q_f`, since they commute with `H_f` and satisfy

```text
||A^(1/2) Z psi|| <= ||Z||*||A^(1/2) psi||.
```

For a normalized initial vector `psi_0 in Q_f`, set
`psi(t)=exp(-itH)psi_0`. The spectral theorem implies that this evolution
preserves `D((H+beta)^(1/2))` and is continuous in that form norm. By norm
equivalence, it is continuous in the `A^(1/2)` norm as well.

The dual-space derivative exists:

```text
[exp(-ihH)-I]*psi/h -> -i*H*psi in Q_f^* as h->0,
```

where `H` on the right is the continuous form map `Q_f->Q_f^*`. To see the
limit, use the spectral resolution of `H`. The scalar difference quotient
converges pointwise, and its squared error divided by the positive energy
weight `lambda+beta` is bounded by a constant times `lambda+beta`. That weight
is integrable for `psi in D((H+beta)^(1/2))`; dominated convergence applies.

Take the difference quotient of `z(t)=<psi(t),Z psi(t)>` and pair it in
`Q_f^* x Q_f`. With the inner product antilinear in its first entry and linear
in its second, the limit is

```text
dot(z)(t)=i*[q_H(psi(t),Z psi(t))-q_H(Z^*psi(t),psi(t))].
```

Both terms are continuous in `t` because the form and `Z,Z^*` are continuous
on `Q_f`. Thus `z` is continuously differentiable for every form-domain initial
vector. This statement needs neither `psi_0 in D(H)` nor a finite equal-time
field second moment.

## 5. Exact lane equation in the form realization

Fix one spectral lane and its normalized preparation. On that lane use

```text
Z=sigma_z+i*sigma_y,
B=S*(phi_cross-i*phi_plus),
z(t)=<Z>_t, w(t)=q_B(psi(t),psi(t)),
Delta=2*epsilon, g=epsilon*d.
```

The bounded source term and the two interaction commutators are

```text
i*[epsilon*S,Z]=-i*Delta*Z,
i*[-g*sigma_z*phi_plus,Z]=-2i*g*S*phi_plus,
i*[-g*sigma_y*phi_cross,Z]=2*g*S*phi_cross.
```

The free field, lane even scalar, and lane counterterm commute with `Z`.
These identities can first be evaluated on the regular cutoff core. Their
forms converge uniformly on bounded subsets of `Q_f` because
`u_n/sqrt(omega)` converges in `L2` and `Z,Z^*` preserve `Q_f`. The form
Ehrenfest identity consequently gives the exact continuum equation

```text
dot(z)=-i*Delta*z+2*g*w
```

at every time. The expectation `w(t)` is a continuous field form expectation.
Neither a factorization of joint expectations nor an unweighted field
operator norm is used.

For reference, the complete complex field form has the weighted bound

```text
||A^(-1/2)*B*A^(-1/2)|| <= sqrt(2*mu).
```

This is the lemma developed in the draft: the annihilation coefficient vector
and the creation coefficient vector each have squared energy-weighted norm
`2*mu`, and their two bilinear estimates combine by Cauchy--Schwarz. It also
supplies continuity of the commutator term just used.

## 6. Phase existence and the uniform pointwise theorem

Suppose the inherited all-time amplitude bound and successor native margin
give `|z(t)|>=m_T>0` for `0<=t<=T`. Since `z` is `C1`, it has a unique `C1`
argument lift fixed by the declared initial orientation `z(0)=M>0`. Explicitly,

```text
gamma(0)=0,
gamma(t)=-integral_0^t Im(dot(z)(s)/z(s)) ds,
z(t)/|z(t)|=exp(-i*gamma(t)),
nu(t)=dot(gamma)(t)=-Im(dot(z)(t)/z(t)).
```

The rate is continuous. Therefore the uniform energy/amplitude inequality in
the draft applies pointwise at every time under this form realization, rather
than only at almost every time.

The preparation in use meets the initial form-domain hypothesis: each retained
exact hard branch is a finite-energy eigenstate of the corresponding closed
hard form, whose form norm is equivalent to the hard free-energy norm. Its
product with the soft vacuum lies in `Q_f`; so does the equal coherent branch
superposition. This is the declared interacting clock preparation. It is
distinct from the labelled placement reference, whose lane current vanishes.

All energy bounds remain in the original normalized model time. In particular,
the supplied remainder and source-energy relation are all-time statements:

```text
E(t)=exp(4*g^2*v_soft*t^2)-1,
K(t)<=K_prep+epsilon*E(t),
E_free(t)<=[sqrt(c)+sqrt(K_prep+epsilon*E(t))]^2.
```

The energy relation also follows from form-energy conservation under the
autonomous Hamiltonian and the retained source-expectation error. The hard
reference has a constant source `S` expectation; the actual source expectation
differs from it by at most `E(t)`. The lane even energy is constant and remains
in the conserved total energy.

Because `E(t)` increases for `t>=0`, the endpoint numerator bound and positive
amplitude denominator from the draft bound the rate on the entire segment.
If its native lower margin is `L_T>0`, then

```text
nu(t)>=L_T>0 on [0,T].
```

The phase is strictly increasing, and its inverse on the phase image is `C1`
with derivative `1/nu`. Reparameterizing the full action is then valid using
`d tau=d gamma/nu`. The receiving coefficients `epsilon,g,R` remain fixed;
retiming does not replace them by the actual rate or by an original signed
active-Write current. Every energy term uses the same actual rate, and the
joint Berry one-form is unchanged. No derivative of an accumulated-phase
error envelope enters this conclusion.

## 7. Scope and remaining centered estimate

The argument specifies the full two-polarization continuum form for the given
finite source, supplies its self-adjoint time evolution, and establishes the
exact continuously differentiable lane clock for form-domain initial states.
Together with the inherited all-time bounds and the actual native margins,
it supports the uniform pointwise interpretation used in the Chapter I
successor.

The original source incidence, physical coupling/time assignments, and capacity
reference keep their existing provenance. This supplement does not select
them from the clock output. It also does not supply a small propagated
weighted difference between the actual trajectory and the hard-reference
trajectory. An achieved `W(t)=|w(t)-w_h(t)|` or direct residual enclosure, with
its continuum and numerical error payments, remains the selected new
correlator calculation.

## 8. Method reference and provenance

The form-domain argument above is self-contained apart from the standard KLMN
form-sum and representation theorems. A primary paper illustrating weighted
annihilation/creation maps and singular field forms is Davide Lonigro,
*Generalized spin-boson models with non-normalizable form factors*, Journal of
Mathematical Physics 63, 072105 (2022),
[arXiv:2111.06121v2](https://arxiv.org/abs/2111.06121v2), especially Sections 3--4.
That paper assumes a positive one-particle mass gap in its stated setup. The
massless two-polarization statement here uses the explicit weighted estimate
and form construction above; its mass-gap hypotheses are not imported.

The receiving law, finite source, exact hard preparation, and all-time energy
inequalities are inherited from these project-relative sources:

- `GEN4/duck_write_coupling_clock1_20261015/DERIVATION.md`.
- `GEN4/duck_write_coupling_clock1_20261015/clock/DERIVATION.md`.
- `GEN4/duck_write_coupling_clock1_20261015/clock/POINTWISE_DERIVATION.md`.
- `GEN4/samland_resolved_clock1/DERIVATION.md`, Sections 1--5.
- `GEN4/duck_chapter1_lane1_20261015/derivation/DERIVATION_DRAFT.md`.

Native numbers and execution custody belong to this successor's results and
receipts. This analytical supplement changes no completed source artifact.
