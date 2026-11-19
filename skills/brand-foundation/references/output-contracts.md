# 输出协议

`BRAND.md` 是唯一持续更新的品牌事实与决策真源。工作簿是输入，日期报告是快照，`MESSAGING.md` 是表达派生物，视觉板是视觉派生物；它们都不能各自保存一套不同的品牌现实。

使用用户的语言撰写。品牌名、产品名和用户指定的市场语言按原文保留。

正文标签必须继承证据/决策状态：`verified` → `[已验证事实]`，`user-stated` → `[用户自述]`，`hypothesis` → `[假设]`，approved choice → `[已批准决策]`，`candidate` → `[候选决策]`，其余使用 `[未知]/[冲突]/[可能过期]`。不得用泛化 `[事实]` 把用户自述、已验证记录和已批准选择混成一类。

## `BRAND.md`

建议位置：单品牌项目根目录，或用户指定的品牌文件夹。使用 Obsidian 可识别的 YAML frontmatter：

```yaml
---
schema: brand-foundation/v2
brand_id: ""
brand_name: ""
subject: unknown
market_model: unknown
stage: unknown
segment: unknown
operator: ""
record_status: in-progress
version: 0.1
updated: YYYY-MM-DD
languages: []
markets: []
owner: ""
approvers: []
approval_scope: []
approved_by: []
approved_at: ""
allowed_use: internal
---
```

枚举：

- `subject`: `personal | company | product | hybrid | unknown`
- `market_model`: `b2b | b2c | dtc | hybrid | unknown`
- `stage`: `idea | prelaunch | active | rebrand | unknown`
- `record_status`: `in-progress | working | approved | archived`
- `allowed_use`: `internal | client-confidential | public-approved | restricted`
- `segment`: 细分包登记表里的标识（首批为 `export-b2b | domestic-b2b | dtc-ecommerce`），或 `generic`（哪一类都不像），或 `unknown`（还没判断）。登记表在 `$brand-journey` 的 `references/segments/INDEX.md`。
- `operator`: 主持建档的一方，例如替客户建站的团队；没有就留空。操作者不是审批人，不能替 owner 批准决策。

不要为了填满 frontmatter 猜测。未知就保留 `unknown` 或空数组。

### v1 与 v2

`brand-foundation/v2` 是 v1 的超集：七组结构不变，只在文件头和组内增加字段。

- `schema: brand-foundation/v1` 的档案可以直接读取和使用，不要求先升级。
- 只有本次任务需要写入 v2 才有的内容时才升级：把 `schema` 改为 v2，补上 `segment` 与 `operator`，并在变更记录里写明升级日期和原因。
- 升级时不重排、不改写未受影响的内容，已有的 Decision ID、Claim ID 原样保留。
- v2 新增的内容没人回答时写 `[unknown]`；属于本次没做的可选模块时写 `[本次未做]`，不要留空，也不要推测。

### 工作簿转换

`BRAND-WORKBOOK.md` 使用 `brand-foundation-workbook/v1`，并声明 `target_schema: brand-foundation/v2`。旧工作簿若声明 `target_schema: brand-foundation/v1`，照样转换，结果按 v1 写，除非本次任务需要 v2 字段。转换时：

- 除 `record_status` 外，同名 frontmatter 原样映射，空值不补造；转换后依据本页生命周期重新判断 `record_status`，不能机械沿用工作簿初始值；
- 工作簿回答按下方七组归档，原始回答仍只是输入；
- 证据行必须保留 `fact_status`，战略选择必须保留 `decision_status / owner / date / reason / scope`；
- 高信息词必须保真：品牌名、人物/岗位、受众、供给、机制、定位、排除项、状态、owner、日期和范围不得在转换时被近义改写或补强；不确定就保留原文并标未知；
- 同一事实或决定发生冲突时标 `conflicted` 或保留多个决策状态，不静默覆盖；
- 只有转换后的 `BRAND.md` 是持续更新的语义真源。

### `record_status` 生命周期

