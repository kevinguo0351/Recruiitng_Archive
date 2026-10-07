"""Render a privacy-safe application tracker from JSON to Markdown and XLSX."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo


FIELDS = (
    "company", "role", "url", "status", "fit_and_next_step",
    "sponsorship_evidence", "confidence", "updated_date",
)
HEADERS = (
    "Company", "Role", "Application URL", "Status", "Fit / limitation / next step",
    "Sponsorship evidence", "Confidence", "Updated date",
)


def load_rows(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("input must be a JSON array")
    rows: list[dict[str, str]] = []
    for index, item in enumerate(data, 1):
        if not isinstance(item, dict):
            raise ValueError(f"row {index} must be an object")
        row = {field: str(item.get(field, "")).strip() for field in FIELDS}
        if not row["company"] or not row["role"] or not row["status"]:
            raise ValueError(f"row {index} requires company, role, and status")
        if row["url"] and urlparse(row["url"]).scheme not in {"http", "https"}:
            raise ValueError(f"row {index} has a non-HTTP URL")
        rows.append(row)
    return rows


def write_markdown(rows: list[dict[str, str]], path: Path) -> None:
    lines = ["# Application tracker", "", "| " + " | ".join(HEADERS) + " |", "|" + "|".join(["---"] * len(HEADERS)) + "|"]
    for row in rows:
        values = [row[field].replace("|", "\\|").replace("\n", " ") for field in FIELDS]
        lines.append("| " + " | ".join(values) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_xlsx(rows: list[dict[str, str]], path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Applications"
    sheet.sheet_view.showGridLines = False
    sheet.append(HEADERS)
    for row in rows:
        sheet.append([row[field] for field in FIELDS])
    for cell in sheet[1]:
        cell.fill = PatternFill("solid", fgColor="16324F")
        cell.font = Font(name="Aptos", bold=True, color="FFFFFF")
    widths = (22, 38, 50, 18, 65, 45, 24, 16)
    for index, width in enumerate(widths, 1):
        sheet.column_dimensions[chr(64 + index)].width = width
    for row in sheet.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    sheet.freeze_panes = "A2"
    if rows:
        table = Table(displayName="ApplicationsTracker", ref=f"A1:H{len(rows) + 1}")
        table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        sheet.add_table(table)

    summary = workbook.create_sheet("Summary")
    summary.sheet_view.showGridLines = False
    summary.append(("Status", "Count"))
    for status, count in sorted(Counter(row["status"] for row in rows).items()):
        summary.append((status, count))
    summary.append(("Total", len(rows)))
    for cell in summary[1]:
        cell.fill = PatternFill("solid", fgColor="16324F")
        cell.font = Font(name="Aptos", bold=True, color="FFFFFF")
    summary.column_dimensions["A"].width = 30
    summary.column_dimensions["B"].width = 12
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--xlsx", type=Path, default=Path("application-tracker.xlsx"))
    parser.add_argument("--markdown", type=Path, default=Path("application-tracker.md"))
    args = parser.parse_args()
    rows = load_rows(args.input)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(rows, args.markdown)
    write_xlsx(rows, args.xlsx)
    print(f"wrote {len(rows)} records")


if __name__ == "__main__":
    main()
