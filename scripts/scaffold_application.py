"""Create an auditable folder for one company and role."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


TEMPLATE_NAMES = ("01-JD.md", "02-Company-Reviews.md", "03-ATS-Keywords.md", "04-Tailoring-Notes.md")


def safe_component(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", value).strip().rstrip(".")
    value = re.sub(r"\s+", " ", value)
    if not value or value in {".", ".."}:
        raise ValueError("company and role must contain filename-safe text")
    return value[:100]


def scaffold(root: Path, company: str, role: str, templates: Path) -> Path:
    folder = root / f"{safe_component(company)} - {safe_component(role)}"
    folder.mkdir(parents=True, exist_ok=True)
    for name in TEMPLATE_NAMES:
        source = templates / name
        if not source.is_file():
            raise FileNotFoundError(f"missing template: {source}")
        destination = folder / name
        if not destination.exists():
            shutil.copyfile(source, destination)
    return folder.resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Local application archive (keep personal packages out of Git)")
    parser.add_argument("company")
    parser.add_argument("role")
    parser.add_argument(
        "--templates",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "templates",
    )
    args = parser.parse_args()
    print(scaffold(args.root, args.company, args.role, args.templates))


if __name__ == "__main__":
    main()
