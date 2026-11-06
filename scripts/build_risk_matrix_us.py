# -*- coding: utf-8 -*-
"""Build the US-law risk matrix workbook."""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3\deliverables\05-risk-matrix.xlsx")

HEAD_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
BODY_FONT = Font(name="Calibri", size=10)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

LEVEL_FILL = {
    "Critical": PatternFill("solid", fgColor="C00000"),
    "High": PatternFill("solid", fgColor="F4CCCC"),
    "Medium": PatternFill("solid", fgColor="FCE5CD"),
}
LEVEL_FONT = {
    "Critical": Font(name="Calibri", size=10, bold=True, color="FFFFFF"),
    "High": Font(name="Calibri", size=10, bold=True, color="990000"),
    "Medium": Font(name="Calibri", size=10, bold=True, color="B45F06"),
}

ROWS = [
    ("R01", "1.1", "Deliverable defined by vendor's website, changeable at vendor's discretion", "High",
     "Contract certainty; no ascertainable standard to breach", "Bind feature set, seats, retention, response times to Exhibit A", "Must fix", "Legal + Procurement"),
    ("R02", "1.2", "Unilateral modification or discontinuation of any feature without notice", "High",
     "Illusory promise; no notice means no cure opportunity", "30-day notice for non-core; consent for core; refund on material reduction", "Must fix", "Legal"),
    ("R03", "2.2", "Automatic 12-month renewal on 60-day notice at then-current list price", "High",
     "Cal. Bus. & Prof. Code 17602(b)(2) (15-45 day reminder); 15 U.S.C. 8403", "Affirmative renewal quote; 60-day delivery; 5% cap", "Must fix", "Procurement"),
    ("R04", "2.3", "No termination for convenience; early termination accelerates all remaining fees", "High",
     "Penalty vs. actual damages; unenforceable liquidated damages risk", "Termination on 30 days with pro rata refund; 90 days for Provider", "Must fix", "Legal"),
    ("R05", "3.1", "Annual prepayment in full, non-refundable, no acceptance gate", "Medium",
     "Credit risk; no performance leverage", "50% signature / 50% production acceptance; refundable if unused", "Trade", "Finance"),
    ("R06", "3.2", "Unilateral fee increase during the Initial Term on 30 days' notice", "Critical",
     "Illusory consideration; no assent to changed price", "Fee lock for Initial Term; renewal cap 5%", "Must fix", "Legal + Finance"),
    ("R07", "3.3", "Interest at 1.5% per month (18% annualized)", "Medium",
     "Usury limits vary by state; enforceability risk above statutory rate", "Reduce to 1.0% per month or lawful maximum", "Trade", "Finance"),
    ("R08", "4.2", "Sole and exclusive remedy is a credit capped at 5% of one month's fee", "High",
     "UCC 2-719(2) failure of essential purpose", "10% per point below target; termination below 95%; credits not exclusive for material breach", "Must fix", "Legal + IT"),
    ("R09", "4.3", "Hosting provider and third-party supplier failures excluded from uptime", "High",
     "Vendor transfers its own infrastructure risk", "Subcontractor failures count as vendor downtime", "Must fix", "IT"),
    ("R10", "5.2", "Perpetual, irrevocable license to use Customer Data to train and improve models", "Critical",
     "Cal. Civ. Code 1798.100(d) limited and specified purposes; 1798.100(c)", "License limited to hosting and display; no training; no third-party disclosure", "Walk-away", "Legal + Security"),
    ("R11", "5.3", "Provider owns all derived data, models, and outputs", "High",
     "Trade secret misappropriation risk; ownership of outputs unclear", "Customer owns outputs; de-identification standard with no re-identification", "Must fix", "Legal"),
    ("R12", "6.1", "'Commercially reasonable' security; no responsibility absent gross negligence", "Critical",
     "Cal. Civ. Code 1798.150 statutory damages $100-$750 per consumer per incident", "Written security program; annual SOC 2 Type II; breach liability restored", "Walk-away", "Security"),
    ("R13", "6.2", "Incident notice within a 'commercially reasonable time'", "High",
     "State breach-notification deadlines run from discovery", "72-hour notice; cooperation; cost-bearing for notice and monitoring", "Must fix", "Security"),
    ("R14", "6.3", "No data processing addendum; no CCPA service-provider terms", "Critical",
     "Cal. Civ. Code 1798.100(d)(1)-(5)", "Execute Exhibit B satisfying 1798.100(d) before any processing", "Walk-away", "Legal + Security"),
    ("R15", "7.1", "All feedback and usage data assigned to Provider", "Medium",
     "Overbroad assignment captures pre-existing IP", "Customer retains feedback; non-exclusive license to Provider", "Trade", "Legal"),
    ("R16", "8.1", "One-way, perpetual confidentiality obligation on Customer only", "Medium",
     "Mismatch with data exposure; unenforceable as to public information", "Mutual; Term plus 3 years; trade secrets while they remain secret", "Trade", "Legal"),
    ("R17", "9.1", "Cap at fees paid in prior 12 months; no consequential damages; no carve-outs", "Critical",
     "UCC 2-719(3); 2-302 unconscionability", "Greater of 12 months' fees or 2x annual fee; carve-outs for gross negligence, willful misconduct, Section 6, indemnity", "Must fix", "Legal + CFO"),
    ("R18", "9.2", "Limitations 'may not be modified by any court or arbitrator'", "High",
     "UCC 2-302; separation of powers over judicial review", "Delete; replace with unenforceable-provision carve-out", "Must fix", "Legal"),
    ("R19", "10.1", "Customer indemnifies Provider for claims caused by Provider's own negligence", "High",
     "Risk transfer of vendor's own tort exposure", "Limit to IP claims arising from Customer Data as permitted", "Must fix", "Legal"),
    ("R20", "11.1", "Immediate suspension on suspicion, with or without notice", "High",
     "De facto termination bypassing Section 2; no cure period", "Notice + 48-hour cure; legal compulsion only for immediate; narrow scope", "Must fix", "Legal + IT"),
    ("R21", "12.1", "'AS IS'; all implied warranties disclaimed; no express warranty", "High",
     "UCC 2-316(1) conflict with express terms; 2-316(3)(a) 'as is'", "Express conformance and workmanlike warranty; disclaimer limited to implied warranties", "Must fix", "Legal"),
    ("R22", "13.1/13.2", "Texas law and forum, plus mandatory arbitration in Austin and a class waiver", "High",
     "Internal inconsistency between forum and arbitration clauses; FAA enforcement", "Ohio law and Cuyahoga County; no mandatory arbitration; severable waiver", "Must fix", "Legal"),
    ("R23", "14.1", "Provider may assign to any affiliate or successor; Customer may not assign", "Medium",
     "Counterparty substitution without consent on a prepaid contract", "Mutual consent; successor exception; competitor carve-out", "Trade", "Legal"),
    ("R24", "15.1", "Provider may amend by posting; continued use is acceptance", "Critical",
     "Assent doctrine; nullifies all negotiated protections", "Signed writing only; exhibits by specified mechanisms", "Must fix", "Legal"),
]


