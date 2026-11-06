# -*- coding: utf-8 -*-
"""极简 Markdown -> DOCX 转换器（标题/段落/列表/表格/粗体/链接）。"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


def set_run_font(run, size=12, bold=False, color=None):
    run.font.size = Pt(size)
    run.bold = bold
    run.font.name = "Times New Roman"
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "宋体")
    if color is not None:
        run.font.color.rgb = color


def add_hyperlink(paragraph, text, url, size=12):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "宋体")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(rFonts)
    rPr.append(sz)
    rPr.append(color)
    rPr.append(u)
    r.append(rPr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    hyperlink.append(r)
    paragraph._p.append(hyperlink)


INLINE = re.compile(r"(\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))")


def add_inline(paragraph, text, size=12, bold_all=False):
    for chunk in INLINE.split(text):
        if not chunk:
            continue
        if chunk.startswith("**") and chunk.endswith("**"):
            run = paragraph.add_run(chunk[2:-2])
            set_run_font(run, size=size, bold=True)
        elif chunk.startswith("[") and "](" in chunk:
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", chunk)
            if m:
                add_hyperlink(paragraph, m.group(1), m.group(2), size=size)
            else:
                run = paragraph.add_run(chunk)
                set_run_font(run, size=size, bold=bold_all)
        else:
            run = paragraph.add_run(chunk)
            set_run_font(run, size=size, bold=bold_all)


def convert(md_path: Path, docx_path: Path, title: str | None = None):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.8)
        section.right_margin = Cm(2.8)
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), "宋体")

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()
        if not line.strip() or line.strip() == "---":
            i += 1
            continue
        if line.startswith("# "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_inline(p, line[2:], size=18, bold_all=True)
        elif line.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            add_inline(p, line[3:], size=14, bold_all=True)
        elif line.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            add_inline(p, line[4:], size=12.5, bold_all=True)
        elif line.startswith("|"):
            # collect table
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.match(r"^:?-+:?$", c) for c in cells):
                    tbl.append(cells)
                i += 1
            if tbl:
                table = doc.add_table(rows=len(tbl), cols=len(tbl[0]))
                table.style = "Table Grid"
                for r, row in enumerate(tbl):
                    for c, val in enumerate(row):
                        cell = table.cell(r, c)
                        cell.text = ""
                        p = cell.paragraphs[0]
                        add_inline(p, val, size=10, bold_all=(r == 0))
            continue
        elif re.match(r"^\d+\.\s", line):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.74)
            add_inline(p, line)
        elif line.startswith("- "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.74)
            add_inline(p, "• " + line[2:])
        else:
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.4
            p.paragraph_format.first_line_indent = Cm(0.74)
            add_inline(p, line)
        i += 1

    doc.save(docx_path)
    print("written:", docx_path)


if __name__ == "__main__":
    base = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3\deliverables")
    convert(base / "04-审查备忘录.md", base / "04-审查备忘录.docx")
    convert(base / "06-引用核验日志.md", base / "06-引用核验日志.docx")
    convert(base / "07-可复用审查清单.md", base / "07-可复用审查清单.docx")