- `in-progress`：仍在提取材料或访谈，现有内容不足以在不补造的情况下完成本次任务；不得作为下游默认输入。
- `working`：已形成带版本号、用途和缺口的内部工作稿，可以支持声明范围内的任务；关键选择仍可为 `candidate`。缺少批准本身不会把可用工作稿降回 `in-progress`。视觉 committed 模式只有在用户明确指定该 working 版本为本轮依据时才可使用。
- `approved`：具名 owner/approver 已明确接受本次范围内的全部承重选择，并填写 `approval_scope`、`approved_by` 与 `approved_at`。沉默、继续聊天、润色完成或文件存在都不构成批准。
- `archived`：该版本已停用或被替代；默认不得用于新交付。

从 `in-progress` 升为 `working` 的条件，是另一位执行者能在声明范围内继续工作而无需自创品牌对象、实际供给、优先受众、关键取舍或公开承诺。升为 `approved` 时，当前交付所依赖的承重选择至少包括：品牌对象与边界、优先受众及情境、实际供给与适配范围、定位/比较框架与取舍、允许公开的主信息与承诺，以及当前任务实际使用的声音方向。若只批准其中一部分，保持 `working`，同时把单项决定标为 `approved`。

### 新建档案的规范字段

从工作簿、访谈或散乱材料新建完整 `BRAND.md` 时，以下字段必须按同一顺序出现；来源没有回答就写 `[unknown]`，不能因输入形式不同而省略。审计/更新既有档案时不要为满足此表重排未受影响内容。

1. **范围与治理**：current task、brand object、intended use、owner、approvers、permission boundary；
2. **当前现实**：actual offering、commercial state、fit conditions、exclusion conditions、promise limits；v2 另加 business model and revenue mix、product architecture、current price rules and terms、current channels and customer sources、sales follow-up、people and budget；
3. **客户情境**：priority audience、trigger/job、alternatives、buying roles、choice/loss evidence；v2 另加 competition and alternatives table；
4. **战略选择**：v2 先写 diagnosis、guiding policy、positioning five elements，再接固定决策表，包含 Decision ID、choice、decision_status、owner、date、reason、scope，v2 另加 formed_by、origin_ref；
5. **身份、声音与信息**：origin/principles、voice_basis、voice direction、voice samples、main message、supporting points、intended action、public claims；
6. **证据、冲突与未知**：source register、claim register、conflicts、stale material、research gaps；
7. **会话状态与变更记录**：current goal、interaction mode、interaction pace、session status、materials read、decisions recorded、highest-priority gap、next action、change log。

`reason` 只记录来源提供的业务理由、证据或取舍。“明确批准”“用户说了”只能证明 decision_status、owner 和 date，不是决策理由；来源没给理由时，两种入口都写 `[unknown]`。

正文按需要使用以下七组；不适用的组可省略，缺失但会影响当前任务的字段写 `[unknown]`：

### 1. 范围与治理

当前品牌对象、使用目的、对外范围、owner、审批人、敏感信息限制。

### 2. 当前现实

实际存在的产品/服务、交付内容、适配条件、排除条件、承诺限制与当前阶段。

v2 在本组另记经营现状，全部是事实，各带 `fact_status`：

- 业务模式与收入构成；
- 产品架构：有哪些产品线，哪些是主推品；
- **现行**价格规则与交易条款，注明生效日期；
- 现有渠道与客户来源；
- 销售与跟进方式；
- 可投入的人力与预算。

业务模式、产品线和客户来源的基本事实任何时候都记。其余细项由落地模块（见 [strategy-and-execution.md](strategy-and-execution.md)）补全；本次没做落地模块时，细项写 `[本次未做]`。

### 3. 客户情境

优先受众、触发事件/任务、替代方案、选择或流失证据。B2B/DTC/个人分支只在适用时加入。

v2 在本组用一张竞争与替代表记录客户不选我们时的办法，三层都要有：

| 层级 | 替代方案 | 它的定位 | 真实优势 | 对我们的威胁 | 来源与查询日期 |
|---|---|---|---|---|---|

层级取"直接"（同类对手）、"间接"（用别的办法解决同一件事）、"维持现状"（不处理或自己凑合）。"真实优势"写对方确实更强的地方，不写成贬低。对手官网只证明它这样公开表述；没有来源的行写 `[假设]`。

### 4. 战略选择

