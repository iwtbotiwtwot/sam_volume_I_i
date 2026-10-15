"""Source-bound, exact scalar replay of the six Chapter I clock certificates.

The hard-branch M, Omega and Kprep bounds are imported hypotheses.  This code
independently propagates their consequences through E(T), F_T, weighted Duhamel
and the centered rate inequality.  It checks the outward printed intervals;
it does not reproduce the native hard eigenbranch certificate or domain proof.
"""

import hashlib
import json
from pathlib import Path
from fractions import Fraction as F

from .intervals import Interval as IV, decimal_outward, expm1, pi_interval, sqrt
from .reference import (EPSILON, KAPPA, K, PAIRS, T, root_count,
                        shifted_source_polynomial, source_matrix)


CLOCK_FIELDS = (
    "epsilon", "Delta", "g", "R", "mu", "counterterm", "Kprep",
    "M_lower", "M_upper", "actual_initial_rate", "CYCLE_E", "vsoft", "time_CYCLE",
)


class CertificateError(ValueError):
    """A hypothesis, binding or displayed conclusion failed validation."""


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_pointer(document, pointer):
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        document = document[int(part)] if isinstance(document, list) else document[part]
    return document


def _exact_real_matrix(matrix):
    result = []
    for row in matrix["entries"]:
        result_row = []
        for cell in row:
            real, imaginary = IV.from_json(cell["re"]), IV.from_json(cell["im"])
            if real.lower != real.upper or imaginary != IV.point(0):
                raise CertificateError("Expected an exact real finite-source matrix")
            result_row.append(str(real.lower))
        result.append(result_row)
    return result


def _real_diagonal(matrix):
    return [row[i]["re"] for i, row in enumerate(matrix["entries"])]


def extract_packet(evidence_root):
    """Extract compact operands without changing the source evidence bytes."""
    evidence_root = Path(evidence_root)
    files = {"exact_inputs": evidence_root / "sources/EXACT_INPUTS.json",
             "results": evidence_root / "RESULTS.json"}
    source = {key: json.loads(path.read_text()) for key, path in files.items()}
    exact, results = source["exact_inputs"], source["results"]
    packet = {
        "schema": "SAM_CHAPTER1_SCALAR_CERTIFICATE_V1",
        "scope": "Six separately prepared coherent hard-branch lanes; 0<=tau<=573049*pi; normalized model-time chart.",
        "hard_inputs": "Retained certified hard eigenbranch gap, amplitude and preparation-energy bounds; no hard-state solver in this independent reconstruction.",
        "source_bindings": {key: {"path": path.relative_to(evidence_root).as_posix(),
                                    "sha256": sha256(path)} for key, path in files.items()},
        "matrices": {key: _exact_real_matrix(exact[key]) for key in ("T", "K", "Q")},
        "q": _real_diagonal(exact["q"]),
        "lanes": [], "bindings": [],
    }
    for key in ("T", "K", "Q"):
        packet["bindings"].append({"packet_pointer": "/matrices/" + key,
                                    "source": "exact_inputs", "source_pointer": "/" + key,
                                    "transform": "exact_real_matrix"})
    packet["bindings"].append({"packet_pointer": "/q", "source": "exact_inputs",
                                "source_pointer": "/q", "transform": "real_diagonal"})
    for index, pair in enumerate(PAIRS):
        clock = {key: exact["clock_outputs"][key]["entries"][index][index]["re"]
                 for key in CLOCK_FIELDS}
        packet["lanes"].append({"pair": list(pair), "clock": clock,
                                  "certificate": results["lanes"][index]})
        for key in CLOCK_FIELDS:
            packet["bindings"].append({
                "packet_pointer": f"/lanes/{index}/clock/{key}", "source": "exact_inputs",
                "source_pointer": f"/clock_outputs/{key}/entries/{index}/{index}/re"})
        packet["bindings"].append({"packet_pointer": f"/lanes/{index}/certificate",
                                    "source": "results", "source_pointer": f"/lanes/{index}"})
    return packet


