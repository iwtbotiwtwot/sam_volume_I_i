"""Scientific invariants and deliberate failure cases, without a GEN6 runtime."""

import copy
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import unittest

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sam_chapter1.certificates import (CertificateError, replay_certificate,
                                       replay_lane, verify_packet_bindings)
from sam_chapter1.intervals import (Interval as IV, decimal_outward, expm1,
                                    pi_interval, sqrt)
from sam_chapter1.reference import (EPSILON, Gaussian, I, actual_clock_rate,
                                    centered_rate_error, centered_residual,
                                    characteristic_polynomial, commutator,
                                    counterterms, identity, inverse_phase_coordinates,
                                    lane_operators, matadd, matmul, matscale,
                                    pair_operators, phase_action_coefficients,
                                    phase_coordinates, placement_calibration,
                                    polynomial_value, root_count,
                                    shifted_source_polynomial, source_matrix,
                                    spectral_calibration, static_square,
                                    weighted_duhamel, write_action_differential)


def exact_complex_matrix(matrix):
    return [[value if isinstance(value, Gaussian) else Gaussian(value)
             for value in row] for row in matrix]


class ExactFiniteSourceTests(unittest.TestCase):
    def assertMatrixEqual(self, left, right):
        self.assertEqual(exact_complex_matrix(left), exact_complex_matrix(right))

    def test_receiving_strength_is_explicit(self):
        self.assertEqual(source_matrix()[0], [F(756), F(104), F(40), F(0)])
        self.assertEqual(source_matrix(0)[0], [F(84), F(8), F(8), F(0)])
        self.assertNotEqual(source_matrix(), source_matrix(F(1, 2)))

    def test_characteristic_polynomial_and_cayley_hamilton(self):
        coefficients = shifted_source_polynomial()
        self.assertEqual(coefficients, [1, -1344, -14016, 4300800, 17305600])
        shifted = matadd(source_matrix(), matscale(identity(4), -756))
        value = [[F(0)] * 4 for _ in range(4)]
        for coefficient in coefficients:
            value = matadd(matmul(value, shifted), matscale(identity(4), coefficient))
        self.assertEqual(value, [[F(0)] * 4 for _ in range(4)])

    def test_full_source_signed_commutators(self):
        ops = pair_operators()
        s, d, c = (ops[key] for key in ("Swap", "D", "C"))
        self.assertMatrixEqual(commutator(s, d), matscale(c, -2 * I))
        self.assertMatrixEqual(commutator(s, c), matscale(d, 2 * I))
        self.assertMatrixEqual(matmul(c, c), matmul(d, d))
        self.assertMatrixEqual(commutator(d, c), matscale(matmul(s, matmul(d, d)), -2 * I))
        self.assertMatrixEqual(matmul(s, s), identity(16))
        zero = [[F(0)] * 16 for _ in range(16)]
        self.assertMatrixEqual(commutator(ops["even"], d), zero)
        self.assertMatrixEqual(commutator(ops["even"], c), zero)

    def test_all_four_helicity_words_preserve_signed_charge(self):
        ops = pair_operators()
        ns = matscale(matadd(identity(16), ops["Swap"]), F(1, 2))
        # The irrelevant common sqrt(2) is omitted from both source ladders.
        lowering = matadd(ops["D"], matscale(ops["C"], I))
        raising = matadd(ops["D"], matscale(ops["C"], -I))
        self.assertMatrixEqual(commutator(ns, lowering), matscale(lowering, -1))
        self.assertMatrixEqual(commutator(ns, raising), raising)
        # (source charge change, photon signed-charge change): L a+dagger,
        # Ldagger a+, Ldagger a-dagger, L a-. No word is discarded.
        self.assertTrue(all(source + photon == 0 for source, photon in
                            [(-1, 1), (1, -1), (1, -1), (-1, 1)]))

    def test_negative_lane_difference_has_signed_sigma_y(self):
        ops = lane_operators(-7)
        self.assertEqual(ops["C"][0][1], Gaussian(0, 7))
        self.assertMatrixEqual(ops["C"], matscale(matmul(ops["S"], ops["D"]), I))
        flipped = matscale(ops["C"], -1)
        self.assertNotEqual(exact_complex_matrix(commutator(ops["S"], ops["D"])),
                            exact_complex_matrix(matscale(flipped, -2 * I)))

    def test_original_calibration_is_expectation_not_eigenstate(self):
        calibration = placement_calibration()
        self.assertEqual(calibration["energy_expectation"], 573049)
        self.assertEqual(calibration["energy_variance"], 14384109824)
        self.assertEqual(calibration["Q_second_moment"], 583952)
        self.assertEqual(calibration["D_expectation"], 0)
        self.assertEqual(calibration["C_expectation"], Gaussian())
        # Zero current expectation is not annihilation of the original ket.
        self.assertTrue(any(row[0] != 0 for row in pair_operators()["D"]))

    def test_spectral_weights_reconstruct_original_energy(self):
        with mp.workdps(90):
            spectrum = spectral_calibration(90)
            self.assertTrue(all(weight > 0 for weight in spectrum["weights"]))
            self.assertLess(abs(spectrum["weight_sum"] - 1), mp.mpf("1e-80"))
            self.assertLess(abs(spectrum["population_sum"] - 1), mp.mpf("1e-80"))
            self.assertLess(abs(spectrum["population_energy"] - 573049), mp.mpf("1e-75"))
            self.assertLess(max(abs(a - b) for a, b in
                                zip(spectrum["weights"], spectrum["resolvent_weights"])), mp.mpf("1e-80"))

    def test_sturm_root_counter_is_not_a_rounded_root_comparison(self):
        self.assertEqual(root_count([1, 0, -2], 1, 2), 1)
        self.assertEqual(root_count([1, 0, -2], 2, 3), 0)
        self.assertEqual(root_count([1, 0, -2], -2, 2), 2)
        with self.assertRaises(ValueError):
            root_count([1, -1], 1, 2)


