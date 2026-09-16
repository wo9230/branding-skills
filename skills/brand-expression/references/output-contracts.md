# 表达交付协议

只有用户明确要求创建、保存、更新、写入或导出文件时才允许落盘。目标目录、附件、读取或评审请求本身不构成写入授权。所有文件写入用户的品牌项目目录，不得写回已安装 Skill。

## `MESSAGING.md`

`MESSAGING.md` 是 `BRAND.md` 的受控表达派生物，不是第二事实源。推荐使用以下 frontmatter：

```yaml
---
schema: brand-expression/v1
brand_id: ""
brand_name: ""
message_status: working
version: 0.1
updated: YYYY-MM-DD
foundation_file: BRAND.md
foundation_version: ""
foundation_read_date: YYYY-MM-DD
intended_use: []
audiences: []
channels: []
owner: ""
approvers: []
approved_by: []
approved_at: ""
allowed_use: internal
---
```

`message_status` 使用 `working | approved | archived`。只有具名 approver 接受当前范围内采用的定位领域、核心信息、承诺、声音和主要 CTA 后才能标 `approved`。

按当前任务选用以下章节，不为完整而填空：

1. **使用说明与状态**：foundation、适用受众/渠道、批准范围和重要限制；
2. **推荐定位与候选领域**：推荐理由、各自取舍和批准状态；
3. **核心信息架构**：受众张力、信念转移、承诺、机制、证明、边界、行动；
4. **使命、愿景与观点**：只保留有事实或决策支撑的部分；
5. **品牌故事素材/成稿**：明确素材范围，不补剧情；
6. **声音系统**：voice basis、关系姿态、可观察写法、禁用模式和场景变化；
7. **表达库**：主张、口号、简介、产品说明或页面文案；
8. **个人 IP 内容支柱**：仅个人/创始人分支；
9. **产品与渠道应用**：仅用户请求的产品和触点；
10. **Claim Map**：所有重要公开句子的来源与放行状态；
11. **验证计划与学习记录**：待测试表达、信号、范围和下一步；
12. **版本记录**：改了什么、为什么、谁批准。

## 公开文案与内部治理分层

公开文案区不得出现 `[用户自述]`、`[候选决策]`、`fact_status` 等内部标签。治理说明和 Claim Map 紧随其后，至少包含：

| Copy ID | 公开表达/用途 | 来源 Claim/Decision ID | 来源状态 | permission | 放行结论与限制 |
|---|---|---|---|---|---|

放行结论使用：

- `approved-public`：内容、证据和权限均适合指定公开范围；
- `approved-internal`：可用于内部讨论，不能公开；
- `candidate`：表达候选，待 owner 选择；
- `proof-required`：表达可以保留为结构，但当前不得公开；
- `blocked`：存在冲突、禁止主张或权限问题。

一个 Copy ID 可引用多个来源；不得让一条低风险来源替整句中的高风险数字、比较或结果背书。

## 渠道成品

用户只要简介、首页首屏、销售页或社交文案时，可以在聊天中直接交付成品，同时附最小 Claim Map。若写入文件，优先更新已有 `MESSAGING.md` 的对应表达库和渠道区，不为每个平台创建一份新的事实文件。

## 更新纪律

更新前重读最新 `BRAND.md` 和 `MESSAGING.md`。foundation 决策变化时，将旧文案标为 superseded/archived 并保留版本记录；不得静默改写后继续沿用旧批准日期。表达测试结果写学习记录，不能反向把候选解释升级为品牌事实。
