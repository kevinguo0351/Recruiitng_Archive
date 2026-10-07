import sqlite3
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app  # noqa: E402


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "test.db"
        self.connection = app.connect(self.db_path)
        app.migrate(self.connection)
        app.seed(self.connection)

    def tearDown(self):
        self.connection.close()
        self.tempdir.cleanup()

    def test_synthetic_applications_are_queryable(self):
        rows = app.list_applications(self.connection)
        self.assertEqual(2, len(rows))
        self.assertEqual(
            {"Example Analytics", "Demo Advisory Group"},
            {row["company"] for row in rows},
        )

    def test_status_filter(self):
        rows = app.list_applications(self.connection, "ready")
        self.assertEqual(1, len(rows))
        self.assertEqual("ready", rows[0]["status"])

    def test_summary_counts(self):
        result = app.summary(self.connection)
        self.assertEqual(2, result["total"])
        self.assertEqual(1, result["by_status"]["researching"])

    def test_foreign_keys_reject_orphan_job(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO jobs(company_id, title, location, job_url, track) "
                "VALUES (999, 'Orphan', 'Remote', 'https://example.invalid/orphan', 'Test')"
            )

    def test_seed_refuses_any_preexisting_domain_row(self):
        second = app.connect(Path(self.tempdir.name) / "partial.db")
        try:
            app.migrate(second)
            second.execute(
                "INSERT INTO candidates(public_alias, requires_future_sponsorship) VALUES (?, ?)",
                ("existing-private-record", 0),
            )
            second.commit()
            with self.assertRaises(RuntimeError):
                app.seed(second)
            count = second.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
            self.assertEqual(0, count)
        finally:
            second.close()


if __name__ == "__main__":
    unittest.main()
