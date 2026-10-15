# A resolved interacting source clock in the full tensor law

This is the next SAM_land construction after H002466. It uses the same autonomous Hamiltonian and a new, declared preparation. Its result is an interval for the exact stationary source gap and an all-orders bound for the actual source and complete receiver after the entire low-frequency field is coupled. The preparation parameter is lambda=64Delta. Both frequency pieces remain in the final Hamiltonian.

## 1. Retained source, interaction and references

The original16-dimensional pair source has six unequal-root two-state lanes and four unforced diagonal states. On each lane, the full matrices reduce exactly to

\[
H_{ab}=e_{ab}+\epsilon S+H_f-g(\sigma_x\phi_++\sigma_y\phi_\times)+2g^2\mu,
\quad S=\operatorname{diag}(-1,1),\quad\Delta=2\epsilon.
\]

Here g=epsilon d_ab is signed, e_ab=epsilon(q_a+q_b+q_aq_b), kappa=4/5, propagation speed=1 and mu=1/(4R). The original real D and C=iSD currents, the complete18/68 common metric and all54 background/constituent references are inherited through the parent root and frozen input map. D²=C² commutes with the whole Hamiltonian. H_pair−S commutes with both currents; the even energy is carried before the lane reduction. The four unforced channels remain in the full source structure.

The source form factor and complete radial norms are

\[
|u_R(\omega)|^2=\frac{2\omega j_2(\omega R)^2}{\kappa\pi},\qquad
\mu=\int_0^\infty\frac{|u_R|^2}{\omega}d\omega=\frac1{4R},
\]
\[
b=\int_0^\infty\frac{|u_R|^2}{\omega^2}d\omega=\frac1{6\kappa\pi},\qquad
b_3=\int_0^\infty\frac{|u_R|^2}{\omega^3}d\omega=\frac{2R}{105\kappa}=\frac R{42}.
\]

