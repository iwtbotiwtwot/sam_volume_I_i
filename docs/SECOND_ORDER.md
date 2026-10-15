# Independent second-order hard-clock test

The second-order test checks the weak-coupling sign and normalization of the
interacting hard-branch gap. It uses the same two real polarizations, signed
lane coupling, hard split and two counterterms as Chapter I. It also checks the
predicted coefficient against independently diagonalized finite matrices.

```bash
python scripts/second_order.py
python -m unittest discover -s tests -p 'test_second_order.py' -v
```

The command first verifies the retained input bindings and writes
`build/second_order.json`. It operates offline and submits no native job.

## Derivation from the retained Hamiltonian

The [resolved hard-clock derivation](../references/derivations/RESOLVED_CLOCK_DERIVATION.md),
sections 1–3, specifies the isolated hard branches. The
[reference supplement](../references/derivations/REFERENCE_SUPPLEMENT.md),
sections 1–3, binds their gap to the reference clock. In the source-energy basis,
with the common even energy displayed separately, the hard operator is

\[
H_h=\epsilon S+H_{f,h}
 -g(\sigma_x\phi_{+,h}+\sigma_y\phi_{\times,h})+2g^2\mu_h,
\quad S=\operatorname{diag}(-1,1),\quad\Delta=2\epsilon,
\quad\lambda=64\Delta.
\]

Here \(\mu_h=\int_\lambda^\infty |u_R(\omega)|^2/\omega\,d\omega\).
The unperturbed source-vacuum state of sign \(s=\pm1\) has energy
\(s\Delta/2\). Each polarization flips the source and creates one photon.
Its energy denominator is \(s\Delta-\omega\). Thus the coefficient of
\(g^2\), including the full common counterterm, gives

\[
E_s^{(2)}=s\Delta/2+g^2\left[
 2\mu_h-2\int_\lambda^\infty
 \frac{|u_R(\omega)|^2}{\omega-s\Delta}\,d\omega\right].
\]

The factor two counts the two real polarizations. Their counterterms contribute
equally to both branch energies and cancel from the gap. The even source energy
also cancels from this difference. Both remain in the complete action.

Subtracting the two branch energies gives

\[
\Omega^{(2)}=\Delta-4g^2\Delta J,
\qquad J=\int_\lambda^\infty
 \frac{|u_R(\omega)|^2}{\omega^2-\Delta^2}\,d\omega>0.
\]

This predicts a slower hard clock at second order. The source transition overlap
has the independent second-order prediction

\[
M^{(2)}=1-g^2\int_\lambda^\infty |u_R(\omega)|^2
\left[\frac1{(\omega-\Delta)^2}+\frac1{(\omega+\Delta)^2}\right]d\omega.
\]

These expansions concern the stationary hard branches. The actual full-field
instantaneous rate retains Chapter I's soft interaction and uniform remainder
estimates.

## Complete-continuum coefficient check

The test encloses \(J\) analytically, without a frequency grid or ultraviolet
cutoff. From the retained quadrupole identities

\[
b=\int_0^\infty\frac{|u_R(\omega)|^2}{\omega^2}d\omega
  =\frac1{6\kappa\pi},\qquad
b_s\le\frac{R^4\lambda^4}{450\kappa\pi},
\]

and \(\omega\ge\lambda>\Delta\), one obtains

\[
\max(0,b-b_s^{\rm up})\le J
\le\frac{b}{1-(\Delta/\lambda)^2}.
\]

Exact rational interval arithmetic and an enclosed \(\pi\) propagate this
coefficient into all six source-bound lane predictions. For the bundled inputs,
each predicted interval lies inside the retained exact hard-gap enclosure and
below \(\Delta\). The report records those comparisons and the conservative
interval difference divided by \(g^4\).

The coefficient enclosure is rigorous. The second-order gap omits higher
orders; its continuum fourth-order remainder is not bounded here. The retained
exact hard-branch bounds supply the clock certificate. Containment of the
perturbative interval in a retained enclosure is a consistency check.

## Independent finite-mode convergence check

A separate declared synthetic fixture has \(\Delta=1\), one radial frequency
\(\omega=4\), and smearing \(u=7/10\) for each real polarization. Circular
modes expose all four interaction words,

\[
-\sqrt2gu(\sigma_-a_+^\dagger+\sigma_+a_+
          +\sigma_+a_-^\dagger+\sigma_-a_-).
\]

The matrices retain signed charge \(Q=N_s+N_+-N_-\), both charge-0/1 sectors,
and total photon number up to four. Each sector has five basis states. The test
diagonalizes these matrices directly and evaluates the source-lowering matrix
element between their lowest branches. It does not use the perturbative formula
to construct the eigenvalues or overlap.

At \(g=-1/20,-1/40,-1/80\), the absolute errors of the second-order gap and
overlap decrease by approximately sixteen whenever the coupling halves:

| Quantity | First error ratio | Second error ratio |
|---|---:|---:|
| Hard gap | 15.99448681 | 15.99862114 |
| Transition overlap | 15.99284567 | 15.99821050 |

These observed ratios agree with an \(O(g^4)\) remainder for the fixture.
Additional tests check that both branch energies retain the common counterterm,
the gap and overlap are invariant under a common energy shift, the spectral
results are invariant under coupling reversal, and a larger six-photon fixture
agrees beyond the tested fourth-order term. Invalid hard denominators are
rejected.

The finite-mode fixture tests the perturbative algebra. Its photon cutoff and
single radial bin define a separate numerical model; it supplies no replacement
continuum evolution, exact Chapter I preparation, or native certificate.
