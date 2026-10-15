#!/usr/bin/env python3
"""Run the independent second-order hard-clock diagnostic, without GEN6."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp

from sam_chapter1.certificates import CertificateError, sha256, verify_packet_bindings
from sam_chapter1.intervals import Interval as IV, decimal_outward
from sam_chapter1.second_order import (convergence_fixture, hard_gap_coefficient,
                                       hard_gap_second_order)


def display_interval(value):
    return {"exact": value.as_json(),
            "decimal": {"lower": decimal_outward(value.lower, 30, "lower"),
                        "upper": decimal_outward(value.upper, 30, "upper")}}


def numerical_json(value, precision):
    if isinstance(value, dict):
        return {key: numerical_json(item, precision) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [numerical_json(item, precision) for item in value]
    if isinstance(value, (mp.mpf, mp.mpc)):
        return mp.nstr(value, precision)
    return value


def diagnose(packet, precision):
    lanes = []
    for lane in packet["lanes"]:
        delta, coupling, radius, retained = (IV.from_json(lane["clock"][key]) for key in
                                            ("Delta", "g", "R", "actual_initial_rate"))
        if coupling.upper >= 0:
            raise ValueError("Retained lane coupling must preserve signed g < 0")
        cutoff = 64 * delta
        j = hard_gap_coefficient(delta, cutoff, radius)
        prediction = hard_gap_second_order(delta, coupling, cutoff, radius)
        compatible = retained.contains(prediction)
        passed = j.lower > 0 and prediction.upper < delta.lower and compatible
        difference = retained - prediction
        lanes.append({"pair": lane["pair"], "status": "PASS" if passed else "FAIL",
                      "J_coefficient": display_interval(j),
                      "second_order_gap": display_interval(prediction),
                      "second_order_delay": display_interval(delta - prediction),
                      "retained_exact_hard_gap": display_interval(retained),
                      "retained_gap_contains_second_order_interval": compatible,
                      "retained_minus_second_order_gap": display_interval(difference),
                      "retained_minus_second_order_gap_over_g4": display_interval(
                          difference / coupling ** 4)})
    fixture = convergence_fixture(precision)
    passed = all(lane["status"] == "PASS" for lane in lanes) and fixture["status"] == "PASS"
    return {"schema": "SAM_CHAPTER1_SECOND_ORDER_DIAGNOSTIC_V1",
            "status": "PASS" if passed else "FAIL",
            "scope": "Independent second-order hard-branch coefficient check and separate finite-mode convergence fixture",
            "interpretation": "The exact coefficient integral is enclosed over the complete hard continuum. Its g^2 prediction is compatible with the retained hard-gap enclosure; no continuum O(g^4) remainder bound is claimed. The numerical O(g^4) convergence check concerns only the declared synthetic finite-mode fixture.",
            "continuum_lanes": lanes, "finite_mode_convergence": numerical_json(fixture, precision)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=70)
    parser.add_argument("--inputs", type=Path, default=ROOT / "data/chapter1_certificate.json")
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence/native")
    parser.add_argument("--output", type=Path, default=ROOT / "build/second_order.json")
    args = parser.parse_args(argv)
    try:
        if args.precision < 40:
            raise ValueError("--precision must be at least 40")
        packet = json.loads(args.inputs.read_text())
        bindings = verify_packet_bindings(packet, args.evidence)
        report = diagnose(packet, args.precision)
        report["input_sha256"] = sha256(args.inputs)
        report["source_bindings"] = packet["source_bindings"]
        report["bindings"] = bindings
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"{report['status']}: six second-order hard-gap comparisons and two-polarization O(g^4) fixture")
        print(f"Wrote {args.output}")
        return 0 if report["status"] == "PASS" else 1
    except (CertificateError, ValueError, KeyError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
