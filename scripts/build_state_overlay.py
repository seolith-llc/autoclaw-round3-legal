# -*- coding: utf-8 -*-
"""Build the multi-state overlay workbook for the Northwind footprint."""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3\deliverables\08-state-overlay.xlsx")

HEAD_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
BODY = Font(name="Calibri", size=10)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

SEV_FILL = {
    "Driver": PatternFill("solid", fgColor="C00000"),
    "Yes": PatternFill("solid", fgColor="F4CCCC"),
    "Conditional": PatternFill("solid", fgColor="FCE5CD"),
    "No": PatternFill("solid", fgColor="D9EAD3"),
}
SEV_FONT = {
    "Driver": Font(name="Calibri", size=10, bold=True, color="FFFFFF"),
    "Yes": Font(name="Calibri", size=10, bold=True, color="990000"),
    "Conditional": Font(name="Calibri", size=10, bold=True, color="B45F06"),
    "No": Font(name="Calibri", size=10, bold=True, color="274E13"),
}

STATES = [
    ("California", "CCPA / CPRA", "Cal. Civ. Code 1798.100 et seq.",
     "Business doing business in CA meeting one of the statutory thresholds (revenue, consumer volume, or data-selling share).",
     "Employees and job applicants ARE covered.", "Driver",
     "Only state in the footprint where the workforce data in the platform is protected data. Drives the DPA."),
    ("Virginia", "VCDPA", "Va. Code 59.1-575 et seq.",
     "Persons conducting business in VA or targeting residents, above the statutory processing thresholds.",
     "Consumer excludes commercial and employment context (59.1-575).", "Conditional",
     "Applies only if the platform touches Virginia consumers. Processor duties are the drafting template."),
    ("Maryland", "MODPA (eff. Oct 1, 2025)", "Md. Code, Com. Law 14-4601 et seq.",
     "Persons conducting business in MD or targeting residents, above the statutory thresholds.",
     "Consumer excludes commercial and employment context (14-4601(H)).", "Conditional",
     "Violations are unfair, abusive, or deceptive trade practices under the Maryland Consumer Protection Act."),
    ("Delaware", "DPDPA", "6 Del. C. ch. 12D",
     "35,000 consumers, or 10,000 consumers plus more than 20% of gross revenue from selling personal data (12D-103(a)).",
     "Consumer excludes commercial and employment context (12D-102(8)).", "Conditional",
     "Threshold is consumer-count based; a 400-person manufacturer's own workforce does not get there."),
    ("Texas", "TDPSA", "Tex. Bus. & Com. Code ch. 541",
     "Conducts business in TX or produces a product or service consumed by residents, processes or sells personal data, and is not a small business (541.002(a)).",
     "Consumer excludes commercial and employment context (541.001(7)).", "Conditional",
     "Small-business exemption is the swing factor; selling sensitive data removes it."),
    ("District of Columbia", "No comprehensive statute", "D.C. Code 28-3901 et seq. (CPPA)",
     "No comprehensive consumer privacy law identified. General consumer protection and breach-notification law apply.",
     "n/a", "No",
     "Contract and security obligations here come from the agreement, not a privacy statute. Breach notice still applies."),
]

REQS = [
    ("Purpose limitation",
     "Personal information disclosed only for limited and specified purposes.",
     "1798.100(d)(1)", "All five require a written controller-processor contract; this list is the common core. Quote from CA and VA, which are verified in text."),
    ("Same level of protection",
     "Processor must comply with the statute and provide the same level of privacy protection.",
     "1798.100(d)(2)", "Verified in CA text."),
    ("Audit / assurance rights",
     "Controller may take reasonable steps to ensure compliant use; processor must make information available and allow assessments.",
     "1798.100(d)(3); 59.1-579(B)(3)-(4)", "VA allows either direct assessment or an independent assessor report."),
    ("Notice of inability to comply",
     "Processor must notify the controller if it can no longer meet its obligations.",
     "1798.100(d)(4)", "Verified in CA text."),
    ("Stop and remediate",
     "Controller may stop and remediate unauthorized use.",
     "1798.100(d)(5)", "Verified in CA text."),
    ("Confidentiality of personnel",
     "Everyone processing the data is under a duty of confidentiality.",
     "59.1-579(B)(1)", "Verified in VA text; covered by NDA in our redline Section 8."),
    ("Return or deletion",
     "At the controller's direction, return or delete data at end of services unless retention is required by law.",
     "59.1-579(B)(2)", "Verified in VA text; missing from the vendor draft."),
    ("Subcontractor flow-down",
     "Subcontractors engaged under a written contract meeting the processor's obligations.",
     "59.1-579(B)(5)", "Verified in VA text; the draft allows unbound subcontractors."),
]


