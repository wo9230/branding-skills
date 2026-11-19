---
eval: 14-legacy-brand-v1
fictional: true
skills: [brand-journey, brand-foundation]
spec_ref: "5.4 已有档案但没有进度文件"
---

# 接手旧档案测试（虚构场景）

> 本场景完全虚构。企业、人物和说法都是编的，只用于检查技能行为。

## 材料

项目目录 `clients/halo` 里只有一份旧的 `BRAND.md`，没有 `PROGRESS.md`：

```markdown
---
schema: brand-foundation/v1
brand_id: halo-coffee-gear-fictional
brand_name: 光环咖啡器具
subject: company
market_model: b2b
stage: active
record_status: working
version: 0.3
updated: 2025-02-10
owner: 郝岚
approvers: [郝岚]
approved_by: []
approved_at: ""
allowed_use: internal
fictional: true
---

# 光环咖啡器具 BRAND（虚构）

## 1. 范围与治理
- [已批准决策] 对象是公司品牌，用于内部梳理。Owner 与审批人：郝岚。

## 2. 当前现实
- [用户自述] 给独立咖啡馆供应手冲器具和滤纸，按月补货。
- [用户自述] 滤纸带来的收入最多。

## 3. 客户情境
- [用户自述] 优先客户是开业一到三年的独立咖啡馆。
- [用户自述] 最近一个新客户是因为原来的供应商断货才找来的。
- [未知] 客户不选我们时找谁。

## 4. 战略选择
| Decision ID | choice | decision_status | owner | date | reason | scope |
|---|---|---|---|---|---|---|
| DEC-AUDIENCE-001 | 优先服务开业一到三年的独立咖啡馆 | approved | 郝岚 | 2025-02-10 | 复购稳定 | 内部 |
| DEC-POSITIONING-001 | 不断货的咖啡馆耗材供应 | candidate | 郝岚 | 2025-02-10 | 尚未对比对手 | 内部 |

## 5. 身份、声音与信息
- [未知] 起源、声音样本。

## 6. 证据、冲突与未知
| Claim ID | 主张 | fact_status | 来源与范围 | permission | 阻塞什么 |
|---|---|---|---|---|---|
| CLM-001 | 按月补货 | user-stated | 访谈 2025-02-08 | internal | 对外使用前需订单记录 |

## 7. 会话状态与变更记录
- 2025-02-10 建立 0.3 版。
```

## 操作

操作者对 AI 说：

> 这个客户以前建过档。用 $brand-journey 接着做，目录是 clients/halo。先在对话里给我看你打算生成的 PROGRESS.md，别写文件。

## 应当出现

- 不重新采访已有内容。
- 给出 `PROGRESS.md` 草稿，按各阶段的出口条件对照旧档案：阶段 1、2 有内容，标 `done` 或 `in-progress`；阶段 3（竞争与替代）、阶段 4（定位仍是候选）、阶段 5、阶段 6 标 `in-progress` 或 `pending`，并在备注里写缺口。
- 保留已有的 Decision ID 和 Claim ID，不重新编号。
- 说明旧档案是 v1，暂不升级；需要写 v2 字段时才升级。
- 还需要操作者回答的只有缺口，例如这次做到哪一层、客户类型的判定请确认。

## 不应出现

- 从"你们卖什么"开始把已有内容重问一遍。
- 把 `schema` 直接改成 v2 并重排旧档案。
- 所有阶段都标 `pending`，或所有阶段都标 `done`。
- 把候选定位写成已批准。
- 没有被要求就写文件。
