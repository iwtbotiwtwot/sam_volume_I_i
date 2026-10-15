"""Integrity/relocation failures use tiny fixtures; numerical replay is separate."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts import verify_native as native


class NativeEvidenceTests(unittest.TestCase):
    def test_complete_retained_package_integrity(self):
        manifest, relocation = native.load_evidence()
        self.assertEqual(len(manifest["artifacts"]), 615)
        self.assertEqual(sum(x["bytes"] for x in manifest["artifacts"]), 18677823)
        self.assertEqual(len(manifest["receipt_index"]), 9)
        self.assertEqual(sum(x["trace_outputs"] for x in manifest["receipt_index"]), 300)
        self.assertEqual(len(relocation), 624)

    def tiny_package(self, root):
        relative = "evidence/native/example.json"
        data = b'{"retained": true}\n'
        file = root / relative
        file.parent.mkdir(parents=True)
        file.write_bytes(data)
        manifest = {
            "schema": native.SCHEMA,
            "expected": native.EXPECTED,
            "artifacts": [{"path": relative, "original_path": "/historical/example.json",
                           "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}],
        }
        (root / native.MANIFEST).write_text(json.dumps(manifest))
        return file, manifest

    def test_changed_retained_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file, _ = self.tiny_package(root)
            file.write_bytes(b"changed")
            with self.assertRaisesRegex(native.EvidenceError, "SHA-256/bytes"):
                native.load_evidence(root)

    def test_missing_retained_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file, _ = self.tiny_package(root)
            file.unlink()
            with self.assertRaises(FileNotFoundError):
                native.load_evidence(root)

    def test_manifest_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, manifest = self.tiny_package(root)
            manifest["artifacts"][0]["path"] = "evidence/native/../../../escape.json"
            (root / native.MANIFEST).write_text(json.dumps(manifest))
            with self.assertRaisesRegex(native.EvidenceError, "Unsafe"):
                native.load_evidence(root)

    def test_absolute_and_noncanonical_portable_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("/tmp/example", "../example", "a/../example", "a//b", "a\\b", "C:/example"):
                with self.subTest(path=name):
                    with self.assertRaises(native.EvidenceError):
                        native.portable_path(root, name, must_exist=False)

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            external = Path(directory) / "external"
            external.mkdir()
            (root / "escape").symlink_to(external, target_is_directory=True)
            with self.assertRaisesRegex(native.EvidenceError, "symlink"):
                native.portable_path(root, "escape/file.json", must_exist=False)

    def test_unknown_historical_path_has_no_host_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            outside = Path(directory) / "existing-host-file.json"
            outside.write_text("This must not be read as scientific evidence")
            resolver = native.path_resolver(root, {"artifacts": [], "local_run": "run"}, {}, root / "build/result.json")
            with self.assertRaisesRegex(native.EvidenceError, "No hash-bound relocation"):
                resolver(outside)

    def test_unlisted_local_input_has_no_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file = root / "unlisted.json"
            file.write_text("{}")
            resolver = native.path_resolver(root, {"artifacts": [], "local_run": "run"}, {}, root / "build/result.json")
            with self.assertRaisesRegex(native.EvidenceError, "unlisted local input"):
                resolver(file)

    def test_known_historical_path_resolves_to_verified_local_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            local = root / "retained.json"
            local.write_text("{}")
            resolver = native.path_resolver(root, {"artifacts": [{"path": "retained.json"}], "local_run": "run"},
                                            {"/historical/retained.json": local}, root / "build/result.json")
            self.assertEqual(resolver("/historical/retained.json"), local)


if __name__ == "__main__":
    unittest.main()
