#!/usr/bin/env python3
"""Replay the unchanged original checker against hash-bound retained evidence.

This runs no GEN6 Duck engine and starts no new scientific campaign. The only
adaptation to the preserved checker is its Path constructor: historical source
paths resolve through the checked relocation manifest, never the local host.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "evidence/MANIFEST.json"
SCHEMA = "SAM_CHAPTER1_PORTABLE_EVIDENCE_V1"
EXPECTED = {
    "receipt_count": 9,
    "trace_outputs": 300,
    "verified_matrix_readouts": 134,
    "checks": 23804,
    "passed_checks": 23804,
    "status": "PASS",
}


class EvidenceError(ValueError):
    """The retained package is missing, changed, or not safely relocatable."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def portable_path(root: Path, relative: str, *, must_exist: bool = True) -> Path:
    """Resolve one repository-relative POSIX path without traversal/symlinks."""
    if not isinstance(relative, str) or not relative:
        raise EvidenceError("A nonempty repository-relative path is required")
    parts = PurePosixPath(relative)
    if (
        parts.is_absolute()
        or ".." in parts.parts
        or "\\" in relative
        or ":" in relative
        or relative != parts.as_posix()
    ):
        raise EvidenceError(f"Unsafe repository-relative path: {relative!r}")
    candidate = root.joinpath(*parts.parts)
    current = root
    for part in parts.parts:
        current = current / part
        if current.is_symlink():
            raise EvidenceError(f"Evidence/output path contains a symlink: {relative}")
    resolved = candidate.resolve(strict=must_exist)
    if not resolved.is_relative_to(root.resolve()):
        raise EvidenceError(f"Path leaves the repository: {relative}")
    return resolved


def load_evidence(root: Path = REPO_ROOT) -> tuple[dict[str, Any], dict[str, Path]]:
    """Validate every exported byte and return the historical path resolver."""
    root = root.resolve()
    manifest_path = portable_path(root, MANIFEST)
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema") != SCHEMA:
        raise EvidenceError("Unrecognized evidence manifest schema")
    if manifest.get("expected") != EXPECTED:
        raise EvidenceError("Manifest does not identify the Chapter I check scope")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise EvidenceError("Evidence artifact inventory is absent")
    local_paths: set[str] = set()
    relocation: dict[str, Path] = {}
    for entry in artifacts:
        relative = entry["path"]
        if not relative.startswith("evidence/native/"):
            raise EvidenceError(f"Artifact outside the native evidence tree: {relative}")
        if relative in local_paths or entry["original_path"] in relocation:
            raise EvidenceError(f"Duplicate artifact mapping: {relative}")
        local = portable_path(root, relative)
        if not local.is_file():
            raise EvidenceError(f"Retained artifact is not a regular file: {relative}")
        if local.stat().st_size != entry["bytes"] or sha256(local) != entry["sha256"]:
            raise EvidenceError(f"Retained artifact does not match SHA-256/bytes: {relative}")
        original = entry["original_path"]
        if not isinstance(original, str) or not PurePosixPath(original).is_absolute():
            raise EvidenceError(f"Original provenance path must be absolute: {relative}")
        local_paths.add(relative)
        relocation[original] = local
    actual_paths = set()
    for path in portable_path(root, "evidence/native").rglob("*"):
        if path.is_symlink():
            raise EvidenceError(f"Native evidence contains a symlink: {path.relative_to(root)}")
        if path.is_file():
            actual_paths.add(path.relative_to(root).as_posix())
    if actual_paths != local_paths:
        raise EvidenceError("Native evidence files differ from the complete portable inventory")

    # The original checker joins trace filenames onto these historical roots.
    # Each root is accepted only when its exact files were verified above.
    for entry in manifest.get("directories", []):
        original, relative = entry["original_path"], entry["path"]
        local = portable_path(root, relative)
        if not local.is_dir() or original in relocation:
            raise EvidenceError(f"Invalid/duplicate directory relocation: {relative}")
        members = [p for p in local_paths if p.startswith(relative + "/")]
        if not members:
            raise EvidenceError(f"Relocation directory has no retained files: {relative}")
        for member in members:
            source = original + member[len(relative):]
            if relocation.get(source) != root / member:
                raise EvidenceError(f"Directory relocation disagrees with file proof: {member}")
        relocation[original] = local

    receipts = manifest.get("receipt_index", [])
    actual_receipts = {
        p.relative_to(root).as_posix()
        for p in portable_path(root, manifest["local_run"]).glob("workers/*/tasks/*/RESULT.json")
    }
    if len(receipts) != EXPECTED["receipt_count"] or {e["path"] for e in receipts} != actual_receipts:
        raise EvidenceError("Receipt inventory does not match the original nine tasks")
    total_traces = 0
    for item in receipts:
        receipt = json.loads(portable_path(root, item["path"]).read_text())
        if receipt.get("key") != item["key"]:
            raise EvidenceError(f"Receipt task key mismatch: {item['path']}")
        original_root = receipt["gen6_execution_path"]
        if original_root not in relocation:
            raise EvidenceError(f"Unmapped original trace root: {original_root}")
        trace = receipt["gen6_execution"]["trace"]
        if len(trace) != item["trace_outputs"]:
            raise EvidenceError("Receipt trace count differs from portable index")
        for step in trace:
            for kind in ("input", "output"):
                name = step[kind]
                # The strict helper rejects absolute/traversing trace names.
                local = portable_path(root, relocation[original_root].relative_to(root).as_posix() + "/" + name)
                historical = original_root + "/" + name
                if historical not in relocation or relocation[historical] != local:
                    raise EvidenceError(f"Trace is absent from relocation inventory: {historical}")
                if sha256(local) != step[kind + "_sha256"]:
                    raise EvidenceError(f"Receipt trace hash mismatch: {historical}")
        total_traces += len(trace)
    if total_traces != EXPECTED["trace_outputs"]:
        raise EvidenceError("Trace scope differs from the original 300 operations")
    return manifest, relocation