def verify_packet_bindings(packet, evidence_root):
    """Reject edited compact operands even if their conclusions still happen to hold."""
    evidence_root = Path(evidence_root).resolve()
    documents = {}
    for key, binding in packet["source_bindings"].items():
        path = (evidence_root / binding["path"]).resolve()
        if not path.is_relative_to(evidence_root):
            raise CertificateError("Evidence binding escapes its declared root")
        if sha256(path) != binding["sha256"]:
            raise CertificateError(f"Evidence SHA-256 mismatch: {binding['path']}")
        documents[key] = json.loads(path.read_text())
    count = 0
    for binding in packet["bindings"]:
        original = json_pointer(documents[binding["source"]], binding["source_pointer"])
        transform = binding.get("transform")
        if transform == "exact_real_matrix":
            original = _exact_real_matrix(original)
        elif transform == "real_diagonal":
            original = _real_diagonal(original)
        elif transform is not None:
            raise CertificateError("Unknown evidence transform")
        if json_pointer(packet, binding["packet_pointer"]) != original:
            raise CertificateError(f"Changed operand at {binding['packet_pointer']}")
        count += 1
    # Re-extraction also validates the complete expected field set: deleting a
    # binding must not turn a changed operand into an unbound accepted value.
    expected = extract_packet(evidence_root)
    if packet != expected:
        raise CertificateError("Compact packet does not match complete source-bound extraction")
    return {"status": "PASS", "checked_bindings": count,
            "source_files": len(documents)}


def _require(condition, message):
    if not condition:
        raise CertificateError(message)


def _clock(lane, name):
    return IV.from_json(lane["clock"][name])


def replay_lane(lane, q, bits=512):
    """Rigorous scalar consequences; returned endpoints are rational brackets."""
    pair = tuple(lane["pair"])
    _require(pair in PAIRS, "Unknown spectral lane")
    a, b = pair
    epsilon = IV.point(EPSILON)
    delta = 2 * epsilon
    cutoff = 64 * delta
    radius = _clock(lane, "R")
    g = _clock(lane, "g")
    gap = _clock(lane, "actual_initial_rate")
    ml = _clock(lane, "M_lower").lower
    kp = _clock(lane, "Kprep")
    _require(radius.lower > 0 and g.upper < 0, "Require positive R and signed g<0 for a<b")
    _require(0 < gap.lower <= gap.upper < delta.lower, "Require 0<Omega<Delta")
    _require(0 < ml <= 1 and kp.lower >= 0, "Invalid hard preparation bounds")
    for key, exact in (("epsilon", epsilon), ("Delta", delta)):
        _require(_clock(lane, key).contains(exact), f"Normalized {key} mismatch")
    qdiff = IV.from_json(q[a]) - IV.from_json(q[b])
    _require(g.contains(epsilon * qdiff), "Coupling does not enclose signed source-root incidence")
    mu = 1 / (4 * radius)
    c = 2 * (g ** 2) * mu
    time = pi_interval(bits) / epsilon
    # The inherited vsoft is itself an upper bound. Reconstructing the stated
    # Bessel-tail expression gives another rigorous bound. Their maximum keeps
    # this replay conservative with respect to both retained representations.
    vsoft_formula = radius ** 4 * cutoff ** 6 / (675 * KAPPA * pi_interval(bits))
    vsoft_native = _clock(lane, "vsoft")
    _require(vsoft_formula.overlaps(vsoft_native), "Soft bound differs from retained receiving law")
    vsoft = IV(min(vsoft_formula.lower, vsoft_native.lower),
               max(vsoft_formula.upper, vsoft_native.upper))
    _require(mu.overlaps(_clock(lane, "mu")), "mu does not match 1/(4R)")
    _require(c.overlaps(_clock(lane, "counterterm")), "Both-current counterterm mismatch")
    _require(time.overlaps(_clock(lane, "time_CYCLE")), "Retained time differs from one bare cycle")
    norm_margin = F(3, 2) - 2 * epsilon - 3 * c
    _require(norm_margin.lower > 0, "Weighted evolution comparison hypothesis failed")
    exponent = 4 * g ** 2 * vsoft * time ** 2
    error = expm1(exponent, bits)
    # CYCLE_E is retained separately. Its exact native input arithmetic is
    # replayed by the original checker; here we require overlap with a direct
    # receiving-law calculation and take the larger upper endpoint.
    error_native = _clock(lane, "CYCLE_E")
    _require(error.overlaps(error_native), "Whole-cycle source error mismatch")
    error_upper = max(error.upper, error_native.upper)
    error_bound = IV(min(error.lower, error_native.lower), error_upper)
    field = (sqrt(c, bits) + sqrt(kp + epsilon * error_bound, bits)) ** 2
    w = 8 * g.absolute() * time * sqrt(mu * vsoft * (1 + field) * (1 + field + cutoff), bits)
    amplitude_lower = ml - error_upper
    _require(amplitude_lower > 0, "Actual amplitude can reach zero")
    w_display = F(lane["certificate"]["W_upper_display"])
    _require(w.upper <= w_display, "Displayed correlator bound rounds inward")
    # Use the printed upward-rounded correlator ceiling for an independently
    # checkable displayed rate certificate, including all endpoint slack.
    gabs = g.absolute().upper
    positive_margin = gap.lower * ml - delta.upper * error_upper - 2 * gabs * w_display
    _require(positive_margin > 0, "Centered sufficient condition failed")
    rho = ((delta.upper - gap.lower) * error_upper + 2 * gabs * w_display) / amplitude_lower
    rate = IV(gap.lower - rho, gap.upper + rho)
    printed = lane["certificate"]["rate_display_times_1e6"]
    printed_rate = IV(F(printed["lower"]) / 10 ** 6, F(printed["upper"]) / 10 ** 6)
    _require(printed_rate.contains(rate), "Displayed uniform rate rounds inward")
    _require(printed_rate.lower > 0 and printed_rate.upper < delta.lower,
             "Displayed rate is not strictly positive and below Delta")
    # Check summary/native enclosure bookkeeping as exact fractions as well.
    native_rate = IV.from_json(lane["certificate"]["actual_uniform_rate"])
    native_w = IV.from_json(lane["certificate"]["uniform_correlator_error"])
    _require(native_w.upper <= w_display, "Correlator display misses retained native enclosure")
    _require(printed_rate.contains(native_rate), "Rate display misses retained native enclosure")
    native_inverse = IV.from_json(lane["certificate"]["instantaneous_inverse"])
    _require(native_inverse.contains(native_rate.reciprocal()), "Retained reciprocal interval is inconsistent")
    return {
        "pair": list(pair), "status": "PASS",
        "time": time.as_json(), "vsoft": vsoft.as_json(), "source_error": error.as_json(),
        "field_energy": field.as_json(), "weighted_duhamel": w.as_json(),
        "norm_comparison_margin_lower": str(norm_margin.lower),
        "amplitude_lower": str(amplitude_lower),
        "centered_positive_margin_lower": str(positive_margin),
        "centered_rate_error_upper": str(rho),
        "independently_replayed_rate": rate.as_json(),
        "printed_rate": printed_rate.as_json(), "printed_rate_times_1e6": printed,
        "replayed_inverse_rate": rate.reciprocal().as_json(),
        "replayed_rate_outward_times_1e6": {
            "lower": decimal_outward(rate.lower * 10 ** 6, 12, "lower"),
            "upper": decimal_outward(rate.upper * 10 ** 6, 12, "upper")},
    }


