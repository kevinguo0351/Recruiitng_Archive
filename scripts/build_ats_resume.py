"""Build a simple one-column ATS resume PDF from a verified JSON profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def load_profile(path: Path) -> dict:
    profile = json.loads(path.read_text(encoding="utf-8"))
    for field in ("name", "contact", "profile", "education", "experience", "skills"):
        if field not in profile:
            raise ValueError(f"missing required field: {field}")
    return profile


def build(profile: dict, output: Path) -> None:
    normal = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9.6, leading=10.8)
    name = ParagraphStyle("name", fontName="Times-Bold", fontSize=18, leading=20, alignment=TA_CENTER)
    contact = ParagraphStyle("contact", parent=normal, alignment=TA_CENTER)
    section_style = ParagraphStyle("section", fontName="Times-Bold", fontSize=12, leading=13, spaceBefore=3)
    role = ParagraphStyle("role", fontName="Times-Bold", fontSize=10.8, leading=11.5)
    right = ParagraphStyle("right", parent=role, alignment=TA_RIGHT)
    bullet_style = ParagraphStyle("bullet", parent=normal, leftIndent=10, firstLineIndent=-7, bulletIndent=1.5)

    def section(title: str) -> list:
        return [Paragraph(title, section_style), HRFlowable(width="100%", thickness=0.55, color=colors.black, spaceAfter=2)]

    def heading(left: str, right_text: str, subtitle: str = "", dates: str = "") -> Table:
        table = Table(
            [[Paragraph(left, role), Paragraph(right_text, right)], [Paragraph(subtitle, normal), Paragraph(dates, right)]],
            colWidths=[6.0 * inch, 1.35 * inch],
        )
        table.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        return table

    def bullets(items: list[str]) -> list[Paragraph]:
        return [Paragraph("• " + item, bullet_style) for item in items]

    story = [Paragraph(profile["name"], name), Paragraph(profile["contact"], contact), Spacer(1, 3)]
    story += section("PROFILE") + [Paragraph(profile["profile"], normal)]
    story += section("EDUCATION")
    for item in profile["education"]:
        story.append(KeepTogether([heading(item["school"], item.get("location", ""), item["degree"], item.get("date", "")), *bullets(item.get("bullets", []))]))
    story += section("EXPERIENCE")
    for item in profile["experience"]:
        title = f'{item["organization"]} | {item["role"]}'
        story.append(KeepTogether([heading(title, item.get("location", ""), "", item.get("dates", "")), *bullets(item.get("bullets", []))]))
    story += section("SKILLS") + [Paragraph("; ".join(profile["skills"]), normal)]

    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(output), pagesize=letter, leftMargin=0.4 * inch, rightMargin=0.4 * inch, topMargin=0.3 * inch, bottomMargin=0.3 * inch, title="ATS Resume")
    document.build(story)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path, help="Verified profile JSON; keep real profiles outside source control")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(load_profile(args.profile), args.output)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
