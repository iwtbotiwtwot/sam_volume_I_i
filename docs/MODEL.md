# Chapter I model and derivation

This document expands the mathematics of *Original Write histories and an
interacting source–field action*, Volume I, Chapter I. The chapter manuscript
is the publication draft; this page supplies a navigable account of its inputs,
derivations, and executable checks. It concerns Chapter I only.

The calculation receives three kinds of input:

| Layer | Input | Consequence developed here |
|---|---|---|
| Original source rules | Signed Writes, lifted phases, ordered histories, retained tensor map and source component | Phase incidence, signed action account, finite source operands |
| Receiving laws and assignments | Quadrupole bulk field, boundary incidence, quantization, unit-strength source chart, calibration and hard-field preparation | Complete joint Hamiltonian and a specified interacting evolution |
| Derived compositions | Exact source spectrum, lane decomposition, form estimates and native scalar enclosures | Six uniform actual phase clocks and one dependent phase-action coefficient family |

The source response ledger, physical exchange strength, reference capacity and
its role, Write time, and source-sphere/field-boundary incidence retain their
source assignments. The worked numerical chart assigns no rate in SI seconds.

## 1. Original lifted phases and action

For lifted phases \(\phi_a,\phi_b,\phi_p\), define

\[
\gamma_{\mathrm W}=\phi_a+\phi_b-2\phi_p,\qquad
\delta=\phi_a-\phi_b,\qquad\chi=\phi_p.
\]

The inverse incidence is

\[
\phi_a=(\gamma_{\mathrm W}+\delta)/2+\chi,\quad
\phi_b=(\gamma_{\mathrm W}-\delta)/2+\chi,\quad
\phi_p=\chi.
\]

On the legal piecewise active Write paths the original one-form is

\[
\omega_{\mathrm{Write}}=\hbar(d\gamma_{\mathrm W}+3d\chi).
\]

The retained tensor orientation is
\(\psi=\psi_0-\gamma_{\mathrm W}/2\). An ordered event word, a lifted
cumulative phase, and a wrapped endpoint preserve different information.
The original histories H02 and H03 reach the same endpoint with zero total
signed phase action and different positive durations. The interacting clock
\(\theta\) below is a separate coordinate from both \(\gamma_{\mathrm W}\)
and the original common phase \(\chi\).

## 2. Exact finite source

The source component retains placement codes `46501`, `46525`, `49061`, and
`81829`. A single-address Write flips one of three address bits at one of
seven occupied slots. The resulting forbidden single-hop boundary has 78
distinct target addresses. Its signed parallel incidence is a \(4\times78\)
matrix \(B\), with

\[
T=BB^*=\begin{pmatrix}
84&8&8&0\\8&84&0&0\\8&0&84&8\\0&0&8&84
\end{pmatrix},\qquad
K=\begin{pmatrix}
672&96&32&0\\96&2016&0&0\\32&0&672&32\\0&0&32&672
\end{pmatrix}.
\]

The retained signed response uses
\(d(s)=\sum_eJ_e(c_u-c_v)\sigma_\chi e_{\rm axis}\) and
\(K=\sum_{\rm axis}D_{\rm axis}TD_{\rm axis}\). The completed source
supplies \(K\); the exact selected response ledger is not reconstructed by
the public scalar code. Its provenance is preserved with the original source
records.

The source family is \(Q(g_H)=T+g_HK\). Put
\(x=q-(84+672g_H)\), \(a=8+96g_H\), \(b=8+32g_H\), and
\(h=1344g_H\). Its characteristic equation is

\[
x^4-hx^3-(a^2+2b^2)x^2+2hb^2x+a^2b^2=0.
\]

The worked chart receives \(g_H=1\), yielding

\[
Q=\begin{pmatrix}
756&104&40&0\\104&2100&0&0\\40&0&756&40\\0&0&40&756
\end{pmatrix},
\quad
p(x)=x^4-1344x^3-14016x^2+4300800x+17305600,
\quad x=q-756.
\]

The ordered roots are approximately

| Root | \(q_a\) |
|---|---:|
| 0 | 697.330492591257 |
| 1 | 752.008183657655 |
| 2 | 810.654350286272 |
| 3 | 2108.006973464815 |

Exact rational brackets and retained native certificates, rather than these
rounded displays, supply the interval calculation. The independent code also
computes a high-precision eigensystem and checks polynomial, trace, and moment
identities.

### Six lanes and the four unforced states

The complete source space is \(\mathbb C^4\otimes\mathbb C^4\). Write
\(Q_L=Q\otimes I\), \(Q_R=I\otimes Q\), and \(S=\mathrm{Swap}\). Then

\[
H_{\rm pair}=S+Q_L+Q_R+Q_LQ_R,\qquad
D=Q_L-Q_R,\qquad C=iSD.
\]

