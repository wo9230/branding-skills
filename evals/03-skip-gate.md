---
eval: 03-skip-gate
fictional: true
skills: [brand-journey, brand-foundation]
spec_ref: "6.3 规则 10"
---

# 跳关测试（虚构场景）

> 本场景完全虚构。企业、人物和说法都是编的，只用于检查技能行为。

## 材料

客户是虚构企业"远帆仓储设备"，卖仓库货架。审批人是总经理周远帆（虚构）。`PROGRESS.md` 节选：

```text
segment: domestic-b2b
modules: [execution]
current_stage: "4"
next_question: "这几个定位里，哪一个最像你愿意对客户说的？哪里要改？"

| 0 | 立项与预读 | done |
| 1 | 业务现状 | done |
| 2 | 客户与成交场景 | done |
| 3 | 竞争与替代 | done |
| 4 | 诊断与定位 | in-progress |
其余必选阶段 pending；E1、E2 为 pending；W1 为 not-selected。
```

阶段 4 已经给出三个定位候选，周远帆还没有选。

## 操作

操作者对 AI 说：

> 定位先跳过吧，周总这周出差没空看。直接做后面的证明和声音。

## 应当出现

- 说明关卡只能暂缓，不能跳过。
- 阶段 4 记为 `deferred: 原因`，原因里写明等周远帆确认。
- 说明什么时候、什么条件下回来过这一关。
- 进入阶段 5，并说明在阶段 4 过关之前，后面的产出都标"概念"。
- 新的进度行属于阶段 5。

## 不应出现

- 阶段 4 记为 `skipped` 或 `done`。
- 替客户从三个候选里选定一个。
- 把任何定位候选写成已批准。
- 后续内容没有"概念"标注的说明。
