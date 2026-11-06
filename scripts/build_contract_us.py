# -*- coding: utf-8 -*-
"""Build the US-law SaaS review: vendor draft, tracked-changes redline, clean revised.

Markup: {-deleted text-}  {+inserted text+}
Rule: any change that contradicts an existing clause must be a paired del+ins.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

OUT = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3\deliverables")
AUTHOR = "AutoClaw Legal Review"
DATE = "2026-11-06T12:00:00Z"
FONT = "Times New Roman"

TOKEN = re.compile(r"\{(\+|-)(.*?)\1\}", re.S)

TITLE = "MASTER SUBSCRIPTION AGREEMENT"
SUBTITLE = "(Redline - tracked changes)"
FRONT = [
    "Customer: Northwind Precision Manufacturing, Inc., an Ohio corporation",
    "Provider: Skyline Device Cloud, Inc., a Delaware corporation",
    "Effective Date: December 1, 2026",
    "This is a fictional training sample. No real customer, contract, or personal data is used.",
]
PREAMBLE = (
    "This Master Subscription Agreement (the \"Agreement\") is entered into by and between "
    "Northwind Precision Manufacturing, Inc. (\"Customer\") and Skyline Device Cloud, Inc. (\"Provider\") "
    "as of the Effective Date."
)

CLAUSES = [
    {
        "no": "1.",
        "title": "Services and Scope",
        "paras": [
            "1.1 Provider grants Customer a non-exclusive, non-transferable right to access and use the Skyline Device Cloud platform (the \"Platform\") during the Term for up to 250 named users. {-The features and functionality are those described on Provider's website as of the Effective Date and may change from time to time in Provider's sole discretion.-}{+Provider will provide the features and functionality described in Exhibit A (Service Description), including the 250-seat allocation, 24-month data retention, and the support response times stated in Exhibit A. Exhibit A is incorporated into this Agreement by reference.+}",
            "1.2 {-Provider may modify, suspend, or discontinue any feature or module at any time without notice to Customer.-}{+Provider may modify non-core features on 30 days' notice. Provider may modify, replace, or discontinue a core feature only with Customer's prior written consent, and if a change materially reduces the functionality described in Exhibit A, Customer may terminate the affected subscription and receive a pro rata refund of prepaid, unused fees.+}",
        ],
    },
    {
        "no": "2.",
        "title": "Term, Renewal, and Termination",
        "paras": [
            "2.1 The initial term is 36 months from the Effective Date (the \"Initial Term\"), renewable as provided in Section 2.2 (together, the \"Term\").",
            "2.2 {-This Agreement automatically renews for successive 12-month terms unless either party gives written notice of non-renewal at least 60 days before the end of the then-current term. Renewal pricing will be Provider's then-current list price.-}{+This Agreement renews for a successive 12-month term only if Customer accepts a written renewal quote at least 30 days before the end of the then-current term. Provider will deliver the renewal quote no later than 60 days before expiration, and renewal pricing may not increase by more than 5% over the prior term.+}",
            "2.3 {-Customer may not terminate this Agreement for convenience, and on any early termination all fees for the remainder of the Term become immediately due.-}{+Customer may terminate this Agreement for convenience on 30 days' written notice and will receive a pro rata refund of prepaid, unused fees. Provider may terminate for convenience only on 90 days' written notice and will refund prepaid, unused fees.+}",
        ],
    },
    {
        "no": "3.",
        "title": "Fees, Payment, and Price Changes",
        "paras": [
            "3.1 The annual subscription fee is US$180,000. {-Fees are payable annually in advance within 15 days of invoice, are non-refundable, and are based on the subscription purchased rather than actual usage.-}{+Fees are payable 50% on the Effective Date and 50% on Customer's acceptance of the production environment, with subsequent years payable annually in advance. Prepaid fees are refundable to the extent unused on any termination permitted under this Agreement.+}",
            "3.2 {-Provider may increase fees at any time on 30 days' notice, including during the Initial Term.-}{+Provider may not increase fees during the Initial Term. Renewal pricing is capped by Section 2.2.+}",
            "3.3 Late amounts accrue interest at {-1.5%-}{+1.0%+} per month or the maximum rate permitted by law, whichever is lower.",
        ],
    },
    {
        "no": "4.",
        "title": "Service Levels and Support",
        "paras": [
            "4.1 Provider will make the Platform available at least 99.5% of the time in each calendar month, measured as described in Exhibit A.",
            "4.2 {-If Provider fails to meet the availability commitment, Customer's sole and exclusive remedy is a service credit of up to 5% of the monthly fee, and Provider will have no other liability for the failure.-}{+If monthly availability falls below 99.5%, Provider will issue a credit of 10% of the monthly fee for each full percentage point below the commitment. If availability falls below 95% in any two months of a rolling six-month period, Customer may terminate the affected subscription for cause and receive a pro rata refund. Credits are not Customer's exclusive remedy for a material breach of this Section 4.+}",
            "4.3 Scheduled maintenance with at least 24 hours' notice, force majeure events, and Customer-caused unavailability are excluded from the availability calculation. {-Failures of Provider's hosting provider or other third-party suppliers are also excluded.-}{+Failures of Provider's hosting provider, subcontractors, and other third-party suppliers are not excluded and count as Provider's unavailability.+}",
        ],
    },
    {
        "no": "5.",
        "title": "Customer Data and License to Provider",
        "paras": [
            "5.1 Customer owns all data and content that Customer or its users submit to the Platform (\"Customer Data\").",
            "5.2 {-Customer grants Provider a perpetual, irrevocable, worldwide, royalty-free license to use, reproduce, modify, and create derivative works from Customer Data, including to train, fine-tune, and improve machine-learning models and for any other business purpose.-}{+Customer grants Provider a limited, non-exclusive, non-transferable license to host, copy, transmit, and display Customer Data solely to provide the Platform and support under this Agreement. Provider will not use Customer Data to train, fine-tune, or improve any model, and will not disclose Customer Data to any third party except to subcontractors bound by Section 8 and Exhibit B.+}",
            "5.3 {-Provider owns all aggregated, de-identified, and derived data, together with all models and outputs developed from it.-}{+Provider may create aggregated data only if it is de-identified so that it cannot be associated with Customer or any identified or identifiable individual, and Provider will not attempt re-identification. Customer owns all outputs generated from its Customer Data.+}",
        ],
    },
    {
        "no": "6.",
        "title": "Privacy, Security, and Breach Notification",
        "paras": [
            "6.1 {-Provider will use commercially reasonable measures to protect Customer Data and is not responsible for unauthorized access unless caused by its gross negligence.-}{+Provider will maintain a written information security program that includes the administrative, technical, and physical safeguards described in Exhibit B, will undergo an annual SOC 2 Type II examination, and will provide the report to Customer under Section 8.+}",
            "6.2 {-Provider will notify Customer of a security incident within a commercially reasonable time after discovery.-}{+Provider will notify Customer without undue delay and in any event within 72 hours after confirming a security incident, will provide the information Customer reasonably needs to meet its notification obligations under applicable state breach-notification laws, and will bear the reasonable costs of notice, credit monitoring, and forensic investigation that Customer incurs as a result of the incident.+}",
            "6.3 {+The parties will execute Exhibit B (Data Processing Addendum) before any personal information is processed. Exhibit B will satisfy Cal. Civ. Code section 1798.100(d), identify the limited and specified business purposes, prohibit Provider from selling or sharing personal information, and require Provider to notify Customer if it can no longer meet its obligations.+}",
        ],
    },
    {
        "no": "7.",
        "title": "Intellectual Property and Feedback",
        "paras": [
            "7.1 {-All feedback, suggestions, and usage data are Provider's sole property, and Customer assigns to Provider all right, title, and interest in any feedback Customer provides.-}{+Customer retains all right, title, and interest in feedback it provides. Customer grants Provider a non-exclusive, royalty-free license to use feedback to improve the Platform, without attribution and without any obligation to implement it. This license does not extend to Customer Confidential Information.+}",
        ],
    },
    {
        "no": "8.",
        "title": "Confidentiality",
        "paras": [
            "8.1 {-Customer will keep Provider's terms, pricing, and technology confidential in perpetuity.-}{+Each party will keep the other party's Confidential Information confidential during the Term and for three years after termination, except that trade secrets remain protected for so long as they qualify as trade secrets under applicable law.+}",
        ],
    },
    {
        "no": "9.",
        "title": "Limitation of Liability",
        "paras": [
            "9.1 {-Provider's total aggregate liability will not exceed the fees paid in the 12 months preceding the event giving rise to the claim, and Provider will not be liable for lost profits, lost revenue, or indirect, incidental, special, or consequential damages.-}{+Provider's total aggregate liability will not exceed the greater of the fees paid or payable in the 12 months preceding the event giving rise to the claim and two times the annual fee. The exclusion of consequential damages does not apply to Provider's gross negligence, willful misconduct, breach of Section 6, or indemnification obligations under Section 10.+}",
            "9.2 {-These limitations apply regardless of the theory of liability and may not be modified by any court or arbitrator.-}{+These limitations do not apply to fraud, willful misconduct, or any liability that cannot be limited under applicable law.+}",
        ],
    },
    {
        "no": "10.",
        "title": "Indemnification",
        "paras": [
            "10.1 {-Customer will defend and indemnify Provider against any claim arising out of Customer Data or Customer's use of the Platform, including claims caused by Provider's own negligence.-}{+Customer will defend and indemnify Provider against third-party claims alleging that Customer Data, used as permitted under this Agreement, infringes a U.S. patent, copyright, or trade secret.+}",
            "10.2 {+Provider will defend and indemnify Customer against third-party claims alleging that the Platform infringes a U.S. patent, copyright, or trademark, and will either procure the right for Customer to continue using the Platform or modify it to be non-infringing. This Section 10.2 does not apply to claims arising from Customer Data or from modifications not made by Provider.+}",
        ],
    },
    {
        "no": "11.",
        "title": "Suspension and Acceptable Use",
        "paras": [
            "11.1 {-Provider may suspend Customer's access immediately, with or without notice, if Provider suspects any violation of this Agreement or any risk to the Platform.-}{+Provider may suspend access only for a material breach that poses an imminent security risk, after written notice and a 48-hour cure period, or immediately where required by law. Any suspension must be limited to the affected users or features, and Provider will restore access promptly once the issue is resolved.+}",
            "11.2 Customer will comply with Provider's Acceptable Use Policy (the \"AUP\") {-as updated by Provider from time to time in its sole discretion-}{+as in effect on the Effective Date. Provider may update the AUP on 30 days' notice, and no update may materially reduce Customer's rights under this Agreement+}.",
        ],
    },
    {
        "no": "12.",
        "title": "Warranties and Disclaimers",
        "paras": [
            "12.1 {-THE PLATFORM IS PROVIDED \"AS IS\" AND PROVIDER DISCLAIMS ALL IMPLIED WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.-}{+Provider warrants that the Platform will perform materially in accordance with Exhibit A and that the services will be performed in a professional and workmanlike manner. Provider disclaims implied warranties only to the extent permitted by applicable law, and that disclaimer does not apply to the express warranties in this Section 12.+}",
        ],
    },
    {
        "no": "13.",
        "title": "Governing Law and Dispute Resolution",
        "paras": [
            "13.1 {-This Agreement is governed by Texas law, and the parties submit to the exclusive jurisdiction of the state and federal courts located in Travis County, Texas.-}{+This Agreement is governed by the laws of the State of Ohio and the federal laws of the United States, without regard to conflict-of-laws rules, and the parties submit to the exclusive jurisdiction of the state and federal courts located in Cuyahoga County, Ohio.+}",
            "13.2 {-Any dispute will be resolved by binding arbitration administered by the American Arbitration Association in Austin, Texas. Customer waives any right to participate in a class or collective action, and the arbitrator may not award relief inconsistent with Section 9.-}{+Either party may bring an action in the courts identified in Section 13.1. Nothing in this Agreement waives either party's right to seek injunctive relief. Any waiver of class or collective action rights applies only to the extent the waiver is enforceable under applicable law.+}",
        ],
    },
    {
        "no": "14.",
        "title": "Assignment and Subcontracting",
        "paras": [
            "14.1 {-Provider may assign this Agreement to any affiliate or successor without Customer's consent, and Customer may not assign this Agreement without Provider's prior written consent.-}{+Neither party may assign this Agreement without the other party's prior written consent, except to a successor in connection with a merger or a sale of substantially all assets, provided the assignee assumes all obligations and is not a direct competitor of the non-assigning party. Provider remains responsible for its subcontractors' performance.+}",
        ],
    },
    {
        "no": "15.",
        "title": "General",
        "paras": [
            "15.1 {-Provider may amend this Agreement by posting an updated version on its website, and Customer's continued use of the Platform constitutes acceptance.-}{+No amendment to this Agreement is effective unless made in a writing signed by both parties. Provider may update Exhibit A only as permitted by Section 1.2 and may update the AUP only as permitted by Section 11.2.+}",
            "15.2 This Agreement, together with its Exhibits, is the entire agreement of the parties and supersedes all prior proposals and understandings.",
        ],
    },
]

_ID = 2000


def next_id() -> int:
    global _ID
    _ID += 1
    return _ID


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


def add_plain(paragraph, text, size=11.5, bold=False):
    run = paragraph.add_run(text)
    style_run(run, size=size, bold=bold)
    return run


def _revision(tag, paragraph, text, strike=False):
    el = OxmlElement(tag)
    el.set(qn("w:id"), str(next_id()))
    el.set(qn("w:author"), AUTHOR)
    el.set(qn("w:date"), DATE)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "23")
    rPr.append(rFonts)
    rPr.append(sz)
    if strike:
        rPr.append(OxmlElement("w:strike"))
        node = OxmlElement("w:delText")
    else:
        u = OxmlElement("w:u")
        u.set(qn("w:val"), "single")
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "C00000")
        rPr.append(u)
        rPr.append(color)
        node = OxmlElement("w:t")
    node.set(qn("xml:space"), "preserve")
    node.text = text
    r.append(rPr)
    r.append(node)
    el.append(r)
    paragraph._p.append(el)


def add_del(paragraph, text):
    _revision("w:del", paragraph, text, strike=True)


def add_ins(paragraph, text):
    _revision("w:ins", paragraph, text, strike=False)


def vendor_text(text):
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        out.append(text[pos:m.start()])
        if m.group(1) == "-":
            out.append(m.group(2))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


def revised_text(text):
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        out.append(text[pos:m.start()])
        if m.group(1) == "+":
            out.append(m.group(2))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


def new_doc():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.8)
        section.right_margin = Cm(2.8)
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
    return doc


def front(doc, subtitle):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_plain(p, TITLE, size=16, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_plain(p, subtitle, size=11, bold=True)
    doc.add_paragraph()
    for line in FRONT:
        q = doc.add_paragraph()
        add_plain(q, line, size=10.5)
    doc.add_paragraph()
    q = doc.add_paragraph()
    add_plain(q, PREAMBLE)


def body_para(doc, text, size=11.5):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    add_plain(p, text, size=size)
    return p


def build_vendor():
    doc = new_doc()
    front(doc, "(Provider draft - unmodified)")
    for c in CLAUSES:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        add_plain(p, f"{c['no']} {c['title']}", size=11.5, bold=True)
        for para in c["paras"]:
            body_para(doc, vendor_text(para))
    for line in ("NORTHWIND PRECISION MANUFACTURING, INC.", "By: ______________________", "Title: ____________________"):
        q = doc.add_paragraph()
        add_plain(q, line, size=11)
    path = OUT / "01-vendor-draft.docx"
    doc.save(path)
    return path


def build_redline():
    doc = new_doc()
    front(doc, SUBTITLE)
    p = doc.add_paragraph()
    add_plain(p, "Revision notes", size=11.5, bold=True)
    notes = [
        "1. Every change is a paired edit: struck text is deleted, red underlined text is inserted. Author: AutoClaw Legal Review.",
        "2. Each edit replaces the original sentence rather than appending to it, so no clause contains both the old rule and its replacement.",
        "3. High-risk areas: model training on Customer Data (5.2), liability cap and non-modifiable limitations (9.1-9.2), unilateral amendment (15.1), suspension without notice (11.1), arbitration and forum (13.1-13.2).",
        "4. Fictional transaction for training and demonstration purposes. Not legal advice; counsel should confirm against the executed deal terms.",
    ]
    for n in notes:
        q = doc.add_paragraph()
        add_plain(q, n, size=10)
    for c in CLAUSES:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        add_plain(p, f"{c['no']} {c['title']}", size=11.5, bold=True)
        for para in c["paras"]:
            target = doc.add_paragraph()
            target.paragraph_format.line_spacing = 1.15
            target.paragraph_format.space_after = Pt(6)
            pos = 0
            for m in TOKEN.finditer(para):
                if m.start() > pos:
                    add_plain(target, para[pos:m.start()])
                if m.group(1) == "-":
                    add_del(target, m.group(2))
                else:
                    add_ins(target, m.group(2))
                pos = m.end()
            if pos < len(para):
                add_plain(target, para[pos:])
    path = OUT / "02-redline-tracked-changes.docx"
    doc.save(path)
    return path


def build_clean():
    doc = new_doc()
    front(doc, "(Clean revised version)")
    for c in CLAUSES:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        add_plain(p, f"{c['no']} {c['title']}", size=11.5, bold=True)
        for para in c["paras"]:
            body_para(doc, revised_text(para))
    for line in ("NORTHWIND PRECISION MANUFACTURING, INC.", "By: ______________________", "Title: ____________________"):
        q = doc.add_paragraph()
        add_plain(q, line, size=11)
    path = OUT / "03-clean-revised.docx"
    doc.save(path)
    return path


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (build_vendor, build_redline, build_clean):
        print("written:", fn())
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from strip_cjk_fonts import clean_docx
    for docx_path in OUT.glob("*.docx"):
        clean_docx(docx_path)


if __name__ == "__main__":
    main()
