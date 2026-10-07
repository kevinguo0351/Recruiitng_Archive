import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_sensitive_content.py"
spec = importlib.util.spec_from_file_location("sensitive_check", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class SensitiveContentTest(unittest.TestCase):
    def test_allows_reserved_example_email(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.txt"
            path.write_text("applicant@example.test", encoding="utf-8")
            original = module.ROOT
            module.ROOT = Path(temp)
            try:
                self.assertEqual(module.scan([path], []), [])
            finally:
                module.ROOT = original

    def test_rejects_private_binary_suffix(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "resume.pdf"
            path.write_bytes(b"synthetic")
            original = module.ROOT
            module.ROOT = Path(temp)
            try:
                self.assertTrue(module.scan([path], []))
            finally:
                module.ROOT = original


if __name__ == "__main__":
    unittest.main()