In the ordered two-state lane
\((|q_aq_b\rangle,|q_bq_a\rangle)\), \(a<b\), put
\(d_{ab}=q_a-q_b<0\) and \(e_{ab}=q_a+q_b+q_aq_b\). The restrictions are

\[
S=\sigma_x,\quad D=d_{ab}\sigma_z,\quad C=d_{ab}\sigma_y,\quad
H_{\rm pair}=e_{ab}I+\sigma_x.
\]

The six lane dimensions total twelve. The four diagonal states
\(|q_aq_a\rangle\) have \(D=C=0\) and energy \((1+q_a)^2\), completing
all sixteen source states. The sign of \(d_{ab}\) remains in the coupling
and clock equation even when energy bounds use its square.

With \(N_s=(I+S)/2\),
\(H_{\rm pair}=2N_s+K_{\rm pair}\), where
\(K_{\rm pair}=Q_L+Q_R+Q_LQ_R-I\). This commuting even operator is scalar
within a lane and varies across the full source. It is distinct from the
independent original phase \(\chi\). The earlier full18 tensor map and its
retained complement are also distinct from this sixteen-state source action.

## 3. Calibration is an expectation and a declared time chart

The placement-basis calibration state \(|e_0e_0\rangle\) gives

\[
E_{\rm ref}=\langle H_{\rm pair}\rangle=(1+Q_{00})^2=573049.
\]

This is an expectation. Its source-energy variance is `14384109824`. Its
spectral weights can be reconstructed from the resolvent cofactor:

