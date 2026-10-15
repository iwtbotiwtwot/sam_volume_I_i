"""Perturbative coefficient checks with independent finite-matrix evidence."""

from fractions import Fraction as F
import json
from pathlib import Path
import sys
import unittest

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sam_chapter1.intervals import Interval as IV
from sam_chapter1.second_order import (convergence_fixture, discrete_second_order,
                                       finite_mode_branches, hard_gap_coefficient,
                                       hard_gap_second_order)


class ContinuumCoefficientTests(unittest.TestCase):
    def test_six_source_bound_gap_predictions_agree_with_retained_enclosures(self):
        packet = json.loads((ROOT / "data/chapter1_certificate.json").read_text())
        for lane in packet["lanes"]:
            with self.subTest(pair=lane["pair"]):
                delta, coupling, radius, gap = (IV.from_json(lane["clock"][key]) for key in
                                                ("Delta", "g", "R", "actual_initial_rate"))
                coefficient = hard_gap_coefficient(delta, 64 * delta, radius)
                predicted = hard_gap_second_order(delta, coupling, 64 * delta, radius)
                self.assertGreater(coefficient.lower, 0)
                self.assertLess(predicted.upper, delta.lower)
                self.assertTrue(gap.contains(predicted))
                self.assertEqual(predicted, hard_gap_second_order(delta, -coupling, 64 * delta, radius))

    def test_no_resonant_denominator_or_nonpositive_radius(self):
        for delta, cutoff, radius in [(1, 1, 1), (2, 1, 1), (0, 2, 1), (1, 2, 0)]:
            with self.subTest(args=(delta, cutoff, radius)), self.assertRaises(ValueError):
                hard_gap_coefficient(delta, cutoff, radius)


class FiniteModePerturbationTests(unittest.TestCase):
    def test_both_polarizations_opposite_denominators_and_full_counterterm(self):
        with mp.workdps(60):
            predicted = discrete_second_order(1, F(-1, 20), [4], [F(7, 10)])
            g, u = mp.mpf(-1) / 20, mp.mpf(7) / 10
            self.assertEqual(predicted["counterterm"], 2 * g ** 2 * u ** 2 / 4)
            self.assertAlmostEqual(predicted["minus_energy"] + mp.mpf(1) / 2,
                                   predicted["counterterm"] - 2 * g ** 2 * u ** 2 / 5, places=55)
            self.assertAlmostEqual(predicted["plus_energy"] - mp.mpf(1) / 2,
                                   predicted["counterterm"] - 2 * g ** 2 * u ** 2 / 3, places=55)
            self.assertAlmostEqual(predicted["gap"], predicted["plus_energy"] - predicted["minus_energy"], places=55)
            self.assertLess(predicted["gap"], 1)

    def test_independent_exact_matrices_have_fourth_order_remainders(self):
        result = convergence_fixture(60)
        self.assertEqual(result["status"], "PASS")
        for values in result["observed_error_ratios"].values():
            for ratio in values:
                self.assertGreater(ratio, 15)
                self.assertLess(ratio, 17)

    def test_common_counterterm_and_even_energy_cancel_only_from_gap(self):
        with mp.workdps(60):
            args = (1, F(-1, 20), 4, F(7, 10))
            paid = finite_mode_branches(*args)
            unpaid = finite_mode_branches(*args, include_counterterms=False)
            shifted = finite_mode_branches(*args, common_energy=F(23, 7))
            for branch in ("minus_energy", "plus_energy"):
                self.assertAlmostEqual(paid[branch] - unpaid[branch], paid["counterterm"], places=55)
                self.assertAlmostEqual(shifted[branch] - paid[branch], mp.mpf(23) / 7, places=55)
            for key in ("gap", "amplitude"):
                self.assertAlmostEqual(paid[key], unpaid[key], places=55)
                self.assertAlmostEqual(paid[key], shifted[key], places=55)

    def test_fixture_keeps_both_signed_charge_sectors_and_coupling_sign(self):
        with mp.workdps(60):
            negative = finite_mode_branches(1, F(-1, 20), 4, F(7, 10))
            positive = finite_mode_branches(1, F(1, 20), 4, F(7, 10))
            self.assertEqual(negative["sector_dimensions"], [5, 5])
            for key in ("gap", "amplitude"):
                self.assertAlmostEqual(negative[key], positive[key], places=55)
            # A six-photon fixture agrees beyond the tested fourth-order term.
            enlarged = finite_mode_branches(1, F(-1, 20), 4, F(7, 10), max_photons=6)
            self.assertLess(abs(enlarged["gap"] - negative["gap"]), mp.mpf("1e-15"))

    def test_invalid_discretization_and_precision_are_rejected(self):
        for frequencies, smearings in [([], []), ([1], [1]), ([4, 5], [1])]:
            with self.assertRaises(ValueError):
                discrete_second_order(1, F(-1, 20), frequencies, smearings)
        with self.assertRaises(ValueError):
            convergence_fixture(30)
        with self.assertRaises(ValueError):
            finite_mode_branches(1, F(-1, 20), 4, 1, max_photons=1)


if __name__ == "__main__":
    unittest.main()
