"""Placement incidence tests and explicitly synthetic signed-ledger controls."""

import copy
from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sam_chapter1.placements import (PLACEMENT_CODES, bundled_response_bytes,
                                     chapter_source, decode_placement,
                                     encode_placement, generate_boundary,
                                     generate_source, is_cube_path, response_return)
# Independent completed operands transcribed from the unchanged original source
# derivation, never imported from the generator or its downstream consumers.
T = ((84, 8, 8, 0), (8, 84, 0, 0), (8, 0, 84, 8), (0, 0, 8, 84))
K = ((672, 96, 32, 0), (96, 2016, 0, 0),
     (32, 0, 672, 32), (0, 0, 32, 672))


def synthetic_input():
    """A declared three-slot fixture, never an alleged original Li7 ledger."""
    actions = []
    for u in range(8):
        for bit, axis in ((1, "X"), (2, "Y"), (4, "Z")):
            v = u ^ bit
            for choice in ("FORWARD", "REVERSE"):
                sigma = 1 if choice == "FORWARD" else -1
                sign = (1 if u < v else -1) * sigma
                actions.append({"source_site": u, "target_site": v,
                                "action": choice, "sigma_chi": sigma,
                                "octahedral_vertex": axis + ("+" if sign == 1 else "-")})
    def index(u, v, choice):
        return next(i for i, a in enumerate(actions)
                    if (a["source_site"], a["target_site"], a["action"]) == (u, v, choice))
    sites = (0, 1, 3)
    ledger = {"objects": [{"role": i, "site": s, "kind": kind}
                           for i, (s, kind) in enumerate(zip(sites, ("proton", "neutron", "proton")))],
              "cycles": [{"u": i, "v": i + 1, "edge": i,
                          "forward": index(sites[i], sites[i + 1], "FORWARD" if i == 0 else "REVERSE"),
                          "reverse": index(sites[i + 1], sites[i], "REVERSE" if i == 0 else "FORWARD")}
                         for i in range(2)]}
    source = {"actions": actions, "edges": [{"u": 0, "v": 1, "J": 2},
                                             {"u": 1, "v": 2, "J": 3}]}
    return source, ledger, (encode_placement(sites), encode_placement((0, 1, 5)))


class PlacementBoundaryTests(unittest.TestCase):
    def test_original_base_eight_paths_roundtrip(self):
        paths = ((0, 1, 3, 2, 6, 4, 5), (0, 1, 3, 2, 6, 7, 5),
                 (0, 1, 3, 7, 6, 4, 5), (0, 2, 3, 7, 6, 4, 5))
        self.assertEqual(tuple(map(decode_placement, PLACEMENT_CODES)), paths)
        self.assertEqual(tuple(map(encode_placement, paths)), PLACEMENT_CODES)
        self.assertTrue(all(map(is_cube_path, paths)))

    def test_original_boundary_matches_independent_bit_distance_construction(self):
        source = generate_boundary()
        columns = tuple(sorted({code ^ (1 << bit)
                                for code in PLACEMENT_CODES for bit in range(21)}))
        b = tuple(tuple(-2 if (code ^ target).bit_count() == 1 else 0
                        for target in columns) for code in PLACEMENT_CODES)
        self.assertEqual(source.target_codes, columns)
        self.assertEqual(source.B, b)
        self.assertEqual(len(columns), 78)
        self.assertEqual(source.T, T)
        self.assertEqual([sum(value != 0 for value in row) for row in b], [21] * 4)
        self.assertEqual({value for row in b for value in row}, {-2, 0})
        # These collisions retain labelled ambient target identity.
        intersections = [[sum(x != 0 and y != 0 for x, y in zip(a, b))
                          for b in source.B] for a in source.B]
        self.assertEqual(intersections, [[21, 2, 2, 0], [2, 21, 0, 0],
                                         [2, 0, 21, 2], [0, 0, 2, 21]])

    def test_order_and_subcomponents_are_preserved(self):
        codes = tuple(reversed(PLACEMENT_CODES))
        self.assertEqual(generate_boundary(codes).T, tuple(tuple(reversed(row)) for row in reversed(T)))
        self.assertEqual(generate_boundary((PLACEMENT_CODES[0],)).T, ((84,),))

    def test_invalid_paths_and_lossy_operands_are_rejected(self):
        for code in (-1, 8 ** 7, 0):
            with self.assertRaises(ValueError):
                generate_boundary((code,))
        for code in (True, 46501.0, "46501"):
            with self.assertRaises(TypeError):
                decode_placement(code)
        for codes in ((), (46501, 46501)):
            with self.assertRaises(ValueError):
                generate_boundary(codes)
        with self.assertRaises(ValueError):
            encode_placement((0, 1, 8))

    def test_missing_response_is_explicit_in_command_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            process = subprocess.run([sys.executable, str(ROOT / "scripts/generate_source.py"), "--boundary-only",
                                      "--output", str(Path(temporary) / "boundary.json")],
                                     capture_output=True, text=True, check=True)
        output = json.loads(process.stdout)
        self.assertIsNone(output["K"])
        self.assertIn("NOT_CONSTRUCTED", output["response_status"])
        self.assertEqual(output["T"], [list(row) for row in T])