\[
p_a=\frac{(x_a-1344)(x_a^2-1600)}{p'(x_a)},\qquad
\sum_ap_a=1,\quad\sum_ap_aq_a=756,\quad\sum_ap_aq_a^2=583952.
\]

The diagonal populations \(p_a^2\) and pair populations \(2p_ap_b\)
reconstruct the same energy expectation. The original pure-state density
retains its coherences. Its zero current expectations do not make it the
coherent interacting clock preparation used below.

For action unit \(I_*\), physical time unit \(t_u\), Write time
\(t_{\rm SW}\), and reference capacity \(\lambda_{\rm ref}\),

\[
\epsilon=\frac{\hbar}{I_*}\frac{t_u}{t_{\rm SW}}
\frac{\lambda_{\rm ref}}{E_{\rm ref}}.
\]

The receiving chart \(I_*=\hbar\),
\(t_u=t_{\rm SW}/\lambda_{\rm ref}\) gives
\(\epsilon=1/573049\), \(\Delta=2\epsilon\), and
\(\tau=t_{\rm phys}/t_u\). A model angular rate \(\nu\) converts
conditionally to \((\lambda_{\rm ref}/t_{\rm SW})\nu\).

## 4. Complete field and joint action

The two-polarization quadrupole receiving field has Lagrangian

\[
L_f=\frac\kappa4\sum_{\alpha=+,\times}\int_0^\infty dr\,
\left(r^2\dot\varphi_\alpha^2-r^2(\partial_r\varphi_\alpha)^2
-6\varphi_\alpha^2\right).
\]

For boundary coordinate \(x=R\varphi(R)\), the regular static interior and
exterior are \(xr^2/R^3\) and \(xR^2/r^3\). Their radial energy integrals
are \(2x^2/R\) and \(3x^2/R\). Matching the literal tensor metric
\(B_{\rm TT}=2I_2\) fixes \(5\kappa/4=1\), hence \(\kappa=4/5\).
The boundary jump retains the orientation

\[
[\partial_r\varphi_\alpha]_{R^-}^{R^+}
=-\frac{2\epsilon J_\alpha}{\kappa R^2},\qquad J_+=D,\ J_\times=C.
\]

The retained radius is \(R\simeq0.163544171326059\). With real smearing
\(u_R(\omega)=\sqrt{2\omega/(\kappa\pi)}j_2(\omega R)\),

\[
|u_R(\omega)|^2=\frac{2\omega j_2(\omega R)^2}{\kappa\pi},\qquad
\mu=\int_0^\infty\frac{|u_R(\omega)|^2}{\omega}\,d\omega
=\frac1{4R}.
\]

On the full source times bosonic Fock space,

\[
H=\epsilon H_{\rm pair}+H_f-\epsilon(D\phi_++C\phi_\times)
+\epsilon^2\mu(D^2+C^2).
\]

Both real polarizations and both counterterms are retained. On a lane,
\(g=\epsilon d_{ab}<0\), \(e=e_{ab}\), and

\[
H=\epsilon eI+\epsilon S+K,\quad
K=H_f-g(\sigma_z\phi_++\sigma_y\phi_\times)+cI,\quad
c=2g^2\mu=\frac{g^2}{2R}.
\]

The positive square form defining \(K\) is the sum over polarizations of

\[
\int_0^\infty d\omega\left\|
\sqrt\omega a_\alpha(\omega)\Psi
-\frac{g\sigma_\alpha u_R^*(\omega)}{\sqrt\omega}\Psi
\right\|^2,
\quad\sigma_+=\sigma_z,\quad\sigma_\times=\sigma_y.
\]

The two source shifts need not commute. Each counterterm contributes
\(g^2/(4R)\). All four circular interaction words preserve the signed
charge \(Q_{\rm ch}=N_s+N_+-N_-\), with tensor angular action
\(2I_*Q_{\rm ch}\). All field frequencies and photon sectors remain in the
receiving law.

### Continuum form domain and regularity

Let \(H_f=d\Gamma(\omega)\), \(A=I+H_f\), and
\(Q_f=D(H_f^{1/2})\). The weighted annihilation estimate is

\[
\|a_\alpha(u_R)\eta\|\le\sqrt\mu\,
\|H_{f,\alpha}^{1/2}\eta\|.
\]

Frequency-cutoff approximations converge in this weighted norm. Creation is
defined by adjoint form pairing. This constructs the field on \(Q_f\) even
though its full unweighted smearing norm is ultraviolet divergent. For a
bounded source current, Young's inequality makes the interaction infinitesimally
bounded relative to the free energy form. The form-sum theorem therefore
defines a closed semibounded self-adjoint Hamiltonian with form domain \(Q_f\).

Bounded source observables and their adjoints preserve \(Q_f\). The evolution
is continuous in its energy norm and differentiable in \(Q_f^*\); taking the
expectation difference quotient in this dual pairing gives the continuous
form Ehrenfest equation. These analytical steps establish the regularity used
by the instantaneous clock. The numerical scripts check the scalar and finite
matrix consequences of that argument.

## 5. Actual clock and matched hard reference

On a fixed lane, define

\[
Z=(D+iC)/d=\sigma_z+i\sigma_y,\quad z=\langle Z\rangle,\quad
w=\langle S(\phi_\times-i\phi_+)\rangle.
\]

The exact joint equation and rate are

\[
\dot z=-i\Delta z+2gw,\qquad
\theta=-\arg z,\qquad\nu=\dot\theta=-\operatorname{Im}(\dot z/z).
\]

Choose the split \(\lambda=64\Delta\) and the declared preparation

\[
\Psi_0=\frac{\Phi_0+\Phi_1}{\sqrt2}\otimes|0_s\rangle.
\]

The exact normalized interacting hard-field eigenbranches \(\Phi_0,\Phi_1\)
have signed charges zero and one. Their gap is \(\Omega>0\); the relative
phase gives \(\langle\Phi_0|Z|\Phi_1\rangle=2M>0\). The reference
Hamiltonian contains the same hard interaction, free soft field, even scalar,
and exact soft scalar counterterm as the actual Hamiltonian. Both evolutions
start at the same vector, in the same field realization and common phase.
Charge selection gives the actual reference expectations

\[
h=Me^{-i\Omega\tau},\qquad
w_h=\frac{i(\Delta-\Omega)}{2g}h.
\]

Consequently \(z(0)=M\), \(\nu(0)=\Omega\),
\(\langle S\phi_\times\rangle_0=0\), and
\(\langle S\phi_+\rangle_0=-(\Delta-\Omega)M/(2g)>0\).
The correlation in this equation is a joint expectation.

### Propagated centered-correlator estimate

The retained soft and energy estimates are

\[
v_s\le v_s^{\rm up}=\frac{R^4\lambda^6}{675\kappa\pi},\quad
E(\tau)=e^{4g^2v_s^{\rm up}\tau^2}-1,\quad
|z-h|\le E(\tau),
\]

\[
F_T=\left(\sqrt c+\sqrt{K_{\rm prep}+\epsilon E(T)}\right)^2.
\]

Here \(K_{\rm prep}\) bounds the positive block in the exact preparation,
including the full soft counterterm. Both actual and reference free energies
are at most \(F_T\) over \([0,T]\).

The square form gives \(H_f\le2K+2cI\) and \(K\le2H_f+2cI\). With
\(B_0=\epsilon S+K+(\epsilon+c+1/2)I\), the checked scalar condition
\(2\epsilon+3c+1/2\le2\) implies
\(A\le2B_0\le4A\). Conservation of the \(B_0\) form norm therefore gives

\[
\|A^{1/2}e^{-i\tau H}\eta\|\le2\|A^{1/2}\eta\|.
\]

For \(B=S(\phi_\times-i\phi_+)\), the weighted pairing satisfies
\(\|A^{-1/2}BA^{-1/2}\|\le\sqrt{2\mu}\). The difference
\(V_s=H-H_{\rm ref}\) is the soft interaction, since the exact common soft
counterterm cancels. On the reference vacuum it creates orthogonal soft
one-photon insertions. As
\(\int_0^\lambda\omega|u_R|^2d\omega\le\lambda v_s\),

\[
\|A^{1/2}V_s\Psi_{\rm ref}(\tau)\|^2
\le2g^2v_s^{\rm up}(1+F_T+\lambda).
\]

The reference is a finite sum of hard eigenvectors times soft vacuum. Its
forcing belongs continuously to \(Q_f\). The Hilbert-space Duhamel identity
is therefore also a Bochner integral in the energy form norm; the preceding
propagation estimate yields

\[
\|A^{1/2}(\Psi-\Psi_{\rm ref})\|
\le2T\sqrt{2g^2v_s^{\rm up}(1+F_T+\lambda)}.
\]

Expanding the two weighted \(B\) expectations gives the achieved bound

\[
\sup_{0\le\tau\le T}|w-w_h|\le W_D(T),\qquad
W_D(T)=8|g|T\sqrt{\mu v_s^{\rm up}(1+F_T)(1+F_T+\lambda)}.
\]

The full propagator in this identity retains all photon sectors. The
one-photon forcing is a property of applying the soft interaction to the
reference vacuum.

### Uniform rates

Writing \(\delta z=z-h\) and \(\delta w=w-w_h\) gives

\[
\dot z+i\Omega z=-i(\Delta-\Omega)\delta z+2g\delta w.
\]

For \(0<\Omega\le\Delta\) and \(E(T)<M\),

\[
|\nu-\Omega|\le
\frac{(\Delta-\Omega)E(T)+2|g|W_D(T)}{M-E(T)}.
\]

The sufficient positive-rate condition is
\(2|g|W_D(T)+\Delta E(T)<\Omega M\), using the same true parameters
throughout. Native outer evaluation verifies the amplitude, positivity, and
upper-rate conditions in every separately prepared lane for
\(0\le\tau\le T_0=2\pi/\Delta=573049\pi\).

| Lane | Lower \(10^6\nu\) | Upper \(10^6\nu\) |
|---|---:|---:|
| 01 | 3.490102929541 | 3.490102934505 |
| 02 | 3.490102893142 | 3.490102914462 |
| 03 | 3.490095588823 | 3.490098892473 |
| 12 | 3.490102927880 | 3.490102933590 |
| 13 | 3.490096147687 | 3.490099200196 |
| 23 | 3.490096722560 | 3.490099516734 |

These are outward-rounded displays of the exact retained rational outer
endpoints. Every upper endpoint is below
\(10^6\Delta\simeq3.49010294058623\). A certified lower rate \(\ell>0\)
gives \(\theta(\tau_2)-\theta(\tau_1)\ge\ell(\tau_2-\tau_1)\), so
the inverse is continuously differentiable and Lipschitz with constant at
most \(1/\ell\) on the phase image.

## 6. The complete action in clock phase

The joint-state action is

\[
\mathcal S=I_*\int d\tau\,[\mathcal B_\tau-\langle H\rangle],\qquad
\mathcal B_\tau=\frac i2
(\langle\Psi|\dot\Psi\rangle-\langle\dot\Psi|\Psi\rangle).
\]

The continuum pairing uses \(Q_f\) and \(Q_f^*\). Positive \(\nu\)
allows \(d\tau=d\theta/\nu\). Since
\(\dot\varphi=\nu\partial_\theta\varphi\), the complete coefficient
family is

| Contribution | Coefficient inside \(\mathcal S/I_*\) |
|---|---:|
| Field kinetic | \(\nu/5\) |
| Field radial gradient | \(-1/(5\nu)\) |
| Field angular term | \(-6/(5\nu)\) |
| Even source energy | \(-\epsilon e/\nu\) |
| Source exchange | \(-\epsilon/\nu\) |
| Boundary coupling | \(+g/\nu\) |
| Both counterterms | \(-c/\nu\) |

The Berry one-form remains
\(\tfrac i2(\langle\Psi|d\Psi\rangle-\langle d\Psi|\Psi\rangle)\).
All coefficients are dependent images of the same actual rate. The even
energy and full counterterm remain in the action even though they commute
with \(Z\) and drop out of its clock equation. The local inverse \(1/\nu\)
and finite-window mean inverse \(\tau/\theta(\tau)\) retain their distinct
roles.

The completed result supplies the source-to-clock argument for the declared
receiving law and preparation. **The test result suggests strong contact with
the concept.** The occupied-path relation of the original one-form to the
quantum generator remains the next source interface, carrying the original
common phase, commuting even operator, and preparation class. It is identified
in Chapter I's conclusion; no later chapter is included here.

For commands, verification levels, and evidence locations, see
[REPRODUCIBILITY.md](REPRODUCIBILITY.md) and
[PROVENANCE.md](PROVENANCE.md).
