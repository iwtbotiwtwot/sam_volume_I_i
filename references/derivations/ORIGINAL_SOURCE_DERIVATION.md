# From original Write incidence to six received clocks

This new calculation supplements the completed campaigns. It uses the supplied
manuscript as a mathematical source and the user's direct request as execution
authorization. The manuscript's proposed tasks are not independently promoted
to project instructions. All source assignments below retain their provenance.

## Source spectrum

The admitted source component consists of the four labelled cube paths with
codes 46501, 46525, 49061 and 81829. The original single-address Write rule flips
one of three address bits at one of seven occupied slots. The complete forbidden
single-hop boundary has 78 distinct target addresses. Its parallel signed
incidences form a 4 by 78 matrix B. Native multiplication reconstructs T=BB*:

```
84  8  8  0
 8 84  0  0
 8  0 84  8
 0  0  8 84
```

The signed response rule is d(s)=sum_e J_e(c_u-c_v) sigma_chi e_axis and
K=sum_axis D_axis T D_axis. The completed source supplies

```
 672   96    32    0
  96 2016     0    0
  32    0   672   32
   0    0    32  672
```

The construction and mapping are retained in
`SAM_MATTER_LEARNING/{generated_bridge.py,isotope_interaction.py}` and their
native implementations. The exact selected original response ledger is not
locally recovered. K is a retained completed operand, not a reverse-engineered
ledger. The signed-response species and exchange conventions keep their original
Codex exploratory receiving provenance.

Thus Q(g_H)=T+g_H K. Set x=q-(84+672g_H), a=8+96g_H,
b=8+32g_H and h=1344g_H. Its characteristic equation is

    x^4-h*x^3-(a^2+2*b^2)*x^2+2*h*b^2*x+a^2*b^2=0.

At the inherited unit-strength receiving value g_H=1, Q is

```
756  104   40    0
104 2100    0    0
 40    0  756   40
  0    0   40  756
```

The four q values are approximately 697.3304925912571,
752.0081836576553, 810.6543502862722 and 2108.0069734648155.
These decimals are displays. Native exact characteristic coefficients, disjoint
rational brackets, endpoint signs, derivative exclusion and interval Newton
certificates supply the mathematical inputs. The physical g_H remains an
explicit source assignment; setting its unit diagnostic value is not a
derivation of a physical coupling constant.

## Receiving scale from the Write capacity

The full pair Hamiltonian retains its even part:

    H_pair = Swap + Q tensor I + I tensor Q + Q tensor Q.

Equivalently the exchange increment is Swap-I relative to the identity
reference. Off-diagonal paired energies are q_a+q_b+q_a*q_b plus/minus1;
same-root unforced states have energy 1+2*q_a+q_a^2.

For the retained reference preparation |00>, the native reconstruction gives

    E_ref = 1 + 2*Q00 + Q00^2 = (1+756)^2 = 573049.

The original capacity source gives E_ref_phys=hbar*lambda_ref/t_SW with

    lambda_ref = (A0^2*k/2^n)/(1+(A0/2)*q/2^D).

For an action unit I_s and time unit t_u, matching this same preparation yields

    epsilon_R = (hbar/I_s)*(t_u/t_SW)*lambda_ref/E_ref.

This is the source-to-clock scale relation. The native numerical chart uses
I_s=hbar and t_u=t_SW/lambda_ref, giving epsilon_R=1/573049.
The reference preparation's capacity/role assignment must travel with a physical
conversion. No numerical SI value or lambda_ref=1 physical premise is inserted.

The original active-Write rate also gives the separately typed signed relation

    dot(phi_j)=s_j*c*(1-A)*D_j/R_H,
    dot(gamma)=c*(1-A)*(s_a*D_a+s_b*D_b-2*s_p*D_p)/R_H,
    epsilon_current=(t_u/2)*dot(gamma).

The common phase chi remains present. A signed, preparation-dependent current
cannot silently become a positive autonomous constant. R_H is the source sphere;
R below is the field boundary. Their equality requires a source incidence map.
Equating the scalar Write one-form to the occupied quantum source action would
require I_s*<G>*dot(gamma)=hbar*(dot(gamma)+3*dot(chi)); this is a derived
compatibility question, not an additional owner-imposed requirement.

## Receiving the spectrum through the full continuum

For each of the six pairs a<b, retain d_ab=q_a-q_b and g_ab=epsilon_R*d_ab.
The complete source retains its four unforced diagonal states and all even
energies. With kappa=4/5, the adopted boundary incidence gives

    |u_R(omega)|^2 = 2*omega*j2(omega*R)^2/(kappa*pi),
    J_ab(omega) = 2*g_ab^2*|u_R(omega)|^2,
    mu = 1/(4*R),  b = 1/(6*kappa*pi),  b3 = R/42,
    c_ab = 2*g_ab^2*mu = g_ab^2/(2*R).

The factor two retains both helicities. The operator interaction and both
counterterm payments remain those of the completed interacting action. No
rotating-wave or photon-number truncation is used. R is the exact retained
`samland_joint_response1/INPUT.json` radius. Coupling squares alone do not
replace the signed d and g in the interaction or clock correlations.

## Actual clocks for the retained preparation

Receive the completed equal coherent exact hard charge-0/1 preparation and full
soft vacuum, with split lambda=64*Delta and Delta=2*epsilon_R. The original
Gaussian trial expressions, explicit tails, branch isolation and occupation
bounds give certified intervals for the true hard gap Omega and matrix element
M. This native reconstruction is in `clock/DERIVATION.md` and its immutable
original and corrected graphs. The corrected supplement checks the positive
real interval and imaginary zero containment separately; the original typed
predicate failure is preserved.

For z=<D+i*C>/d and gamma=-arg(z), the exact autonomous identity is

    dot(z) = -i*Delta*z + 2*g*<S*(phi_cross-i*phi_plus)>,
    nu(t) = -Im(dot(z)/z).

At the specified initial preparation, z(0)=M>0, dot(z)(0)=-i*Omega*M,

    nu(0)=Omega,
    <S*phi_cross>_0=0,
    <S*phi_plus>_0=-(Delta-Omega)*M/(2*g).

Thus the lane rate is already shifted at time zero. The signed joint
correlation supplies that shift. Products of separately averaged source and
field means would lose it.

For later times, the full all-order soft-field phase envelope gives

    E(t)=exp(4*g^2*v_soft*t^2)-1,
    |gamma(t)-Omega*t| <= arcsin(E(t)/M_lower).

When E/M_lower<=1/2, the native bound arcsin(x)<=2*x is sufficient.
For endpoints a<b, retaining the same Omega at both endpoints gives

    mean_nu[a,b] in [Omega_lower-(delta(a)+delta(b))/(b-a),
                    Omega_upper+(delta(a)+delta(b))/(b-a)].

These are certified actual finite-interval clock rates. They are not later
pointwise evaluations. The exact signed-correlator identity governs pointwise
rates; differentiating a phase envelope would not compute that identity.
The independent verifier uses a different address reconstruction, exact Sturm
root counting and full hypergeometric Gaussian expressions.

## What the chain establishes and what travels as an input

The source chain derives T, the Q family, certified q, the reference denominator,
the normalized epsilon, signed six-lane couplings and received clock bounds.
The completed K, admitted four-placement component, physical g_H, reference
capacity assignment, boundary incidence and radius retain their source roles.
The resulting numerical clock table is reported in its explicit reference-time
chart. Physical inverse-seconds rates carry lambda_ref/t_SW as a factor. The
chain does not silently choose the remaining source assignments from its own
clock outputs.