class PhaseAndActionTests(unittest.TestCase):
    def test_lifted_inverse_and_common_phase(self):
        phases = (F(37, 3), F(-71, 5), F(29, 7))
        coordinates = phase_coordinates(*phases)
        self.assertEqual(inverse_phase_coordinates(*coordinates), phases)
        shift = F(125, 11)
        moved = phase_coordinates(*(phase + shift for phase in phases))
        self.assertEqual(moved[:2], coordinates[:2])
        self.assertEqual(moved[2], coordinates[2] + shift)
        self.assertEqual(write_action_differential(0, shift), 3 * shift)

    def test_write_ledger_is_sum_of_three_lifted_differentials(self):
        a, b, p = F(19, 3), F(-5, 7), F(17, 5)
        gamma, _, chi = phase_coordinates(a, b, p)
        self.assertEqual(write_action_differential(gamma, chi), a + b + p)

    def test_both_polarization_counterterms_and_static_minimum(self):
        g, radius = F(-7, 19), F(3, 11)
        payment = counterterms(g, radius)
        self.assertEqual(payment["total"], g * g / (2 * radius))
        self.assertEqual(payment["total"], payment["plus"] + payment["cross"])
        self.assertNotEqual(payment["total"], payment["plus"])
        eps, current = F(2, 3), F(-7, 5)
        self.assertEqual(static_square(eps * current / 2, eps, current, radius), 0)
        for coordinate in [F(-9), F(0), F(12, 7)]:
            self.assertGreaterEqual(static_square(coordinate, eps, current, radius), 0)

    def test_actual_reference_clock_sign(self):
        with mp.workdps(70):
            delta, omega, g = mp.mpf("2"), mp.mpf("1.7"), mp.mpf("-.3")
            z = mp.mpc(".7", ".2")
            reference_w = 1j * (delta - omega) * z / (2 * g)
            self.assertLess(abs(actual_clock_rate(z, reference_w, delta, g) - omega), mp.mpf("1e-65"))
            self.assertEqual(actual_clock_rate(z, 0, delta, g), delta)
            initial_plus = -(delta - omega) * mp.mpf(".7") / (2 * g)
            self.assertGreater(initial_plus, 0)
        with self.assertRaises(ValueError):
            actual_clock_rate(0, 1, 2, -1)

    def test_centered_residual_cancels_common_reference_exactly(self):
        with mp.workdps(70):
            delta, omega, g = mp.mpf("2"), mp.mpf("1.7"), mp.mpf("-.3")
            h, dz, dw = mp.mpc(".6", "-.2"), mp.mpc(".01", ".02"), mp.mpc(".03", "-.04")
            z, wh = h + dz, 1j * (delta - omega) * h / (2 * g)
            zdot = -1j * delta * z + 2 * g * (wh + dw)
            self.assertLess(abs(zdot + 1j * omega * z
                                - centered_residual(dz, dw, delta, omega, g)), mp.mpf("1e-65"))

    def test_centered_hypotheses_reject_zero_amplitude_or_wrong_gap(self):
        for args in [(2, 1, 1, 1, 1, 1), (2, 3, 1, 0, 1, 0), (2, 1, 1, 0, -1, 0)]:
            with self.assertRaises(ValueError):
                centered_rate_error(*args)
        self.assertEqual(centered_rate_error(F(2), F(1), F(1), F(0), F(1), F(0)), 0)

    def test_one_common_rate_controls_whole_action_family(self):
        nu, eps, even, g, c = F(7, 13), EPSILON, F(19, 7), F(-3, 11), F(2, 17)
        action = phase_action_coefficients(nu, eps, even, g, c)
        self.assertEqual(action["field_kinetic"] * action["field_gradient"], F(-1, 25))
        self.assertEqual(action["field_angular"], 6 * action["field_gradient"])
        self.assertEqual(action["source_even"] * nu, -even)
        self.assertEqual(action["source_exchange"] * nu, -eps)
        self.assertEqual(action["boundary_interaction"] * nu, g)
        self.assertEqual(action["both_counterterms"] * nu, -c)
        self.assertIsInstance(phase_action_coefficients(1, eps, even, g, c)["inverse_rate"], F)
        with self.assertRaises(ValueError):
            phase_action_coefficients(0, eps, even, g, c)

    def test_weighted_duhamel_zero_and_invalid_inputs(self):
        self.assertEqual(weighted_duhamel(0, 2, 3, 4, 5, 6), 0)
        with self.assertRaises(ValueError):
            weighted_duhamel(-1, -2, 3, 4, 5, 6)


