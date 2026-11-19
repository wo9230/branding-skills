---
eval: 16-add-module-later
fictional: true
skills: [brand-journey, brand-foundation]
spec_ref: "6.1 模块可以事后加开"
---

# 事后加开模块测试（虚构场景）

> 本场景完全虚构。企业、人物和说法都是编的，只用于检查技能行为。

## 材料

客户是虚构企业"岚山户外"，做露营用的折叠桌椅，卖给国内的户外用品店。审批人是负责人蓝珊（虚构）。主线已经做完，当时只要定位。`PROGRESS.md` 节选：

```text
segment: domestic-b2b
modules: []
current_stage: "7"
next_question: ""

阶段 0 到 7 全部为 done，阶段 7 完成于 2025-05-20。
E1、E2、W1 为 not-selected。

关键决策：
- DEC-POSITIONING-001 定位（已批准）
- DEC-MESSAGE-001 主信息（已批准）
```

`BRAND.md` 的 `record_status` 是 `approved`，版本 1.0。客户确认报告是 `reports/2025-05-20-client-confirmation.md`。

## 操作

操作者对 AI 说：

> 客户现在决定要建站了。用 $brand-journey 接着做。

## 应当出现

- 先用几行说明现状：主线已完成，这次是加开建站模块。
- `modules` 改为包含 `website`，W1 由 `not-selected` 改为进行中；E1、E2 仍是 `not-selected`。
- 只走 W1，进度行例如"建站 W1 · 网站目标与约束 · 第 1/5 问"。
- 因为没开落地模块，W1 的必答里包含两问：网站上是否展示价格、访客主要从哪里来。
- 说明 W1 结束后做增量确认：只把新增的决策列给蓝珊确认，不重出整份确认报告。

## 不应出现

- 重走阶段 1 到 6，或重新确认定位。
- 开始问落地模块的整套问题，例如各渠道怎么分工、每月推广做什么。
- 把 E1、E2 改成已选。
- 重新生成整份客户确认报告。
