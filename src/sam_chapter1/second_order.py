"""Independent weak-coupling diagnostic for the retained hard clock.

The continuum functions enclose the coefficient of g**2, not its omitted
higher-order remainder. The finite-mode fixture is an explicitly separate
two-polarization model used to test the perturbative derivation.
"""

from fractions import Fraction as F

import mpmath as mp

from .intervals import Interval as IV, interval, pi_interval
from .reference import KAPPA


def hard_gap_coefficient(delta, cutoff, radius, bits=256):
    """Enclose J = integral_h |u_R(w)|**2/(w**2-Delta**2) dw.

    Uses the complete quadrupole norm b and the retained soft b bound.
    It introduces neither a frequency grid nor a UV cutoff.
    """
    delta, cutoff, radius = map(interval, (delta, cutoff, radius))
    if delta.lower <= 0 or cutoff.lower <= delta.upper or radius.lower <= 0:
        raise ValueError("Require positive radius and hard cutoff > Delta > 0")
    pi = pi_interval(bits)
    b = 1 / (6 * KAPPA * pi)
    bsoft_upper = radius ** 4 * cutoff ** 4 / (450 * KAPPA * pi)
    lower = max(F(0), b.lower - bsoft_upper.upper)
    upper = (b / (1 - (delta / cutoff) ** 2)).upper
    return IV(lower, upper)


def hard_gap_second_order(delta, coupling, cutoff, radius, bits=256):
    """Return Delta - 4*g**2*Delta*J; no all-orders error is claimed."""
    delta, coupling = map(interval, (delta, coupling))
    coefficient = hard_gap_coefficient(delta, cutoff, radius, bits)
    return delta - 4 * coupling ** 2 * delta * coefficient


def _real(value):
    if isinstance(value, F):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def discrete_second_order(delta, coupling, frequencies, smearings):
    """Second-order energies, gap and transition overlap for radial bins.

    Every radial bin has both real polarizations, each with the stated
    smearing. Thus the common counterterm is 2*g**2*sum(u**2/w).
    """
    delta, coupling = map(_real, (delta, coupling))
    frequencies, smearings = list(map(_real, frequencies)), list(map(_real, smearings))
    if not frequencies or len(frequencies) != len(smearings):
        raise ValueError("Supply one smearing for each nonempty frequency list")
    if delta <= 0 or any(omega <= delta for omega in frequencies):
        raise ValueError("Each hard frequency must exceed positive Delta")
    mu = mp.fsum(u ** 2 / omega for omega, u in zip(frequencies, smearings))
    counterterm = 2 * coupling ** 2 * mu
    minus_shift = counterterm - 2 * coupling ** 2 * mp.fsum(
        u ** 2 / (omega + delta) for omega, u in zip(frequencies, smearings))
    plus_shift = counterterm - 2 * coupling ** 2 * mp.fsum(
        u ** 2 / (omega - delta) for omega, u in zip(frequencies, smearings))
    j = mp.fsum(u ** 2 / (omega ** 2 - delta ** 2)
                for omega, u in zip(frequencies, smearings))
    overlap_loss = coupling ** 2 * mp.fsum(
        u ** 2 * ((omega - delta) ** -2 + (omega + delta) ** -2)
        for omega, u in zip(frequencies, smearings))
    return {"minus_energy": -delta / 2 + minus_shift,
            "plus_energy": delta / 2 + plus_shift,
            "counterterm": counterterm, "J": j,
            "gap": delta - 4 * coupling ** 2 * delta * j,
            "amplitude": 1 - overlap_loss}