def style_head(ws, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(1, c)
        cell.fill = HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = CENTER
        cell.border = BORDER
    ws.row_dimensions[1].height = 30


def main():
    wb = Workbook()

    ws = wb.active
    ws.title = "Footprint"
    ws["A1"] = "State Overlay - Northwind footprint"
    ws["A1"].font = Font(name="Calibri", size=16, bold=True, color="1F3864")
    ws["A2"] = ("Offices: Virginia, District of Columbia, Maryland, Delaware. Remote staff: California, Texas. "
                "Fictional sample. Review date November 6, 2026.")
    ws["A2"].font = Font(name="Calibri", size=10, italic=True, color="666666")

    headers = ["Jurisdiction", "Regime", "Citation", "Applies if", "Workforce data covered?", "Status", "Why it matters here"]
    ws.append([])
    ws.append(headers)
    header_row = ws.max_row
    for c in range(1, len(headers) + 1):
        cell = ws.cell(header_row, c)
        cell.fill = HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = CENTER
        cell.border = BORDER
    for row in STATES:
        ws.append(row + ())
        r = ws.max_row
        for c in range(1, len(headers) + 1):
            cell = ws.cell(r, c)
            cell.font = BODY
            cell.alignment = WRAP
            cell.border = BORDER
        st = ws.cell(r, 6)
        st.fill = SEV_FILL[row[5]]
        st.font = SEV_FONT[row[5]]
        st.alignment = CENTER
    for i, w in enumerate([18, 20, 26, 52, 34, 12, 48], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = f"A{header_row + 1}"

    r = ws.max_row + 2
    ws.cell(r, 1, "Reading this table").font = Font(name="Calibri", size=12, bold=True)
    notes = [
        "One contract, six jurisdictions. The Ohio choice-of-law clause picks the body of contract law; it does not pick the privacy statutes.",
        "Five of the six comprehensive statutes exclude commercial and employment data. California does not. That single difference is why the DPA is California-shaped.",
        "Only one regime is a driver for this deal. The other four apply only if the platform starts processing consumer data, which today it does not.",
        "District of Columbia has no comprehensive privacy statute, so the obligation there comes from the contract and from breach-notification law.",
    ]
    for i, n in enumerate(notes, start=1):
        cell = ws.cell(r + i, 1, f"{i}. {n}")
        cell.font = BODY
        cell.alignment = WRAP
        ws.merge_cells(start_row=r + i, start_column=1, end_row=r + i, end_column=7)

    ws2 = wb.create_sheet("DPA requirements")
    h2 = ["Requirement", "What it means", "Verified citation", "Notes"]
    ws2.append(h2)
    style_head(ws2, len(h2))
    for row in REQS:
        ws2.append(row)
        rr = ws2.max_row
        for c in range(1, len(h2) + 1):
            cell = ws2.cell(rr, c)
            cell.font = BODY
            cell.alignment = WRAP
            cell.border = BORDER
    for i, w in enumerate([28, 56, 30, 52], start=1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "A2"

    ws3 = wb.create_sheet("Clause map")
    h3 = ["Requirement", "Where the redline puts it", "Gap in the vendor draft", "Status"]
    ws3.append(h3)
    style_head(ws3, len(h3))
    mapping = [
        ("Purpose limitation", "Section 5.2 (limited license)", "Draft grants training rights", "Fixed in redline"),
        ("No third-party sharing", "Section 5.2, Section 8, Exhibit B", "Draft permits transferable license", "Fixed in redline"),
        ("CCPA contract terms", "Section 6.3 + Exhibit B (DPA)", "No DPA exists", "Added as condition precedent"),
        ("Breach notification", "Section 6.2 (72 hours)", "'Commercially reasonable time'", "Fixed in redline"),
        ("Audit / assurance", "Section 6.1 (SOC 2 Type II)", "No assurance right", "Fixed in redline"),
        ("Confidentiality duty", "Section 8.1 (mutual)", "One-way, perpetual, Customer only", "Fixed in redline"),
        ("Deletion / return", "Exhibit B (DPA)", "Not addressed anywhere", "Open - add to DPA"),
        ("Subcontractor flow-down", "Section 14.1", "Unbound assignment and subcontracting", "Fixed in redline"),
    ]
    for row in mapping:
        ws3.append(row)
        rr = ws3.max_row
        for c in range(1, len(h3) + 1):
            cell = ws3.cell(rr, c)
            cell.font = BODY
            cell.alignment = WRAP
            cell.border = BORDER
    for i, w in enumerate([28, 40, 42, 26], start=1):
        ws3.column_dimensions[get_column_letter(i)].width = w

    wb.save(OUT)
    print("written:", OUT)


if __name__ == "__main__":
    main()
