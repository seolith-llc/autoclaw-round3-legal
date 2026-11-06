# -*- coding: utf-8 -*-
"""生成合同审查三件套：供应商原稿、修订对照稿（Word 修订模式）、修订后清洁版。

标记语法：{-被删除的原文-}  {+新增文字+}
"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3\deliverables")
AUTHOR = "AutoClaw 法律审查"
DATE = "2026-11-06T12:00:00Z"

TOKEN = re.compile(r"\{(\+|-)(.*?)\1\}", re.S)

from contract_clauses import CLAUSES, PARTIES, PREAMBLE, TITLE, SUBTITLE


def set_run_font(run, size=12, bold=False, color=None):
    run.font.size = Pt(size)
    run.bold = bold
    run.font.name = "Times New Roman"
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "宋体")
    if color is not None:
        run.font.color.rgb = color


def add_plain_run(paragraph, text, size=12, bold=False):
    run = paragraph.add_run(text)
    set_run_font(run, size=size, bold=bold)
    return run


def add_del_run(paragraph, text):
    del_el = OxmlElement("w:del")
    del_el.set(qn("w:id"), str(next_id()))
    del_el.set(qn("w:author"), AUTHOR)
    del_el.set(qn("w:date"), DATE)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "宋体")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "24")
    rPr.append(rFonts)
    rPr.append(sz)
    r.append(rPr)
    del_text = OxmlElement("w:delText")
    del_text.set(qn("xml:space"), "preserve")
    del_text.text = text
    r.append(del_text)
    del_el.append(r)
    paragraph._p.append(del_el)


def add_ins_run(paragraph, text):
    ins_el = OxmlElement("w:ins")
    ins_el.set(qn("w:id"), str(next_id()))
    ins_el.set(qn("w:author"), AUTHOR)
    ins_el.set(qn("w:date"), DATE)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "宋体")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "24")
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "C00000")
    rPr.append(rFonts)
    rPr.append(sz)
    rPr.append(u)
    rPr.append(color)
    r.append(rPr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    ins_el.append(r)
    paragraph._p.append(ins_el)


_ID = 1000


def next_id():
    global _ID
    _ID += 1
    return _ID


def new_doc():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(3.0)
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), "宋体")
    return doc


def add_heading_cn(doc, text, size=16):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_plain_run(p, text, size=size, bold=True)
    return p


def add_body(doc, text, size=12, bold=False, first_line=True):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    if first_line:
        p.paragraph_format.first_line_indent = Cm(0.74)
    add_plain_run(p, text, size=size, bold=bold)
    return p


def vendor_text(para):
    out = []
    pos = 0
    for m in TOKEN.finditer(para):
        if m.start() > pos:
            out.append(para[pos : m.start()])
        if m.group(1) == "-":
            out.append(m.group(2))
        pos = m.end()
    if pos < len(para):
        out.append(para[pos:])
    return "".join(out)


def revised_text(para):
    out = []
    pos = 0
    for m in TOKEN.finditer(para):
        if m.start() > pos:
            out.append(para[pos : m.start()])
        if m.group(1) == "+":
            out.append(m.group(2))
        pos = m.end()
    if pos < len(para):
        out.append(para[pos:])
    return "".join(out)


def iter_segments(text):
    """yield (kind, text) kind in plain/del/ins"""
    pos = 0
    for m in TOKEN.finditer(text):
        if m.start() > pos:
            yield ("plain", text[pos : m.start()])
        kind = "ins" if m.group(1) == "+" else "del"
        yield (kind, m.group(2))
        pos = m.end()
    if pos < len(text):
        yield ("plain", text[pos:])


def build_common_front(doc, subtitle):
    add_heading_cn(doc, TITLE, size=16)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_plain_run(p, subtitle, size=12, bold=True)
    doc.add_paragraph()
    for line in PARTIES:
        add_body(doc, line, size=11, first_line=False)
    doc.add_paragraph()
    add_body(doc, PREAMBLE)
    doc.add_paragraph()


def build_vendor():
    doc = new_doc()
    build_common_front(doc, "（供应商提供稿 · 未修改）")
    for clause in CLAUSES:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        add_plain_run(p, f"{clause['no']}　{clause['title']}", size=12, bold=True)
        for para in clause["paras"]:
            add_body(doc, vendor_text(para))
    doc.add_paragraph()
    add_body(doc, "甲方（盖章）：　　　　　　　　　　乙方（盖章）：", first_line=False)
    add_body(doc, "授权代表：　　　　　　　　　　　　授权代表：", first_line=False)
    add_body(doc, "日期：　　　　　　　　　　　　　　日期：", first_line=False)
    path = OUT / "01-供应商原稿-未修改.docx"
    doc.save(path)
    return path


def build_redline():
    doc = new_doc()
    build_common_front(doc, "（修订对照稿 · Word 修订模式）")
    # 修订说明
    p = doc.add_paragraph()
    add_plain_run(p, "修订说明", size=12, bold=True)
    notes = [
        "1. 本稿在 Word 修订模式下作出：删除线为建议删除内容，下划线红字为建议新增内容，修订作者为“AutoClaw 法律审查”。每条修订均成对出现——删除原条款、写入新条款，不留自相矛盾的残留句。",
        "2. 修订依据《中华人民共和国民法典》第四百九十六条至第四百九十八条（格式条款）、第五百零六条（免责条款）、第五百七十七条、第五百八十四条、第五百八十五条（违约责任与违约金调整）、《中华人民共和国个人信息保护法》第二十一条（委托处理）、《中华人民共和国数据安全法》第二十七条、第二十九条（数据安全保护义务），以及《最高人民法院关于适用〈中华人民共和国民法典〉合同编通则若干问题的解释》第十条、第六十四条、第六十五条。",
        "3. 高风险条款集中在：数据无限许可与模型训练（5.2）、责任限额与禁止调整违约金（9.1/9.2）、甲方不得解除合同（2.3/10.2）、单方调价与功能下线（3.2/7.1）、无委托处理协议（6.1）、甲方所在地仲裁改判（11.1）。",
        "4. 本稿为演示用虚构交易，不含真实客户信息；正式使用前应由经办律师结合交易背景复核。",
    ]
    for n in notes:
        add_body(doc, n, size=10.5, first_line=False)
    doc.add_paragraph()

    for clause in CLAUSES:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        add_plain_run(p, f"{clause['no']}　{clause['title']}", size=12, bold=True)
        for para in clause["paras"]:
            bp = doc.add_paragraph()
            bp.paragraph_format.line_spacing = 1.5
            bp.paragraph_format.first_line_indent = Cm(0.74)
            for kind, seg in iter_segments(para):
                if not seg:
                    continue
                if kind == "plain":
                    add_plain_run(bp, seg)
                elif kind == "del":
                    add_del_run(bp, seg)
                else:
                    add_ins_run(bp, seg)
    doc.add_paragraph()
    add_body(doc, "甲方（盖章）：　　　　　　　　　　乙方（盖章）：", first_line=False)
    add_body(doc, "授权代表：　　　　　　　　　　　　授权代表：", first_line=False)
    add_body(doc, "日期：　　　　　　　　　　　　　　日期：", first_line=False)
    path = OUT / "02-修订对照稿-修订模式.docx"
    doc.save(path)
    return path


def build_revised():
    doc = new_doc()
    build_common_front(doc, "（修订后清洁版）")
    for clause in CLAUSES:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        add_plain_run(p, f"{clause['no']}　{clause['title']}", size=12, bold=True)
        for para in clause["paras"]:
            add_body(doc, revised_text(para))
    doc.add_paragraph()
    add_body(doc, "甲方（盖章）：　　　　　　　　　　乙方（盖章）：", first_line=False)
    add_body(doc, "授权代表：　　　　　　　　　　　　授权代表：", first_line=False)
    add_body(doc, "日期：　　　　　　　　　　　　　　日期：", first_line=False)
    path = OUT / "03-修订后清洁版.docx"
    doc.save(path)
    return path


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (build_vendor, build_redline, build_revised):
        path = fn()
        print("written:", path)


if __name__ == "__main__":
    main()
