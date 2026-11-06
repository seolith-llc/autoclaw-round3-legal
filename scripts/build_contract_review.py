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

OUT = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3\deliverables")
AUTHOR = "AutoClaw 法律审查"
DATE = "2026-11-06T12:00:00Z"

TOKEN = re.compile(r"\{(\+|-)(.*?)\1\}", re.S)

TITLE = "工业设备远程运维数据平台服务合同"
SUBTITLE = "（修订对照稿 · 修订模式）"
PARTIES = [
    "甲方：宁波汇丰精密制造有限公司（演示用虚构主体）",
    "乙方：上海云衍数字科技有限公司（演示用虚构主体）",
    "签订时间：2026年11月",
    "本合同所有主体、金额、条款均为演示用虚构内容，不含任何真实客户或交易信息。",
]
PREAMBLE = (
    "根据《中华人民共和国民法典》及有关法律法规，甲乙双方本着平等自愿、诚实信用的原则，"
    "就甲方采购乙方工业设备远程运维数据平台服务事宜，达成如下协议。"
)

CLAUSES = [
    {
        "no": "第一条",
        "title": "服务内容",
        "paras": [
            "1.1 乙方向甲方提供“云衍设备云”工业设备远程运维数据平台（以下简称“平台”）的访问权限及配套技术支持服务，具体功能模块以乙方官网当时公布的功能清单为准。{+乙方应在附件一《服务说明书》中明确约定交付的功能模块、设备接入数量上限（500台）、数据保留期限及工单响应时效，并按附件一履行；附件一与本合同具有同等效力。+}",
            "1.2 平台按“现状”提供，乙方不对平台的适用性、完整性、准确性作出任何承诺。{+在附件一约定范围内，乙方保证平台具备实现本合同目的的通常效用；出现功能缺陷的，乙方应按第四条、第九条承担修复、赔偿等违约责任。+}",
        ],
    },
    {
        "no": "第二条",
        "title": "服务期限与续约",
        "paras": [
            "2.1 服务期限自2026年12月1日起至2029年11月30日止，共36个月。",
            "2.2 期满前30日内甲方未书面提出异议的，本合同自动续期12个月，续期费用按乙方届时公布的价目计算。{+任何一方不愿续约的，应于期满前30日书面通知对方；合同期满未续约的，乙方应于10个工作日内退还甲方已预付但未消费的服务费。+}",
            "2.3 本合同履行期内，甲方不得解除本合同；甲方提前终止的，已付费用不予退还，并应支付剩余期间全部服务费的30%作为违约金。{+甲方有权提前30日书面通知解除本合同；解除后，乙方应按剩余服务期间占总服务期间的比例退还相应服务费。+}",
        ],
    },
    {
        "no": "第三条",
        "title": "费用与支付",
        "paras": [
            "3.1 年服务费为人民币480,000元（含税），甲方应于本合同签订后5个工作日内一次性预付全款。{+首年服务费于签订后5个工作日内支付50%，平台验收合格后10个工作日内支付余款；第二、三年服务费于各服务年度开始前15日内支付。+}",
            "3.2 乙方有权根据经营情况调整服务价格，调整后的价格自乙方官网公布之日起7日后生效，并对甲方自动适用。{+服务期内价格不予调整；续约年度价格涨幅不得超过上一服务年度的5%。+}",
            "3.3 甲方逾期付款的，每逾期一日按应付未付金额的{-0.5%-}{+0.05%+}支付违约金。",
        ],
    },
    {
        "no": "第四条",
        "title": "服务水平与故障处理",
        "paras": [
            "4.1 平台月度可用率不低于99.0%。",
            "4.2 未达到前款可用率的，乙方仅相应延长服务期限，不承担赔偿责任。{+月度可用率低于99.0%的，乙方按当月服务费的10%向甲方支付违约金；月度可用率低于95%且连续超过5日的，甲方有权解除本合同并要求乙方赔偿损失。+}",
            "4.3 因电力供应、公共网络、不可抗力或甲方自身原因导致的中断，不计入可用率统计。{+乙方上游服务商故障导致的中断计入可用率统计，乙方应先行向甲方承担违约责任。+}",
        ],
    },
    {
        "no": "第五条",
        "title": "数据权属与使用许可",
        "paras": [
            "5.1 甲方上传至平台的数据，归甲方所有。{+甲方对其上传数据及设备运行数据享有所有权；乙方仅得为履行本合同之目的，在中华人民共和国境内处理相关数据。+}",
            "{-5.2 甲方授予乙方在全球范围内、免费、不可撤销、可转授权的许可，使用前述数据用于平台运营、服务改进、产品开发、算法模型训练及商业分析。-}{+5.2 未经甲方书面同意，乙方不得将甲方数据用于本合同履行之外的任何用途，包括但不限于算法模型训练、产品开发及商业分析；不得向任何第三方提供或出售甲方数据。+}",
            "5.3 乙方对基于甲方数据形成的衍生数据、统计成果、模型及算法享有全部权利。{+乙方对其独立开发的通用模型、算法享有权利，但不得包含甲方数据及可识别甲方商业秘密的内容；基于甲方数据形成的统计成果归甲方所有。+}",
        ],
    },
    {
        "no": "第六条",
        "title": "个人信息与数据安全",
        "paras": [
            "6.1 乙方应按照法律法规的规定处理个人信息。{+双方应另行签署《个人信息委托处理协议》作为本合同附件二，明确委托处理的目的、期限、处理方式、个人信息种类、保护措施以及双方的权利和义务，乙方并对受托处理活动进行监督。+}",
            "6.2 因数据泄露、丢失、损坏造成的一切损失，乙方不承担责任。{+因乙方原因导致数据泄露、丢失、损坏的，乙方应立即采取补救措施、告知甲方并按规定向有关主管部门报告，同时赔偿甲方因此遭受的损失。+}",
        ],
    },
    {
        "no": "第七条",
        "title": "功能变更",
        "paras": [
            "7.1 乙方有权根据产品迭代需要，随时调整、替换或下线平台功能模块，无需事先通知甲方。{+乙方调整、替换或下线核心功能模块的，应提前30日书面通知甲方并征得甲方书面同意；因此影响本合同目的实现的，甲方有权解除本合同并要求乙方退还相应服务费。+}",
        ],
    },
    {
        "no": "第八条",
        "title": "保密",
        "paras": [
            "8.1 甲方应对乙方的技术资料、报价体系等保密信息予以保密，保密期自本合同签订之日起3年。{+双方相互承担保密义务，保密期至相关信息进入公有领域为止；乙方接触甲方数据及商业秘密的人员应签署保密承诺书。+}",
        ],
    },
    {
        "no": "第九条",
        "title": "违约责任与赔偿限额",
        "paras": [
            "9.1 乙方违约的，其赔偿总额以甲方已付服务费的30%为限，且不包括间接损失、预期利益损失。{+乙方违约造成甲方损失的，应依法赔偿；赔偿范围包括直接损失和可预见的间接损失，赔偿总额以本合同服务费总额为限，但乙方故意或重大过失造成的损失不受该限额限制。+}",
            "{-9.2 双方确认前述责任限额系真实意思表示，甲方不得请求人民法院或仲裁机构予以调整。-}{+9.2 本合同违约金及赔偿责任的约定，不影响甲方依法请求人民法院或仲裁机构予以调整的权利。+}",
        ],
    },
    {
        "no": "第十条",
        "title": "合同解除",
        "paras": [
            "10.1 出现下列情形之一的，乙方有权解除本合同：（一）甲方逾期付款超过15日；（二）甲方违反保密义务。",
            "10.2 甲方不得以任何理由解除本合同。{+甲方有权依照法律规定及本合同约定解除本合同；符合《中华人民共和国民法典》第五百六十三条规定情形的，甲方可以解除合同并要求乙方承担违约责任。+}",
        ],
    },
    {
        "no": "第十一条",
        "title": "争议解决",
        "paras": [
            "11.1 因本合同引起的争议，双方应友好协商解决；协商不成的，提交乙方所在地仲裁委员会仲裁。{+提交甲方所在地有管辖权的人民法院诉讼解决。+}",
            "11.2 败诉方应承担对方为实现债权支出的全部律师费、仲裁费。{+违约方承担守约方为实现债权支出的合理律师费、仲裁费，以实际发生并能提供票据支持的金额为限。+}",
        ],
    },
    {
        "no": "第十二条",
        "title": "格式条款与提示说明",
        "paras": [
            "12.1 本合同系乙方提供的格式合同，甲方已充分理解并接受全部条款。{+对免除或者减轻乙方责任、加重甲方责任、限制或者排除甲方主要权利的条款，乙方已以加粗、下划线方式提请甲方注意，并已按甲方要求作出说明。+}",
            "12.2 不可抗力包括地震、台风、洪水、战争、政府行为、政策调整、市场变化以及乙方上游服务商故障。{+不可抗力指不能预见、不能避免且不能克服的客观情况，不包括乙方上游服务商故障、政策调整及市场变化。+}",
        ],
    },
    {
        "no": "第十三条",
        "title": "其他",
        "paras": [
            "13.1 本合同未尽事宜，双方可另行签订补充协议；补充协议与本合同不一致的，以补充协议为准。",
            "13.2 本合同一式两份，双方各执一份，自双方盖章之日起生效。{+附件一《服务说明书》、附件二《个人信息委托处理协议》为本合同组成部分。+}",
        ],
    },
]


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
        "1. 本稿在 Word 修订模式下作出：删除线为建议删除内容，下划线红字为建议新增内容，修订作者为“AutoClaw 法律审查”。",
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
