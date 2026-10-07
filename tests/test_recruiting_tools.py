from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_ats_resume import build, load_profile  # noqa: E402
from build_tracker import load_rows, write_markdown, write_xlsx  # noqa: E402
from scaffold_application import scaffold  # noqa: E402


class RecruitingToolsTest(unittest.TestCase):
    def test_scaffold_is_additive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            folder = scaffold(Path(temporary), "Example/Company", "Analyst: 2027", ROOT / "templates")
            self.assertEqual(folder.name, "Example-Company - Analyst- 2027")
            note = folder / "01-JD.md"
            note.write_text("preserve me", encoding="utf-8")
            scaffold(Path(temporary), "Example/Company", "Analyst: 2027", ROOT / "templates")
            self.assertEqual(note.read_text(encoding="utf-8"), "preserve me")

    def test_tracker_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "records.json"
            source.write_text((ROOT / "templates" / "applications.example.json").read_text(encoding="utf-8"), encoding="utf-8")
            rows = load_rows(source)
            write_markdown(rows, root / "tracker.md")
            write_xlsx(rows, root / "tracker.xlsx")
            self.assertEqual(len(rows), 2)
            self.assertTrue((root / "tracker.xlsx").stat().st_size > 0)
            self.assertIn("Example Company", (root / "tracker.md").read_text(encoding="utf-8"))

    def test_resume_is_one_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile = load_profile(ROOT / "templates" / "applicant-profile.example.json")
            output = root / "resume.pdf"
            build(profile, output)
            content = output.read_bytes()
            self.assertTrue(content.startswith(b"%PDF"))
            self.assertEqual(content.count(b"/Type /Page\n"), 1)

    def test_invalid_tracker_row_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "bad.json"
            source.write_text(json.dumps([{"company": "Example", "role": "", "status": "ready"}]), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_rows(source)


if __name__ == "__main__":
    unittest.main()
