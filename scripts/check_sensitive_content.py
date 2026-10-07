"""Fail when tracked/staged repository content resembles private recruiting data."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {".pdf", ".docx", ".xlsx", ".xls", ".db", ".sqlite", ".sqlite3", ".pem", ".key"}
PATTERNS = {
    "non-example email": re.compile(r"\b[A-Z0-9._%+-]+@(?!example\.(?:test|invalid)\b)[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "US social security number": re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"),
    "Windows user profile path": re.compile(r"[A-Z]:\\Users\\[^\\\s]+\\", re.I),
    "credential assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}"),
}


def repository_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    )
    return [ROOT / item.decode("utf-8") for item in output.split(b"\0") if item]


def scan(paths: list[Path], forbidden_terms: list[str]) -> list[str]:
    findings: list[str] = []
    terms = [term.casefold() for term in forbidden_terms if term.strip()]
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"{relative}: forbidden private/binary suffix")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{relative}: {label}")
        lowered = text.casefold()
        for term in terms:
            if term in lowered:
                findings.append(f"{relative}: caller-supplied forbidden term")
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--forbid", action="append", default=[], help="Additional literal term to reject")
    args = parser.parse_args()
    findings = scan(repository_files(), args.forbid)
    if findings:
        print("Sensitive-content check failed:")
        print("\n".join(f"- {item}" for item in findings))
        return 1
    print("Sensitive-content check passed for tracked and unignored files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