def replay_certificate(packet, bits=512):
    _require(packet.get("schema") == "SAM_CHAPTER1_SCALAR_CERTIFICATE_V1", "Unknown packet schema")
    matrices = {"T": T, "K": K, "Q": source_matrix()}
    for name, exact in matrices.items():
        got = [[F(v) for v in row] for row in packet["matrices"][name]]
        _require(got == [list(row) for row in exact], f"Inherited {name} matrix mismatch")
    _require([tuple(lane["pair"]) for lane in packet["lanes"]] == list(PAIRS),
             "Require all six source lanes in declared order")
    roots = [IV.from_json(root) for root in packet["q"]]
    _require(len(roots) == 4, "Require four retained source roots")
    _require(all(left.upper < right.lower for left, right in zip(roots, roots[1:])),
             "Source-root intervals are not ordered and disjoint")
    polynomial = shifted_source_polynomial()
    counts = [root_count(polynomial, root.lower - 756, root.upper - 756) for root in roots]
    _require(counts == [1, 1, 1, 1], "Source-root bracket failed exact Sturm isolation")
    return {"status": "PASS", "method": "Exact Fraction endpoints; integer-isqrt square-root brackets; rational Taylor tail; Machin pi.",
            "sqrt_and_transcendental_bits": bits,
            "root_isolation": {"method": "Exact Sturm sign variation on the four retained root brackets", "roots_per_interval": counts},
            "conditional_inputs": "Retained source-root/radius and hard-branch gap, amplitude and preparation-energy enclosures.",
            "lanes": [replay_lane(lane, packet["q"], bits) for lane in packet["lanes"]]}