class RationalIntervalTests(unittest.TestCase):
    def test_float_and_reversed_interval_rejected(self):
        with self.assertRaises(TypeError):
            IV.point(0.1)
        with self.assertRaises(ValueError):
            IV(2, 1)
        with self.assertRaises(ValueError):
            IV(-1, 1).reciprocal()

    def test_interval_products_squares_and_reciprocal(self):
        self.assertEqual(IV(-2, 3) * IV(-5, 7), IV(-15, 21))
        self.assertEqual(IV(-2, 3) ** 2, IV(0, 9))
        self.assertEqual(IV(2, 4).reciprocal(), IV(F(1, 4), F(1, 2)))
        self.assertEqual(IV(-4, -2).reciprocal(), IV(F(-1, 2), F(-1, 4)))

    def test_sqrt_is_exactly_bracketed_by_integer_arithmetic(self):
        result = sqrt(IV(2, 3), 256)
        self.assertLessEqual(result.lower ** 2, 2)
        self.assertGreaterEqual(result.upper ** 2, 3)
        self.assertEqual(sqrt(IV.point(4)), IV.point(2))

    def test_pi_and_exponential_tail_enclosures(self):
        with mp.workdps(110):
            pi = pi_interval(256)
            self.assertLess(mp.mpf(pi.lower.numerator) / pi.lower.denominator, mp.pi)
            self.assertGreater(mp.mpf(pi.upper.numerator) / pi.upper.denominator, mp.pi)
            out = expm1(IV.point(F(1, 100)), 256)
            value = mp.expm1(mp.mpf(".01"))
            self.assertLessEqual(mp.mpf(out.lower.numerator) / out.lower.denominator, value)
            self.assertGreaterEqual(mp.mpf(out.upper.numerator) / out.upper.denominator, value)
        with self.assertRaises(ValueError):
            expm1(IV.point(1))

    def test_signed_directed_decimal_rounding(self):
        self.assertEqual(decimal_outward(F(1, 3), 3, "lower"), "0.333")
        self.assertEqual(decimal_outward(F(1, 3), 3, "upper"), "0.334")
        self.assertEqual(decimal_outward(F(-1, 3), 3, "lower"), "-0.334")
        self.assertEqual(decimal_outward(F(-1, 3), 3, "upper"), "-0.333")
        self.assertEqual(decimal_outward(F(2), 3, "upper"), "2.000")


class RetainedCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads((ROOT / "data/chapter1_certificate.json").read_text())

    def test_complete_source_bound_packet(self):
        result = verify_packet_bindings(self.packet, ROOT / "evidence/native")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["source_files"], 2)

    def test_all_six_clocks_are_positive_and_delayed_for_the_same_window(self):
        result = replay_certificate(self.packet)
        self.assertEqual(result["root_isolation"]["roots_per_interval"], [1, 1, 1, 1])
        self.assertEqual(len(result["lanes"]), 6)
        for lane in result["lanes"]:
            rate = IV.from_json(lane["printed_rate"])
            self.assertGreater(rate.lower, 0)
            self.assertLess(rate.upper, 2 * EPSILON)
            self.assertGreater(F(lane["centered_positive_margin_lower"]), 0)

    def test_changed_operand_fails_binding_even_if_positivity_survives(self):
        changed = copy.deepcopy(self.packet)
        changed["lanes"][0]["clock"]["Kprep"]["upper"] = "1/1000000"
        with self.assertRaisesRegex(CertificateError, "Changed operand"):
            verify_packet_bindings(changed, ROOT / "evidence/native")

    def test_deleted_binding_cannot_hide_changed_operand(self):
        changed = copy.deepcopy(self.packet)
        changed["bindings"] = []
        with self.assertRaises(CertificateError):
            verify_packet_bindings(changed, ROOT / "evidence/native")

    def test_positive_g_rejected_even_though_energy_uses_g_squared(self):
        lane = copy.deepcopy(self.packet["lanes"][0])
        g = IV.from_json(lane["clock"]["g"])
        lane["clock"]["g"] = (-g).as_json()
        with self.assertRaisesRegex(CertificateError, "signed g<0"):
            replay_lane(lane, self.packet["q"])

    def test_inward_rate_display_rejected(self):
        lane = copy.deepcopy(self.packet["lanes"][0])
        lane["certificate"]["rate_display_times_1e6"]["lower"] = "3.490102930000"
        with self.assertRaisesRegex(CertificateError, "rounds inward"):
            replay_lane(lane, self.packet["q"])

    def test_inward_signed_coupling_enclosure_rejected(self):
        lane = copy.deepcopy(self.packet["lanes"][0])
        g = IV.from_json(lane["clock"]["g"])
        lane["clock"]["g"] = IV.point(g.midpoint).as_json()
        with self.assertRaisesRegex(CertificateError, "source-root incidence"):
            replay_lane(lane, self.packet["q"])

    def test_unachieved_correlator_ceiling_rejected(self):
        lane = copy.deepcopy(self.packet["lanes"][0])
        lane["certificate"]["W_upper_display"] = "0"
        with self.assertRaisesRegex(CertificateError, "correlator bound rounds inward"):
            replay_lane(lane, self.packet["q"])

    def test_missing_lane_and_modified_root_bracket_rejected(self):
        missing = copy.deepcopy(self.packet)
        missing["lanes"].pop()
        with self.assertRaises(CertificateError):
            replay_certificate(missing)
        shifted = copy.deepcopy(self.packet)
        shifted["q"][0] = IV(690, 691).as_json()
        with self.assertRaisesRegex(CertificateError, "Sturm isolation"):
            replay_certificate(shifted)

    def test_only_one_counterterm_rejected(self):
        lane = copy.deepcopy(self.packet["lanes"][0])
        c = IV.from_json(lane["clock"]["counterterm"])
        lane["clock"]["counterterm"] = (c / 2).as_json()
        with self.assertRaisesRegex(CertificateError, "Both-current counterterm"):
            replay_lane(lane, self.packet["q"])


if __name__ == "__main__":
    unittest.main()