The independent checker obtains these full norms from the [NIST Bessel-product Mellin identity](https://dlmf.nist.gov/10.22.E57). The global inequality |j2(x)|≤x²/15 follows from its [complete integral representation](https://dlmf.nist.gov/10.54.E1), with real x. These identities give bounds over the entire retained continuum.

Both helicities and counterrotating terms are retained. The signed conserved charge is

\[
Q=N_s+N_+-N_-,\qquad N_s=(1+S)/2,
\]

with tensor angular action2I_s Q. The microscopic source angle is the inherited half-angle of the tensor carrier plane. Whole source/field/interaction/counterterm energy and signed action use the original chart. FIXED holds epsilon/g/e_ab fixed; CODILATED scales the whole source by R0/R. All six incidence/radius cases remain, with six conditional lanes of weight1/6.

## 2. New preparation and exact infinite-field branch existence

Split at lambda=64Delta. For omega≥lambda let mu_h and b_h be the exact hard norms, and

\[
K_h=H_{f,h}-g(\sigma_x\phi_{+,h}+\sigma_y\phi_{\times,h})+2g^2\mu_h\ge0,
\qquad H_h(v)=K_h+vS,
\quad |v|\le\epsilon.
\]

The usual annihilation-operator form estimate gives, for hard free-field energy E_f,

\[
\langle K_h\rangle\ge(\sqrt{E_f}-\sqrt{c_h})^2,
\qquad c_h=2g^2\mu_h\le c=2g^2\mu.
\]

On the complement of source×hard vacuum, E_f≥lambda. Since lambda>c,

\[
B_{\rm sep}=(\sqrt\lambda-\sqrt c)^2
\]

is a lower form bound there. Native arithmetic verifies B_sep>c+2epsilon in every lane. Each of the two source-vacuum trial vectors has energy≤c+epsilon, below the complement bound B_sep−epsilon. The minmax principle therefore gives exactly two discrete states below that bound in the complete hard Fock space. There is one in charge0 and one in charge1: each charge sector has one source-vacuum direction, and the same complement bound applies. This argument establishes existence and isolation without a photon-number basis cut.

At v=0, source reversal sigma_x followed by complex conjugation, with the corresponding helicity interchange, preserves K_h and exchanges charge0/1. The two branch energies agree there. They remain isolated in their separate charges throughout [−epsilon,epsilon]. Bounded vS perturbation implies that either branch lies at most Delta above the global bottom.

Let Phi0/Phi1 be these exact branches at v=epsilon, with energies E0/E1. Their phases are chosen so the source transition overlap M is positive. The declared preparation is

\[
\Psi_{\rm prep}=\frac{\Phi_0+\Phi_1}{\sqrt2}\otimes|0_{\rm soft}\rangle.
\]

The full soft field0≤omega<lambda is in its common relative vacuum initially and is then coupled by the unchanged full autonomous law. Selecting these exact branches is the new preparation specification. A finite microscopic actuator for it is the named next recipient.

## 3. Pull-through bounds and a strictly slower exact gap

For a charge0 branch let n be its source excitation probability. Exact charge gives n=⟨N_-−N_+⟩. The complete circular-field pull-through identities are

\[
a_+\Phi=\sqrt2g\,u_R(H_h-E+\omega)^{-1}\sigma_-\Phi,
\qquad
a_-\Phi=\sqrt2g\,u_R(H_h-E+\omega)^{-1}\sigma_+\Phi.
\]

Since H_h−E≥−Delta and omega≥lambda,

\[
A=\frac{2g^2b}{(1-\Delta/\lambda)^2},\qquad
\langle N_-\rangle\le A(1-n),\quad\langle N_+\rangle\le An,
\qquad n\le n_+=\frac A{1+A}.
\]

The full soft norms are bounded by

\[
v_s\le\frac{R^4\lambda^6}{675\kappa\pi},\quad
\mu_s\le\frac{2R^4\lambda^5}{1125\kappa\pi},\quad
b_s\le\frac{R^4\lambda^4}{450\kappa\pi},\quad b_h\in[b-b_s,b].
\]

Use H002466's complete two-quadrature Gaussian joint unitary only as a variational trial on the hard field. If a=g²b_h,

\[
B={}_1F_1(1;3/2;-2a),\quad Z_h=1-4aB,\quad
C_f={}_2F_2(1,1;3/2,2;-2a).
\]

Its actual hard K cost is delta_h=mu_h g²(1+C_f−2B). Native arithmetic uses mu in place of mu_h, and then its outward upper endpoint, as a conservative ceiling delta_bar. The retained field named `hard_Gaussian_trial_positive_K` is this full-mu envelope; `hard_trial_K_ceiling` is the paid ceiling used by the proof. It does not claim an exact hard preparation-energy value. The independent check integrates the complete soft mu and b and verifies the actual trial energy is positive and below delta_bar.

For any v in the branch path, the variational trial and Hellmann-Feynman source expectation imply

\[
K_{\rm up}=\bar\delta+\epsilon(1-Z_{h,\rm low}+2n_+),\quad
E_{f,\rm up}=(\sqrt c+\sqrt{K_{\rm up}})^2,
\quad L=\frac{E_{f,\rm up}}{1-n_+}+c+\Delta.
\]

L bounds the spectral mean of H_h−E in the normalized source-raised branch. The source-flipped interaction expectation vanishes; its free-field contribution is bounded by E_f/(1−n), its counterterm by c, and its source/energy terms by Delta. Jensen's inequality for (omega+x)^−2, followed by (1+y)^−2≥1−2y for y≥0, gives

\[
D=2g^2[(b-b_s)-2Lb_3]>0,\qquad
n\ge n_-=\frac D{1+A+D}.
\]

These are uniform bounds along the full v path. Source reversal gives E1(epsilon)=E0(−epsilon), while E0'(v)=−(1−2n(v)). Therefore the exact stationary gap satisfies

\[
\boxed{\Delta(1-2n_+)\le\Omega=E_1-E_0\le\Delta(1-2n_-)<\Delta.}
\]

This is the actual complete-hard-field spectral gap. It supplies the clock bounds used below. H002466's Delta Z was its projected clock for a different W preparation, and remains separately retained there.

## 4. Source amplitude, energy and conditional entanglement

Charge0's source-ground component has equal circular photon counts. Its non-vacuum probability is at most ⟨N_+⟩≤An_+. The corresponding charge1 component has the reversed bound. Keeping their vacuum overlap and paying the possible non-vacuum overlap gives

\[
M_- =1-(1+2A)n_+\le M=\langle\Phi_0|\sigma_-|\Phi_1\rangle\le1-n_-=M_+<1.
\]

For the equal branch preparation, |⟨S⟩|≤w=n_+−n_-. Its source-current complex amplitude is M exp(−iOmega t), and its source purity is at most (1+M_+²+w²)/2<1. This proves source-field entanglement for each conditional pure lane. The equal-lane mixture retains the full16 source; conditional lane purity and the unconditional mixed-source purity are distinct quantities.

The two Gaussian trial energies have opposite source means, so their average bounds the two exact branch energies by delta_bar. Including the initially vacant soft field's counterterm c_s≤2g²mu_s gives

\[
\langle K\rangle_{\rm prep}\le\bar\delta+\epsilon w+c_s,
\qquad
e_{ab}-\epsilon w\le E_{\rm prep}\le e_{ab}+\bar\delta+c_s.
\]

The original background energy remains in its separate inherited account. The lane even reference is kept in this bound, and no mean or reference is fitted away.

## 5. Actual full autonomous source: complete Gaussian remainder

Work in the interaction picture of the exact hard Hamiltonian and free soft field. The two hard source operators have norm1. Every soft vacuum contraction has magnitude≤v_s. Odd vacuum words vanish. At order2n, the nested-commutator expansion contributes at most2^(2n), the two field choices per contraction at most2^n, Wick pairings number(2n−1)!!, and ordered time volume is t^(2n)/(2n)!. Their full sum is

\[
\boxed{\|\rho_h(t)-\rho_{h,0}(t)\|_1\le\mathcal E(t)
=\exp(4g^2v_st^2)-1.}
\]

Finite soft vacuum variance and bounded source operators control the complete convergent Gaussian expansion; the bound pays every order. The recipient retains every soft mode and all hard photon sectors. No second-order state is substituted for the actual state.

For a qubit, its equatorial Bloch-vector error is bounded by its trace distance. Thus the actual current has amplitude≥M_-−E, and phase error about−Omega t at most arcsin(E/M_-). The delay relative to the signed bare source clock is enclosed by

\[
\boxed{(\Delta-\Omega_+)t-\arcsin(\mathcal E/M_-)
\le\delta\theta(t)\le
(\Delta-\Omega_-)t+\arcsin(\mathcal E/M_-).}
\]

Every positive native source window has a strictly positive lower delay. The tensor carrier plane rotates by half this source phase. Actual source purity is bounded by

\[
\tfrac12[1+(M_++\mathcal E)^2+(w+\mathcal E)^2]<1
\]

through the cycle in every lane, giving conditional source-field entanglement under the full law. Exact total energy and Q conservation give source energy change≤epsilon E in magnitude and signed field-action change≤I_s E. The unbounded actual free-field energy is enclosed by

\[
\bigl[\max(0,\sqrt c-\sqrt{K_t})^2,(\sqrt c+\sqrt{K_t})^2\bigr],
\quad K_t=\bar\delta+\epsilon w+c_s+\epsilon\mathcal E(t).
\]

## 6. Complete receiver, incoming momentum and signed cancellation

Place the receiver at r=R+64. The full retarded kernel is

\[
\chi(s)=\frac{P_2((R^2+r^2-s^2)/(2Rr))}{\kappa Rr},
\qquad64<s<64+2R,
\]

and vanishes outside that interval. Its complete outgoing transform is

\[
\chi_{\rm out}(\Omega)=\frac{e^{i\Omega r}}{\kappa r}
\int_{-1}^1P_2\left(-v+\frac R{2r}(1-v^2)\right)e^{i\Omega Rv}dv.
\]

The same spherical-Bessel/angular construction follows from the [NIST Legendre representation](https://dlmf.nist.gov/10.54.E2). Define the full soft principal-value transfer, with its pole retained, by

\[
\chi_{s,\rm PV}(\Omega)=2\operatorname{PV}\int_0^\lambda
\frac{\omega u_R(\omega)u_r(\omega)}{\omega^2-\Omega^2}d\omega.
\]

Then chi_h=Re chi_out−chi_s,PV>0 in every native lane. Exact stationary mode matrix elements give a hard reference receiver mean g M chi_h exp(−iOmega t). Its free incoming field is

\[
2gM\int_\lambda^\infty u_Ru_r
\frac{\omega\cos(\omega t)-i\Omega\sin(\omega t)}{\omega^2-\Omega^2}d\omega.
\]

Its initial momentum is nonzero. The full retarded source drive is added to this whole incoming field. The exact hard harmonic equals hard incoming plus hard drive. The ideal complete receiver consequently equals the hard harmonic plus the entire soft drive. With

\[
C_{Rr}\le\frac{R^2r^2\lambda^6}{675\kappa\pi},
\]

the ideal soft contribution is enclosed by a disk2|g|M_+t C_Rr. The actual source-current remainder adds a disk |g|E(t)∫|chi(s)|ds. Native arithmetic encloses the complete receiver mean by the sum of those disks about the hard harmonic. The resulting phase halfwidth is

\[
\arcsin\frac{2|g|M_+tC_{Rr}+|g|\mathcal E(t)\|\chi\|_1}
{|g|M_-\chi_{h,\rm low}}.
\]

The stationary hard harmonic includes its fixed initial signed orientation g. Receiver clock delays are measured against the corresponding prepared local bare phase−Delta t, with that same orientation. The outgoing source-induced waveform is separately retained as g M chi_out exp(−iOmega t) after the full pulse, with its radial transfer phase explicit. These reference conventions allow the prepared clock and the causal source waveform to be inspected independently.

The source-induced response measured relative to the full free incoming field first advances at64. Its right plus slope is gM/(kappa Rr), and its cross slope is zero. The complete prepared receiver field can vary before64. This new preparation's ruler is the source-induced arrival; H002466's first-total-change result belongs to its own preparation.

Native chi_s,PV uses the complete convergent j2 product series with an explicit24-term tail and its exact logarithmic PV primitive. The checker instead integrates after subtracting the pole numerator, with the logarithmic pole contribution kept. The full signed retarded transform is independently integrated directly over[-1,1]. Whole incoming and momentum terms are checked by the exact mode oscillator identity.

## 7. Retained result and continuation

STRUCTURE.json.gz gives36 stationary lane certificates. CLOCK.json.gz gives180 actual source windows R,2R,64,quarter,cycle. RECEIVER.json.gz gives144 complete receiver windows at arrival, full causal pulse, received quarter and received cycle. All six incidence/radius preparations retain the original54 background references. These counts refer to the stated preparations and windows.

The reference strongest pair has exact gap fractional change in approximately[−1.65889426e−6,−1.60744986e−6]. Its actual source-cycle delay is[1.00999054e−5,1.04231400e−5]rad. The complete receiver additional phase uncertainty at its received cycle is about5.73357e−10rad. Even the weakest pair's received-cycle delay remains strictly positive. Exact endpoints and all conditional data are in [tables](NUMERICAL_SUMMARY.md).

**The test result suggests strong contact with the concept.** The interacting source gap, actual source phase, conditional entanglement, complete energy/action and tensor receiver now share one model Hamiltonian. The named next construction is a finite preparation protocol for these charged branches, with its duration, error and signed work. Numeric physical unit incidence is a further source input to that protocol.
