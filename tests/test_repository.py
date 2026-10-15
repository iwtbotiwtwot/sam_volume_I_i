"""The portable asset checks must reject changed or escaped scientific inputs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify_repository', ROOT/'scripts/verify_repository.py')
assets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assets)


class AssetIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'source.json').write_text('{"signed_coupling":-1}\n')
        b = (self.root/'source.json').read_bytes()
        self.entry = {'path':'source.json', 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
        self.write_manifest([self.entry])

    def write_manifest(self, entries):
        (self.root/'MANIFEST.json').write_text(json.dumps({'schema':'SAM_CHAPTER_I_PORTABLE_ASSETS_V1', 'files':entries}))

    def test_bound_source_verifies(self):
        self.assertEqual(assets.verify_assets(self.root)['files'], 1)

    def test_changed_signed_operand_is_rejected(self):
        (self.root/'source.json').write_text('{"signed_coupling":+1}\n')
        with self.assertRaisesRegex(ValueError, 'content mismatch'):
            assets.verify_assets(self.root)

    def test_missing_source_is_rejected(self):
        (self.root/'source.json').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing'):
            assets.verify_assets(self.root)

    def test_traversal_is_rejected(self):
        self.entry['path'] = '../source.json'
        self.write_manifest([self.entry])
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            assets.verify_assets(self.root)

    def test_duplicate_binding_is_rejected(self):
        self.write_manifest([self.entry,self.entry])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            assets.verify_assets(self.root)

    def test_all_repository_assets_verify(self):
        self.assertEqual(assets.verify_assets(ROOT)['status'], 'PASS')


if __name__ == '__main__':
    unittest.main()