class SignedResponseTests(unittest.TestCase):
    def test_bundled_operand_authentication_rejects_changed_bytes(self):
        with patch("sam_chapter1.placements.files") as resources:
            resources.return_value.joinpath.return_value.read_bytes.return_value = b"{}"
            with self.assertRaisesRegex(ValueError, "operand changed"):
                chapter_source()

    def test_recovered_chapter_ledger_reconstructs_retained_completed_k(self):
        result = chapter_source()
        self.assertEqual(result.boundary.T, T)
        self.assertEqual(result.K, K)
        self.assertEqual(result.boundary.codes, PLACEMENT_CODES)
        self.assertEqual(result.responses, ((2, 0, -2), (2, 2, -4), (2, 2, 0), (0, 2, 2)))
        # All channel-weighted forbidden incidences independently factor K.
        b, d = result.boundary.B, result.responses
        factored = tuple(tuple(sum(b[i][c] * d[i][a] * b[j][c] * d[j][a]
                                   for a in range(3) for c in range(78))
                               for j in range(4)) for i in range(4))
        self.assertEqual(factored, K)

    def test_default_command_regenerates_complete_chapter_operand(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "source.json"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/generate_source.py"),
                                     "--output", str(output)], capture_output=True, text=True, check=True)
            record = json.loads(result.stdout)
            self.assertEqual(record, json.loads(output.read_text()))
            self.assertEqual(record["K"], [list(row) for row in K])
            self.assertEqual(record["response_status"], "GENERATED_FROM_EXPLICIT_SOURCE_AND_LEDGER")
            self.assertEqual(record["response_provenance"]["selected_ledger"]["template_id"],
                             "00828cbc571003430a27ec44758e76bb6c3bb02344a73dec72a0a783a2da567f")

    def test_recovered_chapter_source_controls_keep_signed_provenance(self):
        packet = json.loads(bundled_response_bytes())
        source, ledger = packet["source"], packet["ledger"]
        original = chapter_source()
        q = tuple(1 if obj["kind"] == "proton" else -1 for obj in ledger["objects"])
        self.assertEqual(q, (1, -1, -1, -1, 1, -1, 1))
        mirror = generate_source(source, ledger, charges=tuple(-x for x in q))
        self.assertEqual(mirror.responses, tuple(tuple(-v for v in row) for row in original.responses))
        self.assertEqual(mirror.K, K)
        self.assertEqual(generate_source(source, ledger, mode="reciprocal").responses, original.responses)
        self.assertEqual(generate_source(source, ledger, charges=(1,) * 7).K, ((0,) * 4,) * 4)
        self.assertNotEqual(generate_source(source, ledger, mode="erase_sign").K, K)

    def test_transported_actions_outside_original_connectors_retain_reciprocals(self):
        packet = json.loads(bundled_response_bytes())
        original = chapter_source()
        selected = {cycle[key] for cycle in packet["ledger"]["cycles"]
                    for key in ("forward", "reverse")}
        transported = {term[1] for row in original.witnesses for term in row}
        # Action 43 is transported to a retained placement but is absent from
        # every original connector pair; its sign changes the resulting K.
        self.assertIn(43, transported - selected)
        for change in ("sigma", "axis", "vertex_sign"):
            source = copy.deepcopy(packet["source"])
            action = source["actions"][43]
            if change == "sigma":
                action["sigma_chi"] *= -1
            elif change == "axis":
                action["octahedral_vertex"] = "Y+"
            else:
                vertex = action["octahedral_vertex"]
                action["octahedral_vertex"] = vertex[0] + ("-" if vertex[1] == "+" else "+")
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "transported reciprocal"):
                generate_source(source, packet["ledger"])

    def test_explicit_fixture_exact_responses_and_k(self):
        source, ledger, codes = synthetic_input()
        result = generate_source(source, ledger, codes)
        self.assertEqual(result.responses, ((4, -6, 0), (4, 0, -6)))
        self.assertEqual(result.boundary.T, ((36, 8), (8, 36)))
        self.assertEqual(result.K, ((1872, 128), (128, 1872)))
        # Check the separate channel factorization, not only the dot-product routine.
        factored = [[sum(result.boundary.B[i][column] * result.responses[i][axis] *
                         result.boundary.B[j][column] * result.responses[j][axis]
                         for axis in range(3) for column in range(len(result.boundary.target_codes)))
                     for j in range(2)] for i in range(2)]
        self.assertEqual(factored, [list(row) for row in result.K])

    def test_mirror_reciprocal_and_species_erasure_controls(self):
        source, ledger, codes = synthetic_input()
        original = generate_source(source, ledger, codes)
        mirrored = generate_source(source, ledger, codes, (-1, 1, -1))
        self.assertEqual(mirrored.responses, tuple(tuple(-x for x in row) for row in original.responses))
        self.assertEqual(mirrored.K, original.K)
        self.assertEqual(generate_source(source, ledger, codes, mode="reciprocal").responses, original.responses)
        self.assertEqual(generate_source(source, ledger, codes, (1, 1, 1)).K, ((0, 0), (0, 0)))
        self.assertNotEqual(generate_source(source, ledger, codes, mode="erase_sign").responses, original.responses)

    def test_changed_sign_j_and_fractional_operand_reach_generated_matrix(self):
        source, ledger, codes = synthetic_input()
        source["edges"][0]["J"] = "1/2"
        result = generate_source(source, ledger, codes)
        self.assertEqual(result.responses, ((F(1), -6, 0), (F(1), 0, -6)))
        self.assertEqual(result.K[0][1], 8)
        self.assertNotEqual(result.K, ((1872, 128), (128, 1872)))

    def test_source_identity_and_unavailable_ledger_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "requires the original"):
            generate_source(None, None)
        source, ledger, codes = synthetic_input()
        for change in ("sigma", "role", "action", "duplicate", "connectivity", "float"):
            s, l = copy.deepcopy(source), copy.deepcopy(ledger)
            if change == "sigma":
                s["actions"][l["cycles"][0]["reverse"]]["sigma_chi"] *= -1
            elif change == "role":
                l["objects"][1]["role"] = 7
            elif change == "action":
                s["actions"].pop()
            elif change == "duplicate":
                s["actions"][0] = copy.deepcopy(s["actions"][1])
            elif change == "connectivity":
                l["cycles"].pop()
            elif change == "float":
                s["edges"][0]["J"] = 0.5
            with self.subTest(change=change), self.assertRaises((ValueError, TypeError)):
                generate_source(s, l, codes)

    def test_response_channel_validation(self):
        for t, d in ((T, ((1, 2, 3),)), (((1, 2), (0, 1)), ((1, 2, 3),) * 2),
                     (((1,),), ((1, 2),)), (((1,),), ((1.0, 2, 3),))):
            with self.assertRaises((ValueError, TypeError)):
                response_return(t, d)


if __name__ == "__main__":
    unittest.main()
