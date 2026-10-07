#!/usr/bin/env python3
"""Local recruiting tracker API and static site; standard library only."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "db" / "migrations"
SEED = ROOT / "db" / "seed_synthetic.sql"
STATIC = Path(__file__).resolve().parent / "static"
DEFAULT_DB = ROOT / "var" / "recruiting.db"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def migrate(connection: sqlite3.Connection) -> list[str]:
    connection.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations "
        "(filename TEXT PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    )
    applied = {row[0] for row in connection.execute("SELECT filename FROM schema_migrations")}
    added: list[str] = []
    for migration in sorted(MIGRATIONS.glob("*.sql")):
        if migration.name in applied:
            continue
        connection.executescript(migration.read_text(encoding="utf-8"))
        connection.execute("INSERT INTO schema_migrations(filename) VALUES (?)", (migration.name,))
        connection.commit()
        added.append(migration.name)
    return added


def seed(connection: sqlite3.Connection) -> None:
    domain_tables = (
        "companies", "jobs", "candidates", "applications",
        "application_events", "research_sources",
    )
    existing = {
        table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in domain_tables
    }
    if any(existing.values()):
        raise RuntimeError("Seed requires an empty database; refusing to overwrite existing data.")
    try:
        connection.executescript("BEGIN;\n" + SEED.read_text(encoding="utf-8") + "\nCOMMIT;")
    except Exception:
        connection.rollback()
        raise


def list_applications(connection: sqlite3.Connection, status: str | None = None) -> list[dict]:
    sql = "SELECT * FROM application_summary"
    values: tuple[str, ...] = ()
    if status:
        sql += " WHERE status = ?"
        values = (status,)
    sql += " ORDER BY updated_at DESC, application_id DESC"
    return [dict(row) for row in connection.execute(sql, values)]


def summary(connection: sqlite3.Connection) -> dict:
    counts = {
        row["status"]: row["count"]
        for row in connection.execute(
            "SELECT status, COUNT(*) AS count FROM applications GROUP BY status"
        )
    }
    return {"total": sum(counts.values()), "by_status": counts}


def make_handler(db_path: Path):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(STATIC), **kwargs)

        def _json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802 - HTTP handler API
            parsed = urlparse(self.path)
            if parsed.path == "/api/health":
                self._json({"status": "ok"})
                return
            if parsed.path in {"/api/applications", "/api/summary"}:
                try:
                    with connect(db_path) as connection:
                        if parsed.path == "/api/applications":
                            status = parse_qs(parsed.query).get("status", [None])[0]
                            self._json(list_applications(connection, status))
                        else:
                            self._json(summary(connection))
                except sqlite3.Error as error:
                    self._json({"error": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR)
                return
            super().do_GET()

    return Handler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", action="store_true", help="Load synthetic sample records")
    parser.add_argument("--no-serve", action="store_true", help="Exit after initialization")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db_path = Path(os.getenv("RECRUITING_DB_PATH", DEFAULT_DB)).resolve()
    with connect(db_path) as connection:
        applied = migrate(connection)
        if applied:
            print(f"Applied migrations: {', '.join(applied)}")
        if args.seed:
            seed(connection)
            print("Loaded synthetic demonstration records.")
    if args.no_serve:
        return
    host = os.getenv("RECRUITING_HOST", "127.0.0.1")
    port = int(os.getenv("RECRUITING_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), make_handler(db_path))
    print(f"Recruiting tracker running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
