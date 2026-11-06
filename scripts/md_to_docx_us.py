# -*- coding: utf-8 -*-
"""Minimal Markdown -> DOCX converter for the English deliverables."""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

FONT = "Times New Roman"


def style_run(run, size=11.5, bold=False):
    run.font.size = Pt(size)
    run.bold = bold
    run.font.name = FONT
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)


def add_link(paragraph, text, url, size=11.5):
    r_id = paragraph.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    for el in (rFonts, sz, color, u):
        rPr.append(el)
    r.append(rPr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    link.append(r)
    paragraph._p.append(link)


INLINE = re.compile(r"(\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))")


def add_inline(paragraph, text, size=11.5, bold=False):
    for chunk in INLINE.split(text):
        if not chunk:
            continue
        if chunk.startswith("**") and chunk.endswith("**"):
            run = paragraph.add_run(chunk[2:-2])
            style_run(run, size, True)
        elif chunk.startswith("[") and "](" in chunk:
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", chunk)
            if m:
                add_link(paragraph, m.group(1), m.group(2), size)
            else:
                run = paragraph.add_run(chunk)
                style_run(run, size, bold)
        else:
            run = paragraph.add_run(chunk)
            style_run(run, size, bold)


def convert(md_path: Path, docx_path: Path):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.4)
        section.bottom_margin = Cm(2.4)
        section.left_margin = Cm(2.6)
        section.right_margin = Cm(2.6)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(11.5)
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)

    i, n = 0, len(lines)
    while i < n:
        line = lines[i].rstrip()
        if not line.strip() or line.strip() == "---":
            i += 1
            continue
        if line.startswith("# "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_inline(p, line[2:], size=17, bold=True)
        elif line.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            add_inline(p, line[3:], size=13, bold=True)
        elif line.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            add_inline(p, line[4:], size=12, bold=True)
        elif line.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.match(r"^:?-{2,}:?$", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows and rows[0]:
                width = max(len(r) for r in rows)
                table = doc.add_table(rows=len(rows), cols=width)
                table.style = "Table Grid"
                for ri, row in enumerate(rows):
                    for ci in range(width):
                        cell = table.cell(ri, ci)
                        cell.text = ""
                        add_inline(cell.paragraphs[0], row[ci] if ci < len(row) else "", size=9.5, bold=(ri == 0))
            continue
        elif re.match(r"^\d+\.\s", line):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.space_after = Pt(4)
            add_inline(p, line)
        elif line.startswith("- "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.space_after = Pt(4)
            add_inline(p, "\u2022 " + line[2:])
        else:
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(6)
            add_inline(p, line)
        i += 1
    doc.save(docx_path)
    print("written:", docx_path)


if __name__ == "__main__":
    base = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3\deliverables")
    convert(base / "04-review-memo.md", base / "04-review-memo.docx")
    convert(base / "06-citation-verification-log.md", base / "06-citation-verification-log.docx")
    convert(base / "07-reusable-checklist.md", base / "07-reusable-checklist.docx")
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from strip_cjk_fonts import clean_docx
    for docx_path in base.glob("*.docx"):
        clean_docx(docx_path)
