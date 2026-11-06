# -*- coding: utf-8 -*-
"""生成合同审查风险矩阵 xlsx。"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.drawing.fill import PatternFillProperties, ColorChoice

OUT = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3\deliverables\05-风险矩阵.xlsx")

HEAD_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
BODY_FONT = Font(name="微软雅黑", size=10)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

LEVEL_FILL = {
    "高": PatternFill("solid", fgColor="F4CCCC"),
    "中": PatternFill("solid", fgColor="FCE5CD"),
    "低": PatternFill("solid", fgColor="D9EAD3"),
}
LEVEL_FONT = {
    "高": Font(name="微软雅黑", size=10, bold=True, color="990000"),
    "中": Font(name="微软雅黑", size=10, bold=True, color="B45F06"),
    "低": Font(name="微软雅黑", size=10, bold=True, color="274E13"),
}

ROWS = [
    ("R01", "1.1/1.2", "服务范围“以官网当时公布为准”、平台“按现状提供”", "高", "民法典 §510、§511、§497", "附件一《服务说明书》固化功能、数量上限、时效；保证通常效用", "必改", "法务+采购"),
    ("R02", "2.2", "自动续期12个月，续期价按乙方届时价目", "中", "民法典 §496、§509", "改双方通知续约；期满未续约退还已付未消费费用", "可让步（提醒义务）", "法务"),
    ("R03", "2.3", "甲方不得解除合同，提前终止付剩余期间30%违约金", "高", "民法典 §563、§497第3项", "恢复甲方解除权，按剩余期间比例退款", "必改", "法务"),
    ("R04", "3.1", "签订后5个工作日一次性预付全款，无验收", "高", "民法典 §525、§526、§577", "50%+验收后付清，其后按年度支付", "必改", "财务+法务"),
    ("R05", "3.2", "乙方单方调价，官网公布7日后自动适用", "高", "民法典 §497第2/3项", "服务期内锁价；续约涨幅≤5%", "必改", "法务"),
    ("R06", "3.3", "逾期付款日0.5%违约金", "中", "民法典 §585 及合同编通则解释 §65", "降至日0.05%并设总额上限", "可让步至0.1%", "财务"),
    ("R07", "4.2", "SLA未达标仅延期不赔偿；上游故障不计入", "高", "民法典 §577、§584、§497", "按当月服务费10%付违约金；连续5日<95%可解约；上游故障计入", "必改", "IT+法务"),
    ("R08", "5.2", "甲方数据全球、免费、不可撤销、可转授权许可，可用于模型训练与商业分析", "高", "个保法 §6、§21、§23；数安法 §32", "删除；乙方仅为履行合同在中国境内处理；禁用于训练/开发/分析", "红线不让", "法务+安全"),
    ("R09", "5.3", "衍生数据、统计成果、模型及算法全部归乙方", "中", "民法典 §127；反不正当竞争法 §9", "通用模型归乙方但不得含甲方数据与商业秘密；统计成果归甲方", "可谈", "法务"),
    ("R10", "6.1", "无《个人信息委托处理协议》", "高", "个保法 §21、§55、§59", "签署附件二DPA，约定目的/期限/方式/种类/措施/监督", "红线不让", "法务+安全"),
    ("R11", "6.2", "数据泄露、丢失、损坏“一切损失乙方不承担责任”", "高", "个保法 §57、§69；数安法 §29；民法典 §506", "改为补救、告知、上报并赔偿", "红线不让", "法务"),
    ("R12", "7.1", "乙方可随时下线功能模块，无需通知", "高", "民法典 §509、§511、§563", "核心模块提前30日通知并经同意；影响合同目的可解约退款", "必改", "IT+法务"),
    ("R13", "8.1", "保密义务仅甲方承担，期限3年", "中", "民法典 §509", "双向保密，至进入公有领域；乙方人员签保密承诺", "可谈", "法务"),
    ("R14", "9.1", "赔偿以已付服务费30%为限，不含间接损失", "高", "民法典 §497、§584", "上限改为合同总额，含可预见间接损失，故意/重大过失除外", "必改", "法务"),
    ("R15", "9.2", "约定甲方不得请求法院/仲裁机构调整违约金", "高", "合同编通则解释 §64第3款", "删除（写了也无效），改为确认保留法定调整权", "必改·无需谈判", "法务"),
    ("R16", "10.2", "“甲方不得以任何理由解除本合同”", "高", "民法典 §563、§497第3项", "删除；明示甲方享有法定解除权", "必改", "法务"),
    ("R17", "11.1", "提交乙方所在地仲裁委员会仲裁（机构不明确）", "高", "仲裁法（2026-03-01施行）", "改甲方所在地法院诉讼；如保留仲裁须指定具体机构并按新法复核", "必改", "法务"),
    ("R18", "11.2", "败诉方承担对方全部律师费、仲裁费", "中", "民法典 §584", "改为违约方承担合理且有票据的费用", "可谈", "法务"),
    ("R19", "12.2", "不可抗力包括上游服务商故障、政策调整、市场变化", "高", "民法典 §180、§590", "回归法定定义，排除上述情形", "必改", "法务"),
    ("R20", "12.1", "“甲方已充分理解并接受全部条款”", "中", "民法典 §496；合同编通则解释 §10", "免责条款加粗提示并留存说明记录；勾选/弹窗不足以免责", "程序必做", "法务"),
]


def style_header(ws, row, ncols):
    for col in range(1, ncols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = CENTER
        cell.border = BORDER


def main():
    wb = Workbook()

    # ---------- 概览 ----------
    ws = wb.active
    ws.title = "概览"
    ws["A1"] = "工业设备远程运维数据平台服务合同 · 风险矩阵概览"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F3864")
    ws["A2"] = "审查日期 2026-11-06 ｜ 法域：中华人民共和国 ｜ 主体均为演示用虚构 ｜ 审查：AutoClaw"
    ws["A2"].font = Font(name="微软雅黑", size=10, italic=True, color="666666")

    ws["A4"] = "风险等级分布"
    ws["A4"].font = Font(name="微软雅黑", size=12, bold=True)
    ws["A5"] = "等级"
    ws["B5"] = "数量"
    ws["C5"] = "占比"
    style_header(ws, 5, 3)
    high = sum(1 for r in ROWS if r[3] == "高")
    mid = sum(1 for r in ROWS if r[3] == "中")
    low = sum(1 for r in ROWS if r[3] == "低")
    total = len(ROWS)
    for i, (lv, n) in enumerate((("高", high), ("中", mid), ("低", low)), start=6):
        ws.cell(i, 1, lv).font = LEVEL_FONT[lv]
        ws.cell(i, 1).fill = LEVEL_FILL[lv]
        ws.cell(i, 1).alignment = CENTER
        ws.cell(i, 1).border = BORDER
        ws.cell(i, 2, n).font = BODY_FONT
        ws.cell(i, 2).alignment = CENTER
        ws.cell(i, 2).border = BORDER
        ws.cell(i, 3, n / total).number_format = "0%"
        ws.cell(i, 3).font = BODY_FONT
        ws.cell(i, 3).alignment = CENTER
        ws.cell(i, 3).border = BORDER

    chart = BarChart()
    chart.type = "col"
    chart.title = "风险等级分布"
    chart.y_axis.title = "条款数"
    chart.x_axis.title = None
    chart.legend = None
    data = Reference(ws, min_col=2, min_row=5, max_row=8)
    cats = Reference(ws, min_col=1, min_row=6, max_row=8)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.shape = 4
    chart.style = 10
    chart.width = 12
    chart.height = 7
    ws.add_chart(chart, "E4")

    ws["A10"] = "签署前提（五项必改）"
    ws["A10"].font = Font(name="微软雅黑", size=12, bold=True)
    must = [
        "1. 第5.2条 数据许可 —— 删除全球/不可撤销/模型训练许可（红线）",
        "2. 第9.1/9.2条 责任限额与禁止调整违约金 —— 9.2写了也无效",
        "3. 第2.3条与第10.2条 解除权 —— 恢复甲方法定解除权",
        "4. 第6.1条 委托处理协议 —— 个保法第21条强制要求",
        "5. 第11.1条 管辖 —— 仲裁机构不明确，改甲方所在地法院",
    ]
    for i, m in enumerate(must, start=11):
        ws.cell(i, 1, m).font = Font(name="微软雅黑", size=11, color="990000")
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=6)

    ws["A17"] = "总体结论"
    ws["A17"].font = Font(name="微软雅黑", size=12, bold=True)
    ws["A18"] = (
        f"共识别 {total} 项风险：高 {high} 项、中 {mid} 项、低 {low} 项。"
        "不建议按供应商原稿签署。数据与个人信息条款属合规红线，不能用商务条件交换；"
        "9.2（禁止调整违约金）依司法解释直接无效，无需谈判。"
    )
    ws["A18"].font = BODY_FONT
    ws["A18"].alignment = WRAP
    ws.merge_cells("A18:F20")

    ws.column_dimensions["A"].width = 110
    for col in "BCDEF":
        ws.column_dimensions[col].width = 14

    # ---------- 矩阵 ----------
    ws2 = wb.create_sheet("风险矩阵")
    headers = ["编号", "条款", "风险点", "等级", "法律依据", "修改建议", "处置", "责任方"]
    ws2.append(headers)
    style_header(ws2, 1, len(headers))
    for row in ROWS:
        ws2.append(row)
        r = ws2.max_row
        lv = row[3]
        for c in range(1, len(headers) + 1):
            cell = ws2.cell(r, c)
            cell.font = BODY_FONT
            cell.alignment = WRAP
            cell.border = BORDER
        ws2.cell(r, 1).alignment = CENTER
        ws2.cell(r, 4).font = LEVEL_FONT[lv]
        ws2.cell(r, 4).fill = LEVEL_FILL[lv]
        ws2.cell(r, 4).alignment = CENTER
        ws2.cell(r, 7).alignment = CENTER

    widths = [8, 10, 46, 8, 34, 52, 16, 12]
    for i, w in enumerate(widths, start=1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = f"A1:H{ws2.max_row}"
    ws2.row_dimensions[1].height = 22

    # ---------- 谈判 ----------
    ws3 = wb.create_sheet("谈判筹码")
    ws3.append(["优先级", "条款", "策略", "可交换条件"])
    style_header(ws3, 1, 4)
    tactics = [
        ("红线不让", "5.2 / 6.1 / 6.2 / 9.2", "数据合规是法定义务，声明“此为合规要求，非商务条件”；9.2 直接出示司法解释第64条第3款", "不以价格换数据"),
        ("必改", "2.3/10.2、3.1、3.2、4.2、7.1、9.1、11.1、12.2", "用修订稿逐条替换，不接受“行业惯例”说法", "可接受合理SLA指标与验收标准"),
        ("可让步", "2.2、3.3、8.1、11.2", "作为交换筹码", "换取红线条款通过；逾期违约金可让至0.1%"),
        ("程序必做", "12.1", "免责条款加粗，会谈纪要留存说明记录", "无"),
    ]
    for t in tactics:
        ws3.append(t)
        r = ws3.max_row
        for c in range(1, 5):
            ws3.cell(r, c).font = BODY_FONT
            ws3.cell(r, c).alignment = WRAP
            ws3.cell(r, c).border = BORDER
        ws3.cell(r, 1).font = Font(name="微软雅黑", size=10, bold=True)
    for i, w in enumerate([14, 40, 62, 40], start=1):
        ws3.column_dimensions[get_column_letter(i)].width = w
    ws3.row_dimensions[1].height = 22

    wb.save(OUT)
    print("written:", OUT, "rows:", len(ROWS), "high:", high, "mid:", mid)


if __name__ == "__main__":
    main()
