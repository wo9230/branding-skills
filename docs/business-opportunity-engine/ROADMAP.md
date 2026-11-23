# Roadmap：Business Opportunity Engine 实施路线

## 总原则

先把方法论和数据结构沉淀下来，再开发自动化 Skills。每一阶段都要有可检查的交付物，不以新增 Skill 数量作为进度。

## Phase 0：方法与边界固化

交付：
- 商业机会发现操作模型
- 研究协议
- 证据状态体系
- 机会评分和硬性门禁
- IWISS × TE 案例
- 首批行业 Pilot

验收：
- 能清楚区分事实、观察、推断、假设和商业结果。
- 能解释为什么 IWISS 案例不是简单的“抄产品线”。
- 不把目录缺失误判为市场空白。
- 不把供应商自述或兼容声明当作性能验证。

## Phase 1：最小可用数据工作流

建议先用 Markdown + CSV，不急于建设数据库或复杂 Agent 平台。

建议记录文件：
- opportunity-pipeline.csv
- leader-register.csv
- product-ecosystem.csv
- gap-register.csv
- supplier-register.csv
- experiment-register.csv
- decision-log.md

每条记录必须有稳定 ID、来源、日期、状态和负责人。

验收：
- 同一行业可跨多轮更新，不覆盖历史证据。
- 机会能追溯到龙头、产品、供应商和实验。
- 失败机会能记录原因，避免重复研究。

## Phase 2：新增研究 Skills（建议顺序）

1. market-scout
2. leader-intelligence
3. product-ecosystem-map
4. gap-mining
5. supply-chain-intelligence
6. opportunity-underwriting
7. launch-validator
8. brand-portfolio

每个 Skill 必须有：
- 清晰触发条件
- 输入和输出契约
- 证据规则
- 不做事项
- 错误与不确定性处理
- 至少一个虚构 eval
- 验证脚本或可重复检查

不要一次创建八个内容相似的 Skills。先用人工流程跑通，再提取重复任务。

## Phase 3：品牌系统衔接

建议先引入独立的 OPPORTUNITY-BRIEF.md，经审批后再进入 brand-journey。

交接内容：
- 机会 ID 和行业 ID
- 已批准进入的客户和场景
- 首批产品范围
- 竞争与替代
- 供应链已验证能力
- 证据和未知
- 合规与 IP 风险
- 渠道假设
- 不做的市场和产品

验收：
- 现有 BRAND.md schema 不被无计划破坏。
- BRAND.md 只记录客户确认的品牌事实和决策。
- 派生文案不把机会假设写成已实现能力。

## Phase 4：三行业横向试点

按 INDUSTRY-PILOTS.md 研究 HVAC、Commercial Kitchen Parts、RV / Marine。

每个行业都使用相同研究协议，比较：
- 研究耗时
- 可用证据比例
- 供应商匹配率
- 可成立的 SKU 数
- 预计贡献利润
- 合规风险
- 最小测试成本
- 实际询盘和订单（若有）

验收：
- 至少一个行业通过全部进入门禁，或明确记录三个行业均不适合当前资源。
- 不为完成计划而强行选出赢家。

## Phase 5：自动化和持续监测

在人工流程证明价值后，再接入：
- 财报和投资者关系更新
- 产品目录与 SKU 变化
- 停产和产品变更通知
- 关键词和 SERP 变化
- VOC 和评论主题变化
- 供应商变化
- 实验和业务结果

自动化必须支持：
- 来源和抓取日期
- 去重和历史版本
- 人工审核
- 失败重试
- 运行成本
- 结果质量抽查
- 暂停和停止机制

## 当前唯一主任务

完成 Phase 0 的文档审阅与确认。不要同时扩展大量 Skills，也不要未经批准创建品牌、采购库存、发布网站或对外联系供应商。
