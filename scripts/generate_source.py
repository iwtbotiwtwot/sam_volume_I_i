#!/usr/bin/env python3
"""Print the exact original-Write source construction as reviewable JSON."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sam_chapter1.placements import (PLACEMENT_CODES, bundled_response_bytes,
                                     generate_boundary, generate_source)


def exact_json(value):
    if isinstance(value, Fraction):
        return value.numerator if value.denominator == 1 else str(value)
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codes", nargs="+", type=int, default=PLACEMENT_CODES)
    parser.add_argument("--output", type=Path, default=ROOT / "build/source_generation.json",
                        help="Save generated JSON here (also printed to standard output)")
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--boundary-only", action="store_true",
                        help="Generate B and T; explicitly leave K unconstructed")
    choice.add_argument("--response-input", type=Path,
                        help="Original JSON with source, ledger and optional charges/mode")
    args = parser.parse_args()
    result = None
    if not args.boundary_only:
        raw = (args.response_input.read_bytes() if args.response_input
               else bundled_response_bytes())
        operand = json.loads(raw)
        result = generate_source(operand["source"], operand["ledger"], args.codes,
                                 operand.get("charges"), operand.get("mode", "original"))
        boundary = result.boundary
    else:
        boundary = generate_boundary(args.codes)
    output = {"schema": "SAM_ORIGINAL_WRITE_SOURCE_V1", "ordered_placement_codes": boundary.codes,
              "decoded_paths": boundary.paths, "boundary_target_codes": boundary.target_codes,
              "B": boundary.B, "T": boundary.T,
              "incidence_per_hop": -2,
              "physical_g_H": "UNASSIGNED"}
    if result is None:
        output.update(K=None, response_status="NOT_CONSTRUCTED: original source actions and selected connector ledger required")
    else:
        output.update(K=result.K, signed_responses=result.responses,
                      action_witnesses=result.witnesses,
                      response_status="GENERATED_FROM_EXPLICIT_SOURCE_AND_LEDGER",
                      response_input_sha256=hashlib.sha256(raw).hexdigest(),
                      mode=operand.get("mode", "original"))
        if "provenance" in operand:
            output["response_provenance"] = operand["provenance"]
    serialized = json.dumps(output, default=exact_json, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
