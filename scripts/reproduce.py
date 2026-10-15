#!/usr/bin/env python3
"""Reproduce Chapter I finite algebra and six conditional scalar certificates.

No GEN6 installation is required and no fresh native science job is submitted.
The separate scripts/verify_native.py replays the retained native-check record.
"""

import argparse
import csv
from fractions import Fraction as F
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp

from sam_chapter1.certificates import (CertificateError, replay_certificate,
                                       sha256, verify_packet_bindings)
from sam_chapter1.intervals import Interval
from sam_chapter1.placements import chapter_source
from sam_chapter1.reference import (EPSILON, Gaussian, PAIRS,
                                    mp_number, phase_action_coefficients,
                                    placement_calibration, shifted_source_polynomial,
                                    source_matrix, spectral_calibration, weighted_duhamel)


def exact_json(value):
    if isinstance(value, Gaussian):
        return {"re": str(value.re), "im": str(value.im)}
    return str(value)


def numerical_reconstruction(packet, precision):
    """magnitude representatives checked independently from rational replay."""
    with mp.workdps(precision):
        spec = spectral_calibration(precision)
        tolerance = mp.power(10, -(precision - 20))
        residuals = {
            "weight_normalization": abs(spec["weight_sum"] - 1),
            "first_source_moment": abs(spec["first_moment"] - 756),
            "second_source_moment": abs(spec["second_moment"] - 583952),
            "population_normalization": abs(spec["population_sum"] - 1),
            "population_energy": abs(spec["population_energy"] - 573049),
            "resolvent_vs_eigenvector_weights": max(abs(a - b) for a, b in
                                                     zip(spec["weights"], spec["resolvent_weights"])),
        }
        if any(value >= tolerance for value in residuals.values()):
            raise CertificateError("Independent spectral/calibration reconstruction failed")
        for root, native in zip(spec["roots"], packet["q"]):
            bounds = Interval.from_json(native)
            if not mp_number(bounds.lower) <= root <= mp_number(bounds.upper):
                raise CertificateError("Independent eigensystem is outside retained root enclosure")
        display = lambda number: mp.nstr(number, precision)
        lanes = []
        for lane in packet["lanes"]:
            get = lambda key: mp_number(Interval.from_json(lane["clock"][key]).midpoint)
            g, radius, kp = get("g"), get("R"), get("Kprep")
            eps = mp_number(EPSILON)
            delta, cutoff = 2 * eps, 128 * eps
            time, mu = mp.pi / eps, 1 / (4 * radius)
            c = 2 * g * g * mu
            vsoft = radius ** 4 * cutoff ** 6 / (540 * mp.pi)
            error = mp.expm1(4 * g * g * vsoft * time ** 2)
            field = (mp.sqrt(c) + mp.sqrt(kp + eps * error)) ** 2
            w = weighted_duhamel(g, time, mu, vsoft, field, cutoff)
            native_w = Interval.from_json(lane["certificate"]["uniform_correlator_error"])
            if not mp_number(native_w.lower) <= w <= mp_number(native_w.upper):
                raise CertificateError("Independent Duhamel representative misses retained native interval")
            gap = Interval.from_json(lane["clock"]["actual_initial_rate"])
            # One common reference-rate representative illustrates dependent
            # coefficients. The actual time-varying rate is enclosed by the
            # separate rigorous result, not numerically simulated here.
            nu = mp_number(gap.midpoint)
            a, b = lane["pair"]
            even_energy = eps * (spec["roots"][a] + spec["roots"][b]
                                 + spec["roots"][a] * spec["roots"][b])
            family = phase_action_coefficients(nu, eps, even_energy, g, c)
            lanes.append({"pair": lane["pair"], "g": display(g),
                          "vsoft": display(vsoft), "source_error_T": display(error),
                          "field_energy_bound": display(field), "weighted_duhamel": display(w),
                          "representative_rate_source": "midpoint of retained hard gap; illustrative coefficient family only",
                          "phase_action_at_one_common_rate": {key: display(value)
                                                               for key, value in family.items()}})
        return {"status": "PASS", "method": "mpmath independent eigsy and high-precision scalar evaluation; numerical representatives, not replacement certificates",
                "decimal_precision": precision, "absolute_residual_threshold": display(tolerance),
                "residuals": {key: display(value) for key, value in residuals.items()},
                "eigenvalues": [display(value) for value in spec["roots"]],
                "calibration_weights": [display(value) for value in spec["weights"]],
                "resolvent_weights": [display(value) for value in spec["resolvent_weights"]],
                "population_energy": display(spec["population_energy"]), "lanes": lanes}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=150,
                        help="mpmath decimal digits; at least 130 for retained 384-bit root brackets")
    parser.add_argument("--output", type=Path, default=ROOT / "build")
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence/native")
    parser.add_argument("--inputs", type=Path, default=ROOT / "data/chapter1_certificate.json")
    args = parser.parse_args(argv)
    if args.precision < 130:
        parser.error("--precision must be at least 130 to cross-check the retained 384-bit roots")
    try:
        packet = json.loads(args.inputs.read_text())
        bindings = verify_packet_bindings(packet, args.evidence)
        rational = replay_certificate(packet)
        numerical = numerical_reconstruction(packet, args.precision)
        calibration = placement_calibration()
        generated = chapter_source()
        report = {
            "schema": "SAM_CHAPTER1_PORTABLE_REPRODUCTION_V1", "status": "PASS",
            "input_sha256": sha256(args.inputs), "source_bindings": packet["source_bindings"],
            "scope": packet["scope"],
            "provenance": {
                "native_certified_inputs": "Unchanged retained exact source roots and hard-branch/preparation bounds in evidence/native; source hashes and JSON pointers are checked before calculation.",
                "exact_independent_replay": "Placement-code boundary, original signed-response ledger, generated B/T/K, finite source algebra, Sturm root isolation and rational interval propagation of conditional scalar consequences.",
                "numerical_independent_reconstruction": "150-digit by default; eigensystem, weights, energy moments and Duhamel representatives.",
                "excluded": "No continuum simulation, hard eigenbranch solver, new GEN6 job, SI time assignment, physical coupling fit or arbitrary sixteen-state clock certificate."},
            "bindings": bindings,
            "exact_source": {
                "ordered_placement_codes": list(generated.boundary.codes),
                "decoded_paths": generated.boundary.paths,
                "boundary_target_codes": generated.boundary.target_codes,
                "B": generated.boundary.B,
                "T": generated.boundary.T,
                "signed_responses": [[str(value) for value in row] for row in generated.responses],
                "K": [[str(value) for value in row] for row in generated.K],
                "placement_response_packet_sha256": sha256(ROOT / "src/sam_chapter1/data/placement_response.json"),
                "Q": [[str(value) for value in row] for row in source_matrix()],
                "shifted_characteristic_polynomial_descending": [str(value) for value in shifted_source_polynomial()],
                "epsilon": str(EPSILON), "Delta": str(2 * EPSILON),
                "placement_calibration": {key: exact_json(value) for key, value in calibration.items()}},
            "rational_interval_replay": rational,
            "high_precision_reconstruction": numerical,
        }
        args.output.mkdir(parents=True, exist_ok=True)
        report_path = args.output / "reproduction.json"
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        with (args.output / "rates.csv").open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["lane", "rate_lower_times_1e6", "rate_upper_times_1e6", "W_upper", "chart", "status"])
            for lane in packet["lanes"]:
                cert = lane["certificate"]
                writer.writerow(["".join(map(str, lane["pair"])),
                                 cert["rate_display_times_1e6"]["lower"],
                                 cert["rate_display_times_1e6"]["upper"],
                                 cert["W_upper_display"], "normalized_model_time", "PASS"])
        print(f"PASS: exact source, four isolated roots and six conditional clock certificates; {args.precision}-digit reconstruction")
        print(f"Wrote {report_path} and {args.output / 'rates.csv'}")
        return 0
    except (CertificateError, ValueError, KeyError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