def header(ws, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = CENTER
        cell.border = BORDER
    ws.row_dimensions[1].height = 24


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Overview"
    ws["A1"] = "Risk Matrix - Skyline Device Cloud Master Subscription Agreement"
    ws["A1"].font = Font(name="Calibri", size=16, bold=True, color="1F3864")
    ws["A2"] = "Review date November 6, 2026  |  Governing law proposed: Ohio  |  Fictional sample  |  AutoClaw Legal Review"
    ws["A2"].font = Font(name="Calibri", size=10, italic=True, color="666666")

    crit = sum(1 for r in ROWS if r[3] == "Critical")
    high = sum(1 for r in ROWS if r[3] == "High")
    med = sum(1 for r in ROWS if r[3] == "Medium")
    total = len(ROWS)

    ws["A4"] = "Severity distribution"
    ws["A4"].font = Font(name="Calibri", size=12, bold=True)
    for i, h in enumerate(["Severity", "Count", "Share"], start=1):
        c = ws.cell(5, i, h)
        c.fill = HEAD_FILL
        c.font = HEAD_FONT
        c.alignment = CENTER
        c.border = BORDER
    for i, (label, n) in enumerate((("Critical", crit), ("High", high), ("Medium", med)), start=6):
        a = ws.cell(i, 1, label)
        a.fill = LEVEL_FILL[label]
        a.font = LEVEL_FONT[label]
        a.alignment = CENTER
        a.border = BORDER
        b = ws.cell(i, 2, n)
        b.font = BODY_FONT
        b.alignment = CENTER
        b.border = BORDER
        c = ws.cell(i, 3, n / total)
        c.number_format = "0%"
        c.font = BODY_FONT
        c.alignment = CENTER
        c.border = BORDER

    chart = BarChart()
    chart.type = "col"
    chart.title = "Issues by severity"
    chart.y_axis.title = "Clauses"
    chart.legend = None
    chart.add_data(Reference(ws, min_col=2, min_row=5, max_row=8), titles_from_data=True)
    chart.set_categories(Reference(ws, min_col=1, min_row=6, max_row=8))
    chart.width = 12
    chart.height = 7
    ws.add_chart(chart, "E4")

    ws["A10"] = "Must-fix before signature"
    ws["A10"].font = Font(name="Calibri", size=12, bold=True)
    must = [
        "1. Section 5.2 - data license for model training (walk-away)",
        "2. Section 6.1-6.3 - security program, 72-hour notice, CCPA addendum (walk-away)",
        "3. Section 9.1-9.2 - cap base, carve-outs, delete the non-modification sentence",
        "4. Section 15.1 - no amendment by posting",
        "5. Section 13.1-13.2 - Ohio forum, no mandatory arbitration",
    ]
    for i, m in enumerate(must, start=11):
        ws.cell(i, 1, m).font = Font(name="Calibri", size=11, color="990000")
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=6)

    ws["A17"] = "Overall assessment"
    ws["A17"].font = Font(name="Calibri", size=12, bold=True)
    ws["A18"] = (
        f"{total} issues: {crit} critical, {high} high, {med} medium. Do not sign as drafted. "
        "The critical items are data-governance failures rather than price terms; the liability clause is "
        "aggressive but likely enforceable as to commercial loss, so the negotiation should target carve-outs "
        "and the cap base rather than arguing nullity."
    )
    ws["A18"].font = BODY_FONT
    ws["A18"].alignment = WRAP
    ws.merge_cells("A18:F20")
    ws.column_dimensions["A"].width = 105
    for col in "BCDEF":
        ws.column_dimensions[col].width = 13

    ws2 = wb.create_sheet("Risk Matrix")
    headers = ["ID", "Section", "Issue", "Severity", "Authority / doctrine", "Recommended change", "Disposition", "Owner"]
    ws2.append(headers)
    header(ws2, len(headers))
    for row in ROWS:
        ws2.append(row)
        r = ws2.max_row
        for c in range(1, len(headers) + 1):
            cell = ws2.cell(r, c)
            cell.font = BODY_FONT
            cell.alignment = WRAP
            cell.border = BORDER
        ws2.cell(r, 1).alignment = CENTER
        cell = ws2.cell(r, 4)
        cell.fill = LEVEL_FILL[row[3]]
        cell.font = LEVEL_FONT[row[3]]
        cell.alignment = CENTER
        ws2.cell(r, 7).alignment = CENTER
    for i, w in enumerate([7, 11, 44, 11, 38, 50, 15, 16], start=1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = f"A1:H{ws2.max_row}"

    ws3 = wb.create_sheet("Negotiation Plan")
    ws3.append(["Priority", "Sections", "Approach", "Concession available"])
    header(ws3, 4)
    plan = [
        ("Walk-away", "5.2, 6.1-6.3, 9.2", "Frame as data-governance and statutory compliance, not leverage. Offer price movement to hold these.",
         "Up to 10% fee increase; extended term"),
        ("Must fix", "1.1-1.2, 2.2-2.3, 3.2, 4.2-4.3, 9.1, 11.1, 12.1, 13.1-13.2, 15.1",
         "Redline as drafted. Reject 'market standard' without a citation.", "Credit schedule sizing; notice periods"),
        ("Trade", "3.3, 5.3, 7.1, 8.1, 14.1", "Concede one to protect the walk-away items.", "Interest rate; confidentiality survival; assignment specifics"),
        ("Paper the file", "12.1", "Keep the express warranty even if the disclaimer survives.", "None"),
    ]
    for p in plan:
        ws3.append(p)
        r = ws3.max_row
        for c in range(1, 5):
            ws3.cell(r, c).font = BODY_FONT
            ws3.cell(r, c).alignment = WRAP
            ws3.cell(r, c).border = BORDER
        ws3.cell(r, 1).font = Font(name="Calibri", size=10, bold=True)
    for i, w in enumerate([14, 38, 62, 40], start=1):
        ws3.column_dimensions[get_column_letter(i)].width = w

    wb.save(OUT)
    print("written:", OUT, "rows:", total, "critical:", crit)


if __name__ == "__main__":
    main()