def finite_mode_branches(delta, coupling, frequency, smearing, max_photons=4,
                         common_energy=0, include_counterterms=True):
    """Diagonalize a declared one-bin, two-polarization diagnostic fixture.

    Circular modes make all four interaction words real. The basis has total
    photon number <= max_photons, separately in signed charges 0 and 1. This
    finite model is not the Chapter I continuum or its declared preparation.
    """
    delta, coupling, frequency, smearing, common_energy = map(
        _real, (delta, coupling, frequency, smearing, common_energy))
    if delta <= 0 or frequency <= delta:
        raise ValueError("The fixture requires frequency > Delta > 0")
    if isinstance(max_photons, bool) or not isinstance(max_photons, int) or max_photons < 2:
        raise ValueError("Retain at least two photons for the fourth-order diagnostic")
    counterterm = 2 * coupling ** 2 * smearing ** 2 / frequency
    common = common_energy + (counterterm if include_counterterms else 0)
    sectors = []
    for charge in (0, 1):
        basis = [(source, plus, minus)
                 for total in range(max_photons + 1)
                 for source in (0, 1)
                 for plus in range(total + 1)
                 for minus in (total - plus,)
                 if source + plus - minus == charge]
        indices = {state: index for index, state in enumerate(basis)}
        matrix = mp.matrix(len(basis))
        for column, (source, plus, minus) in enumerate(basis):
            matrix[column, column] = ((2 * source - 1) * delta / 2
                                      + frequency * (plus + minus) + common)
            # L a+dagger, Ldagger a+, Ldagger a-dagger, L a-.
            transitions = ([(0, plus + 1, minus, plus + 1),
                            (0, plus, minus - 1, minus)] if source else
                           [(1, plus - 1, minus, plus),
                            (1, plus, minus + 1, minus + 1)])
            for target_source, target_plus, target_minus, occupation in transitions:
                target = (target_source, target_plus, target_minus)
                if target in indices and occupation > 0:
                    matrix[indices[target], column] += (
                        -mp.sqrt(2) * coupling * smearing * mp.sqrt(occupation))
        energies, vectors = mp.eigsy(matrix)
        sectors.append((basis, indices, energies[0], vectors[:, 0]))
    basis0, _, energy0, vector0 = sectors[0]
    _, indices1, energy1, vector1 = sectors[1]
    amplitude = abs(mp.fsum(vector0[index] * vector1[indices1[(1, plus, minus)]]
                           for index, (source, plus, minus) in enumerate(basis0)
                           if source == 0 and (1, plus, minus) in indices1))
    return {"minus_energy": energy0, "plus_energy": energy1,
            "gap": energy1 - energy0, "amplitude": amplitude,
            "counterterm": counterterm,
            "sector_dimensions": [len(sector[0]) for sector in sectors]}


def convergence_fixture(precision=70):
    """Check g**4 remainders against independently diagonalized matrices."""
    if precision < 40:
        raise ValueError("Use at least 40 decimal digits for the convergence test")
    with mp.workdps(precision):
        samples = []
        for denominator in (20, 40, 80):
            coupling = -mp.mpf(1) / denominator
            prediction = discrete_second_order(1, coupling, [4], [F(7, 10)])
            exact = finite_mode_branches(1, coupling, 4, F(7, 10))
            errors = {key: abs(exact[key] - prediction[key])
                      for key in ("gap", "amplitude")}
            samples.append({"g": coupling, "exact": exact,
                            "second_order": prediction, "absolute_errors": errors})
        ratios = {key: [samples[i]["absolute_errors"][key]
                         / samples[i + 1]["absolute_errors"][key] for i in (0, 1)]
                  for key in ("gap", "amplitude")}
        # Halving g reduces a nonzero leading g**4 remainder by sixteen.
        passed = all(15 < ratio < 17 for values in ratios.values() for ratio in values)
        return {"status": "PASS" if passed else "FAIL", "decimal_precision": precision,
                "scope": "Synthetic one-radial-bin/two-polarization fixture; total photon cutoff 4, not continuum science",
                "delta": "1", "frequency": "4", "smearing_per_real_polarization": "7/10",
                "expected_error_ratio_on_halving_g": "16", "samples": samples,
                "observed_error_ratios": ratios}
