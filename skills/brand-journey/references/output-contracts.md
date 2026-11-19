# 主线的输出协议

主线自己只产出两样东西：进度文件 `PROGRESS.md` 和客户确认报告。品牌事实与决策一律按 `$brand-foundation` 的输出协议写进 `BRAND.md`；其余文件由各自的技能派生。

## 写入授权

- 只有操作者明确要求建档或保存时才写文件。读取、检查、评审一个目录时保持只读。
- 操作者在阶段 0 指定了客户项目目录并说开始建档，就视为对该目录里 `PROGRESS.md` 和 `BRAND.md` 的本次访谈持续授权：之后每个阶段出口写这两个文件，不再逐次询问。阶段 0 结束时向操作者明确说一次这件事。
- 客户确认报告和每一份派生文件（`MESSAGING.md`、品牌板、`output/DESIGN.md`、`COMPANY.md`、`SITE-BRIEF.md`）生成前各问一次。
- 任何情况下都不写客户项目目录以外的地方，不写回已安装的技能目录。
- 没有指定项目目录时，内容留在对话里，不猜目录。

## `PROGRESS.md`

放在客户项目根目录。只记流程，不记品牌事实。模板见 [../assets/PROGRESS-TEMPLATE.md](../assets/PROGRESS-TEMPLATE.md)。

文件头：

```yaml
---
schema: brand-journey-progress/v1
brand_id: ""
segment: unknown
modules: []
conduct_mode: live
pace: focused
current_stage: "0"
next_question: ""
updated: YYYY-MM-DD
---
```

- `brand_id`、`segment`：与 `BRAND.md` 文件头相同。`segment` 在阶段 0 判定前为 `unknown`。
- `modules`：已选的可选模块，取 `execution`、`website` 的子集，写成行内列表，例如 `[execution, website]`；`[]` 表示只走必选主线。
- `conduct_mode`：`live | questionnaire | transcript`。
- `pace`：`focused | batch`。
- `current_stage`：当前阶段的编号，取 `0` 到 `7`、`E1`、`E2`、`W1`。
- `next_question`：下一问的原文。续接时从它开始。

阶段表的表头固定为 `| stage | name | status | done_at | note |`，共 11 行，编号与名称照模板，不增不减。

`status` 取值：

| 取值 | 含义 | 可用于 |
|---|---|---|
| `pending` | 还没开始 | 全部阶段 |
| `in-progress` | 正在进行，或已有部分内容 | 全部阶段 |
| `awaiting-evidence` | 问完了，在等客户补资料或证明 | 全部阶段 |
| `done` | 达到"做到什么算完" | 全部阶段 |
| `deferred: 原因` | 暂缓；写明原因和回来的条件 | 全部阶段；关卡没过时必须用它 |
| `skipped: 原因` | 选了又中途放弃 | 只用于可选模块的阶段 |
| `not-selected` | 所属模块没选 | 只用于可选模块的阶段 |

- 必选阶段（`0` 到 `7`）不允许 `skipped: 原因` 和 `not-selected`。
- 模块没选时，它的阶段必须是 `not-selected`；模块选了，它的阶段不能是 `not-selected`。
- `done_at` 写 `YYYY-MM-DD`；`note` 写缺口或原因。

正文另有三节：

- **关键决策**：每条一行，只写 Decision ID 和一句提示，例如 `- DEC-POSITIONING-001 定位（已批准）`。内容以 `BRAND.md` 为准，这里不重复。
- **稍后处理清单**：记法见 [anti-drift.md](anti-drift.md)。
- **会话记录**：每次访谈一行，写日期、进行方式、覆盖的阶段、参与人。

每个阶段出口和每次会话结束，都更新 `current_stage`、`next_question` 和 `updated`。

## 客户确认报告

阶段 7 产出，放在 `reports/YYYY-MM-DD-client-confirmation.md`。模板见 [../assets/CLIENT-REPORT-TEMPLATE.md](../assets/CLIENT-REPORT-TEMPLATE.md)。它是给客户负责人看的，不是内部档案。

用大白话，不出现内部标签：

| 档案里的状态 | 报告里的说法 |
|---|---|
| `[已验证事实]` | 资料里写的（说明是哪份资料） |
| `[用户自述]` | 您说的 |
| `[候选决策]` | 我们的建议，待您确认 |
| `[假设]` | 我们的推测，需要您核实 |
| `[未知]` | 还不清楚 |
| `[已批准决策]` | 您已经确认的 |

