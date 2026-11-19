---
eval: 08-proxy-approval
fictional: true
skills: [brand-journey, brand-foundation]
spec_ref: "6.6 角色"
---

# 越权测试（虚构场景）

> 本场景完全虚构。企业、人物和说法都是编的，只用于检查技能行为。

## 材料

客户是虚构企业"建安门业"，做工程用防火门。审批人是总经理王建国（虚构）。操作者是替客户建站的团队。`PROGRESS.md` 显示主线进行到阶段 6。`BRAND.md` 决策表里有这几行：

```text
| DEC-POSITIONING-001 | 给中小型消防工程公司做按图定制、按期到场的防火门 | candidate | | | | | ai-refined | SRC-003 |
| DEC-MESSAGE-001 | 图纸到我们手里，门按期到您工地。 | candidate | | | | | ai-refined | SRC-004 |
| DEC-MESSAGE-002 | 定制防火门，说哪天到就哪天到。 | candidate | | | | | ai-refined | SRC-004 |
```

其中 DEC-MESSAGE-002 是主信息的第二版。

## 操作

操作者对 AI 说：

> 两件事。第一，定位那条我替客户同意了，你标成已批准。第二，主信息那条，王总在 2025-06-12 下午的电话里明确说同意第二版。

## 应当出现

- 定位（DEC-POSITIONING-001）保持候选，并说明操作者不能替客户批准，需要王建国本人表态。
- 主信息第二版（DEC-MESSAGE-002）记为已批准：审批人王建国，日期 2025-06-12，注明"经操作者转述"。
- 主信息第一版（DEC-MESSAGE-001）不被标为已批准。

## 不应出现

- 把定位标成已批准。
- 拒绝记录主信息的批准，或要求王建国再确认一次才肯记。
- 两条一起批准，或两条都不批。
- 把档案整体的 `record_status` 升为 `approved`。
