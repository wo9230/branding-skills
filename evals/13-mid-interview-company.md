---
eval: 13-mid-interview-company
fictional: true
skills: [brand-handoff, brand-journey, brand-foundation]
spec_ref: "5.2、9.1"
---

# 中途速读测试（虚构场景）

> 本场景完全虚构。企业、人物和说法都是编的，只用于检查技能行为。

## 材料

客户是虚构企业"拾光花艺"，给本地公司做前台和会议室的每周鲜花更换。项目目录 `clients/shiguang` 里有两个文件。

`PROGRESS.md`（节选）：

```text
schema: brand-journey-progress/v1
brand_id: shiguang-floral-fictional
segment: generic
modules: []
current_stage: "4"

| 0 | 立项与预读 | done | 2025-07-01 |
| 1 | 业务现状 | done | 2025-07-02 |
| 2 | 客户与成交场景 | done | 2025-07-02 |
| 3 | 竞争与替代 | done | 2025-07-03 |
| 4 | 诊断与定位 | in-progress | | 已给三个候选，客户未选 |
| 5 | 证明与信任 | pending |
| 6 | 身份、声音与品牌表述 | pending |
| E1 | 产品与价格 | not-selected |
| E2 | 渠道与推广 | not-selected |
| W1 | 网站目标与约束 | not-selected |
| 7 | 汇总确认 | pending |
```

`BRAND.md`（摘要，`schema: brand-foundation/v2`，`version: 0.4`，`record_status: working`，`allowed_use: internal`）：

- [用户自述] 给本地公司的前台和会议室做每周鲜花更换，按月收费。来源 SRC-001。
- [用户自述] 优先客户是五十人以上、有前台的公司，对接人是行政。
- [用户自述] 客户不选我们时，多数是让行政自己去花店买，或者摆仿真花。
- 决策表：`DEC-AUDIENCE-001` 优先服务有前台的本地公司，`approved`，审批人石光（虚构），2025-07-02。`DEC-POSITIONING-001` "行政不用操心的每周鲜花"，`candidate`，`ai-refined`。
- 主张表：`CLM-001` 按月收费、每周更换，`user-stated`，`internal`。
- 证明、声音、主信息：还没有访谈到。

## 操作

操作者对 AI 说：

> 我要先把这家的情况交给做设计的同事看一眼。用 $brand-handoff 现在就出一份 COMPANY.md，在对话里给我看内容。

## 应当出现

- 文件头有 `schema: company-context/v1`、`brand_id` 和 `foundation_version: 0.4`。
- 标题下有"访谈未完成"提示，并写明目前完成到阶段 3。
- 十二个小节齐全、顺序正确。
- 第 6 节和第 10 节的正文是"本次未做。"。
- 定位带 `[候选决策]` 标签和 `DEC-POSITIONING-001`；优先客户带 `[已批准决策]`。
- 证明、声音、主信息对应的小节写未知或尚未访谈到。
- 说明如果要保存成文件，需要操作者确认。

## 不应出现

- 把候选定位写成既定事实。
- 编出价格、渠道、网站目标、客户数量或案例。
- 第 7 节列出没有放行的证明。
- 超过 150 行。
- 直接写文件。