候选定位、已批准定位、关键取舍、非目标。每项写 `decision_status`、owner、日期和理由。不要让候选与批准版本混排。

v2 在决策表之前先写三项，方法见 [strategy-and-execution.md](strategy-and-execution.md)：

- **诊断**：当前最关键的难题；
- **方针**：主攻什么、放弃什么；
- **定位五要素**：客户会拿来比的替代方案、我们独有的能力或特点、这些特点给客户的价值、最适合的客户、所在的品类，以及合成的一句话。

三项各自对应决策表里的一行，状态以决策表为准。

v2 的决策表固定为九列，表头照写：

| Decision ID | choice | decision_status | owner | date | reason | scope | formed_by | origin_ref |
|---|---|---|---|---|---|---|---|---|

- `decision_status` 一列只写 `candidate`、`approved`、`rejected`、`superseded` 之一，不加标签或说明；正文里的 `[候选决策]`、`[已批准决策]` 由这一列推出。
- 决策表只登记已经有人提出的候选或决定。还没人提出的事项不占行，写进第 6 组的未知。
- `formed_by` 记这条表述是怎样形成的：`client-original`（客户原话直接采用）、`ai-refined`（AI 的优化稿经客户确认）、`co-edited`（客户在优化稿上改过后确认）。`origin_ref` 填原话所在的 Source ID 或 Claim ID。做法见 [refinement.md](refinement.md)。
- 这两列对判断与表述类的决策必填，即前缀为 `DEC-DIAGNOSIS`、`DEC-POLICY`、`DEC-POSITIONING`、`DEC-AUDIENCE`、`DEC-MESSAGE`、`DEC-VOICE` 的行；其他决策可以留空。
- v1 档案的七列决策表照样可读，升级到 v2 时在行尾补两列，旧行不知道就留空。

事实与决策不能混：现行价格规则是事实，放第 2 组；"网站上是否公开价格、怎么展示"是决策，放本组。渠道同理：客户现在从哪来是事实，各渠道今后各管什么是决策。

Decision ID 必须稳定：已有 ID 原样保留；首次创建时按语义类型使用 `DEC-SCOPE-001`、`DEC-OFFER-001`、`DEC-AUDIENCE-001`、`DEC-POSITIONING-001`、`DEC-CLAIM-001`、`DEC-VOICE-001`、`DEC-MESSAGE-001`、`DEC-VISUAL-001` 或 `DEC-OTHER-001`，同类后续递增。不要因为输入来自工作簿或访谈、表格顺序不同或重写措辞而重新编号。

v2 新增七个前缀，编号规则相同：

| 前缀 | 用于 | 何时产生 |
|---|---|---|
| `DEC-DIAGNOSIS` | 最关键的难题 | 任何时候 |
| `DEC-POLICY` | 主攻什么、放弃什么 | 任何时候 |
| `DEC-GOAL` | 当前周期的主要经营目标 | 任何时候 |
| `DEC-PRICE` | 价格是否公开、怎么展示 | 只在落地模块 |
| `DEC-CHANNEL` | 各渠道的角色与取舍 | 只在落地模块 |
| `DEC-PROMO` | 推广主打什么、由谁持续做 | 只在落地模块 |
| `DEC-SITE` | 网站的任务、主转化与约束 | 只在建站模块 |

### 5. 身份、声音与信息

- 可证明的起源事件、原则和观点；
- `voice_basis: observed | designed | mixed`；
- 样本来源、作者与编辑/AI 参与；
- 场景语气、可观察写法、禁用表达及正反例；
- 当前主信息、支持点、行动和可公开主张。

`observed` 需要有来源清楚的代表性样本；`designed` 是想采用的表达方向，不能称为“本人自然文风”。

### 6. 证据、冲突与未知

来源登记用表格，字段含义见 [evidence-and-decisions.md](evidence-and-decisions.md) 的"最小来源记录"：

| Source ID | source_type | location | source_date | checked_at | scope | read_scope | permission |
|---|---|---|---|---|---|---|---|

重要主张用表格：

| Claim ID | 主张 | fact_status | 来源与范围 | permission | 阻塞什么 |
|---|---|---|---|---|---|

