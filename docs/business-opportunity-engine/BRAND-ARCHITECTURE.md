# Brand Architecture：跨行业品牌架构与表达适配

## 1. 基本原则

品牌定位必须建立在已验证的市场机会、真实供应能力和客户任务之上。

不要先写漂亮的品牌故事，再寻找产品和事实为它背书。

商业机会研究层提供：
- 目标行业和细分市场
- 目标买家和使用者
- 竞争与替代方案
- 产品生态和主推 SKU
- 供应链能力和限制
- 质量、认证和服务证据
- 渠道和交易方式

现有 BRAND.md 仍然是品牌项目事实与决策的唯一来源。商业研究报告是上游证据，必须经过品牌项目确认后，才将适用事实纳入 BRAND.md。

## 2. 品牌模式不是互斥行业分类

建议以“品牌经营模式”识别，而不是只按行业识别：

### Professional Specialist Brand
适合专业工具、工业配件、HVAC、维修设备。
重点：规格、适配、可靠性、技术支持、专业用户任务。

### DTC Consumer Brand
适合 RV、Marine、户外生活、家居和消费产品。
重点：用户、场景、体验、信任、套装、复购和退换政策。

### Aftermarket & Replacement Brand
适合设备替换件、维修耗材、兼容件和长尾型号。
重点：型号映射、兼容边界、库存、质量和售后。

### OEM / ODM Partner Brand
适合设计、制造、检验、定制和供应链服务。
重点：真实生产关系、开发流程、质量体系、交付能力和保密边界。

### Consumable & Replenishment Brand
适合滤芯、耗材、维护套装和周期替换产品。
重点：产品安全、批次一致性、替换周期、复购体验。

### Multi-brand Portfolio
适合一个经营主体管理多个行业或价格带品牌。
重点：母子品牌关系、共享能力、渠道区隔、知识产权和品牌资产归属。

同一个企业可以同时采用多种模式，例如 Professional Specialist + Aftermarket，或 DTC + Consumable。

## 3. 按交易方式适配品牌表达

### B2B 询盘型

优先回答：
- 你供应什么？
- 适合哪类采购商？
- 规格、MOQ、交期和定制能力是什么？
- 哪些认证、检测和质量资料可提供？
- 如何询价、索样和批量采购？

主要转化：完整询盘、样品申请、报价和经销合作。

### B2C 电商型

优先回答：
- 适合谁、解决什么任务？
- 如何选择型号？
- 有什么限制和不适用场景？
- 交付、退换、质保如何执行？
- 为什么值得购买？

主要转化：购买、加购、订阅和复购。

### DTC 品牌型

优先回答：
- 用户身份和生活场景
- 产品体验和设计差异
- 品牌承诺及其证据
- 社群、内容和复购关系

主要转化：直接成交和长期客户关系。

### Hybrid 混合型

明确渠道职责：
- Amazon：标准 SKU、平台搜索和快速成交。
- 独立站：品牌信任、技术内容、型号数据库、套装和售后。
- B2B：批量报价、经销商和企业采购。
- 内容渠道：需求教育、使用演示和售前支持。

渠道价格、促销、库存和客户归属必须协调，避免相互冲突。

## 4. 品牌档案建议增加的上游关联字段

不直接破坏当前 BRAND.md schema。先在机会项目中维护，待验证后再决定是否将部分字段纳入 BRAND.md：
- opportunity_id
- industry_id
- leader_reference_ids
- product_line_ids
- supply_chain_evidence_ids
- channel_model
- approved_entry_scope
- excluded_markets_or_products
- evidence_review_date

建议使用独立的 OPPORTUNITY-BRIEF.md 作为品牌项目的上游交接文件，记录机会来源、证据、边界和批准的进入范围。它不能取代 BRAND.md。

## 5. 品牌定位表达模板

定位句式：

> 面向 [具体客户]，提供 [明确品类/产品]，帮助其完成 [具体任务/结果]；凭借 [已证实的能力或差异]，区别于 [真实替代方案]。

所有括号内容都必须有证据或标记为候选，不得编造。

示例方向（仅为模板，不代表已验证企业）：
- HVAC：Professional HVAC Installation and Maintenance Accessories.
- Commercial Kitchen：Commercial Kitchen Equipment Replacement Parts.
- RV / Marine：RV and Marine Upgrade and Maintenance Products.
- Water Filtration：Residential and Commercial Filtration Components.
- Industrial Tooling：Application-Specific Crimping and Connector Tooling.

## 6. 品牌架构决策

每个项目需要明确：
- 一个主品牌还是多个品牌
- 母品牌与子品牌关系
- 产品系列是否使用描述性系列名
- OEM/ODM 与自有品牌是否分开
- Amazon 店铺与独立站品牌是否一致
- 价格带是否需要品牌隔离
- 不同市场是否需要不同品牌表达

不要为了显得像大公司而人为创建多个子品牌。只有在客户群、价格带、渠道、产品承诺或风险边界确实不同，且运营资源能够支撑时，才考虑多品牌架构。

## 7. 品牌证明与声明边界

禁止：
- 把合作工厂写成自有工厂。
- 把兼容写成原厂授权。
- 把供应商证书扩大到未覆盖型号。
- 把样品测试写成量产质量保证。
- 把行业趋势写成自身客户成果。
- 把市场研究假设写成已实现的产品能力。

所有公开主张应能追溯到 Claim ID、Decision ID 或经批准的事实。