顺序固定，结论先行：

1. **一句话结论**：一段话讲清这家企业的定位。选了建站模块时，再加一句网站要完成的事。
2. **品牌的说法**：逐条列出"您原来的说法、建议的说法、为什么这样改"。每条各自有四个选项：同意、修改、保留原来的说法、暂缓。客户此前已经选择保留原话、而 AI 认为它还有不足时，在这一节写一次保留意见，之后不再提。
3. **需要您拍板的事**：其余承重决策逐项列出，每项写清建议和代价，三个选项：同意、修改、暂缓。只列本次做了的部分。
4. **还不清楚的事**：未知事项、为什么重要、谁来补。
5. **这些内容从哪里来**：哪些来自资料，哪些是客户说的，哪些是需要客户核实的推测。
6. **确认**：确认人姓名、职务和日期。

规则：

- 每条保留 Decision ID，方便写回；不出现 `fact_status`、`candidate` 这类字段名和取值。
- 不放没有许可的敏感内容；可见范围与 `BRAND.md` 的 `allowed_use` 一致。
- 报告是快照，不是事实源。客户的答复写回 `BRAND.md` 之后，以 `BRAND.md` 为准。

## 写回批准结果

客户答复后，操作者把结果告诉 AI。逐项处理：

| 客户的选择 | 怎么记 |
|---|---|
| 同意 | 对应决策改为 `approved`，写审批人和日期。这三格只写值本身；经操作者转述的，在 `BRAND.md` 的变更记录里注明"经操作者转述" |
| 修改，并给了改后的原文 | 按原文记为 `approved`，`formed_by` 为 `co-edited` |
| 修改，只给了方向 | 改稿后保持 `candidate`，再请客户确认；每条最多改两轮 |
| 保留原来的说法 | 原话记为 `approved`，`formed_by` 为 `client-original`；AI 的保留意见只记一次 |
| 暂缓 | 保持 `candidate`，记入稍后处理清单 |
| 没有表态 | 保持 `candidate`。沉默不算同意 |

承重选择（品牌对象、优先客户、实际供给、定位与取舍、主信息与承诺、声音方向）全部获批，并且阶段 4 和阶段 7 两个关卡都已通过，才把 `BRAND.md` 的 `record_status` 升为 `approved`，并填 `approval_scope`、`approved_by`、`approved_at`；否则保持 `working`。

客户暂缓的事项不挡这一步，但也不算批准：`approval_scope` 只列已经批准的范围，并在 `BRAND.md` 第 1 组写明哪些暂缓的事项不在本次批准范围。暂缓的是承重选择时，档案保持 `working`。

## 增量确认

事后加开模块时，不重出整份报告。出一份短的，放在 `reports/YYYY-MM-DD-client-confirmation-<模块>.md`，`<模块>` 为 `execution` 或 `website`。开头一句说明它接在哪一天的确认之后；正文只有"需要您拍板的事"（新增的决策）、"还不清楚的事"和"确认"。写回方式同上。

## 派生顺序

阶段 7 之后依次进行，每份生成前各问一次：

1. `MESSAGING.md`：`$brand-expression`，默认做。
2. 品牌板与 `output/DESIGN.md`：`$brand-visual-board`，可选，由操作者决定。
3. `COMPANY.md`：`$brand-handoff`，默认做。
4. `SITE-BRIEF.md`：`$brand-handoff`，只在选了建站模块时做。

- 没有 `MESSAGING.md` 时，建站交接只用 `BRAND.md` 里已批准的最小信息，其余文案位置标"待表达"。
- `COMPANY.md` 可以在访谈中途按要求生成，开头带"访谈未完成"提示，并写明完成到第几阶段。
- 阶段 7 没过关时派生的文件，都带"概念，未批准"提示。

## 更新循环

企业情况变了（改价、换主推品、进新市场），不重走访谈：

1. 用 `$brand-foundation` 的更新方式改 `BRAND.md`，升版本号，写变更记录。
2. 运行 `python3 scripts/check_brand_project.py <客户项目目录>`，看哪些派生文件已经过期。
3. 重新生成过期的派生文件。
4. 新增或改动的决策需要客户确认时，走增量确认。