编号格式固定，其他文件和自检脚本都按它引用：Source ID 从 `SRC-001` 起，Claim ID 从 `CLM-001` 起，都是三位数字、同类递增；已有编号不重排、不复用。表头的 `Source ID`、`Claim ID` 两个列名照写，不要翻译或改写。"来源与范围"一列用 Source ID 指向来源。

Claim register 只登记材料实际提出的现实主张、用户自述或待验证解释。不要把“不得声称 X”反向扩写成一个新的“X 为 unknown”主张；这类内容保留在批准的排除决定、承诺限制或禁止公开项中。这样同一输入经工作簿与访谈进入时不会因为措辞形式产生不同的虚假主张集合。

另列冲突、过期资料、研究缺口和被排除的虚构/无来源内容。

**AI 的保留意见**（v2）：客户审批人保留了自己的原话，而 AI 认为它没过 [refinement.md](refinement.md) 的某条质量标准时，在这个小标题下记一行：对应的 Decision ID、哪条标准没过、日期。每条决策只记一次，之后不再反复提。它是提醒，不改变决策状态。

如品牌已经进入实际使用，可增加学习记录。学习记录只描述某项已批准或候选表达在指定范围内的观察结果：

| Learning ID | 被测试的决定/文案 | learning_status | 观察范围与日期 | 结果与混杂因素 | 下一步 |
|---|---|---|---|---|---|

不得因为某条文案已获批准就写成 `supported`，也不得因为单次结果直接宣布稳定规律。

### 7. 会话状态与变更记录

保存当前目标、`READY/PARTIAL/RESEARCH-GAP/BLOCKED/DEFERRED` 状态、已读取材料、下一项最高优先级缺口，以及每次修改的日期、内容、理由和批准人。

使用 `$brand-journey` 主持访谈时，阶段进度、下一问和会话记录记在项目根目录的 `PROGRESS.md`。本组只保留变更记录，并写一行指向 `PROGRESS.md`，不重复记流程。

## 日期报告

用户授权文件交付并给出或可解析品牌项目根目录时，默认文件名为该根目录下的 `reports/YYYY-MM-DD-brand-foundation.md`。它是本次判断快照，不复制整份 `BRAND.md`。

报告顺序：

1. **结论与状态**：本次能确定什么，处于哪个访谈状态；
2. **范围与依据**：读了什么、没读到什么、适用范围；
3. **已确认现实**：只写 `verified` 与明确标注的 `user-stated`；
4. **本次决策**：approved、candidate、rejected 分开；
5. **请求的品牌产物**：只输出用户本次要的定位、声音、信息等，不自动扩张；
6. **证据门禁**：哪些句子可公开，哪些仍只能内部使用；
7. **冲突、未知与下一项验证**；
8. **更新摘要**：`BRAND.md` 哪些位置发生变化。

只有用户明确要求创建、保存、更新、写入或导出文件时才允许落盘；目标目录只是目的地信息，不构成写入授权。读取、审计、检查或评审一个目录时保持只读。确认写入意图后再解析品牌项目根目录；路径不明确就留在聊天中，不猜目录。禁止修改已安装 Skill 自身的 `SKILL.md`、`assets/`、`references/` 或 `agents/`。若创建文件，写后重新读取关键 frontmatter、批准状态和高风险主张，确认没有把候选升级。

## 快速一页视图

用户明确需要一页简报时，从 `BRAND.md` 派生：品牌对象、优先受众与任务、实际供给、工作定位、关键取舍、允许使用的证明、语气边界、当前行动、重要未知。它是视图，不成为第二事实源。

## 向 `brand-expression` 交接

下列内容足够时，可将表达任务交给 `$brand-expression`：本次受众与情境、实际供给、批准或明确指定的 working 定位、关键取舍、可用证明、禁止主张、期望行动和声音方向。交接不要求整份档案全部 approved，但必须列出当前表达依赖的候选与未知。

`brand-expression` 可以把同一事实写得更清楚、更有吸引力，不能更改 `BRAND.md` 的事实状态、决策状态或批准范围。若表达过程中发现承重缺口，应返回一个具体 foundation 缺口，而不是在 `MESSAGING.md` 中补造答案。