def path_resolver(root: Path, manifest: dict[str, Any], relocation: dict[str, Path], output: Path):
    """Return the strict Path adapter used by the unmodified original checker."""
    retained = {e["path"] for e in manifest["artifacts"]}

    def relocated_path(*parts: Any) -> Path:
        requested = Path(*parts)
        historical = str(requested)
        if historical in relocation:
            return relocation[historical]
        local = requested if requested.is_absolute() else root / requested
        local = local.resolve()
        if not local.is_relative_to(root):
            raise EvidenceError(f"No hash-bound relocation for historical source path: {historical}")
        relative = local.relative_to(root).as_posix()
        if local == output:
            return output
        if relative not in retained and relative != manifest["local_run"]:
            raise EvidenceError(f"Original checker requested an unlisted local input: {relative}")
        return portable_path(root, relative)

    return relocated_path


def replay(output: Path, precision: int, root: Path = REPO_ROOT) -> dict[str, Any]:
    """Invoke original checker code after strict, complete evidence validation."""
    root = root.resolve()
    manifest, relocation = load_evidence(root)
    output = output if output.is_absolute() else root / output
    if not output.is_relative_to(root):
        raise EvidenceError("Choose an output within this repository, such as build/native_verification.json")
    output = portable_path(root, output.relative_to(root).as_posix(), must_exist=False)
    if output.is_relative_to(root / "evidence"):
        raise EvidenceError("Verification reports must not overwrite retained evidence")
    checker_path = portable_path(root, manifest["checker"])
    spec = importlib.util.spec_from_file_location("sam_retained_original_independent", checker_path)
    if spec is None or spec.loader is None:
        raise EvidenceError("Cannot load retained independent checker")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    previous_bytecode = sys.dont_write_bytecode
    try:
        # Keep the retained evidence tree byte-for-byte read-only during replay.
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous_bytecode

    # Source file bytes, formulas, checks, arithmetic and reporting are intact.
    module.Path = path_resolver(root, manifest, relocation, output)
    argv = sys.argv
    try:
        sys.argv = [str(checker_path), "--run", str(root / manifest["local_run"]),
                    "--inputs", str(root / manifest["inputs"]),
                    "--output", str(output), "--precision", str(precision)]
        code = module.main()
    finally:
        sys.argv = argv
    report = json.loads(output.read_text())
    if code or any(report.get(key) != value for key, value in EXPECTED.items()):
        raise EvidenceError("Original checker did not reproduce its complete PASS scope; inspect the report")
    if report.get("failed_checks") or report.get("unsupported_new_readouts") or report.get("unsupported_trace_outputs"):
        raise EvidenceError("Original checker returned failures or unsupported evidence")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "build/native_verification.json")
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument("--integrity-only", action="store_true", help="Check retained bytes/path mappings without numerical replay")
    args = parser.parse_args()
    if args.precision < 100:
        parser.error("--precision must be at least 100 decimal digits")
    try:
        if args.integrity_only:
            manifest, _ = load_evidence()
            print(json.dumps({"status": "PASS", "artifacts": len(manifest["artifacts"]),
                              "bytes": sum(e["bytes"] for e in manifest["artifacts"]),
                              "scope": "Portable evidence integrity and relocation only"}, sort_keys=True))
        else:
            output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
            replay(output, args.precision)
    except (EvidenceError, OSError, KeyError, TypeError, ImportError, json.JSONDecodeError) as exc:
        print(f"Evidence verification failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
