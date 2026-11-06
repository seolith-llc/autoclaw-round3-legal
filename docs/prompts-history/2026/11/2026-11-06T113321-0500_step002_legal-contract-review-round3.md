---
step: step002
timestamp: 2026-11-06T11:33:21-05:00
title: AutoClaw Round 3 Legal Practice 合同审查参赛作品
project: amtocsoft-megagent
tags: [legal, contract-review, campaign, round3]
---

# step002 - AutoClaw Round 3 Legal Practice 合同审查参赛作品

## Request

```text
I want to participate and win:
```

### Attachments

- `pasted_text_20261106T162514106Z_af555c88.txt`（6082 字节）——AutoClaw Round 3 活动规则全文。

<details>
<summary>附件要点（原文过长，结构化摘录）</summary>

- 活动时间：2026年11月5日00:00 – 11月20日23:59（UTC+8）
- 四大赛道：Legal Practice（特色赛道，双倍积分）、SMB、Open Creation、Video Creation
- Legal Practice：有效参赛 4,000 credits + 质量奖 4,000 或 杰出奖 52,000，单项最高 56,000
- 其他赛道：2,000 + 2,000 或 26,000
- 参赛方式：关注 @AutoClawAIer → 发布公开 X 帖（提及 @AutoClawAIer 并带 #BuiltWithAutoClaw）→ 提交 Round 3 表单
- 帖子必须说明：做了什么、解决什么问题、AutoClaw 如何帮助、最终结果，并附截图/GIF/视频/链接
- 每条赛道一个有效参赛，最多四个；参与奖按表单顺序取前两名有效参赛
- Legal 强作品需展示来源核验，并附有用交付物（redlines、事实时间线、证据索引、研究备忘、起草文件等）
- 评审：质量奖=任务具体、过程清晰、结果可见、有方法沉淀；杰出奖=再加上完整工作流、关键结果核验、方法可复用
- 红线：不得在公开帖中放 AutoClaw 账号邮箱；须脱敏客户/合同/个人信息

</details>

## Response

选择 Legal Practice 赛道（双倍积分 + 评审明确偏好可核验交付物），完成一套完整合同审查工作流，
而不是一篇"体验分享"。法域：中华人民共和国。

### 产出（work/round3/）

| 文件 | 内容 |
| --- | --- |
| `matter/00-任务背景.md` | 虚构案情与交付物索引 |
| `deliverables/01-供应商原稿-未修改.docx` | 乙方格式合同（13 条） |
| `deliverables/02-修订对照稿-修订模式.docx` | Word 修订模式红线：24 处新增、3 处删除 |
| `deliverables/03-修订后清洁版.docx` | 回签用干净文本 |
| `deliverables/04-审查备忘录.docx/.md` | 逐条意见、谈判优先级、遗留事项，20 个可点击官方来源链接 |
| `deliverables/05-风险矩阵.xlsx` | 20 项风险 × 等级 × 法条 × 建议 × 责任方，三个工作表 + 图表 |
| `deliverables/06-引用核验日志.docx/.md` | 每条硬法律事实的检索路径与核验结论 |
| `deliverables/07-可复用审查清单.docx/.md` | SaaS/数据服务合同 12 项审查清单 |
| `entry/08-参赛发布包.md` | X 帖中英文案、截图脚本、表单字段、杰出奖自查表 |
| `entry/09-审查看板.html` | 单页可视化看板（截图用） |

### 关键判断

- 虚构案情（宁波汇丰精密 × 上海云衍，年费 48 万，3 年期），全程标注演示用，规避真实客户数据。
- 最高风险三处：5.2 数据全球不可撤销许可+模型训练；6.1 无委托处理协议；9.2 约定"不得请求调整违约金"。
- 9.2 不需要谈判——《合同编通则解释》第 64 条第 3 款明确法院不予支持。

### 来源核验（过程有波折，已如实记录）

- 元典法规/案例库当日不可用（5 次调用均失败），切换官方公开文本：
  最高人民法院法释〔2023〕13号全文、最高法典型案例、国家网信办发布的个保法与数安法全文、
  政府网转载民法典第三编、商务部政策库确认新《仲裁法》2026-03-01 施行。
- 共 7 组官方来源、20 个备忘录内链；仲裁法仅引用施行时间，未凭记忆引条文序号。

### 验证

- docx 均可被 python-docx 打开；修订稿 XML 含 24 个 `w:ins`、3 个 `w:del`；
  备忘录 20 个超链接；xlsx 三表 20 行风险数据。
- 脚本：`scripts/build_contract_review.py`、`scripts/build_risk_matrix.py`、`scripts/md_to_docx.py`。

### 用户待办（无法由 Agent 完成）

1. 把 `work/round3/` 推到公开仓库拿到演示 URL
2. 关注 @AutoClawAIer 并截图
3. 按 `entry/08-参赛发布包.md` 发布 X 帖（勿放账号邮箱）
4. 11月20日 23:59（UTC+8）前提交表单

## Follow-ups

- 若用户提供真实（脱敏）合同，可替换虚构案情重跑同一工作流
- 元典库恢复后可补案例引证（当前仅有最高法典型案例）
- 仲裁条款如需保留仲裁，应指定具体机构并按 2026-03-01 施行的新《仲裁法》逐条复核
