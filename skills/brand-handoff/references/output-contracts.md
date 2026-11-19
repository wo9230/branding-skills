# 交接文件的输出协议

本技能产出三种文件，都放在客户项目根目录，都是 `BRAND.md` 的派生物：

| 文件 | 给谁用 | 什么时候出 | 格式 |
|---|---|---|---|
| `COMPANY.md` | 任何需要快速了解这家企业的 AI | 每个客户都出 | [company-context.md](company-context.md) |
| `SITE-BRIEF.md` | 建站的人或建站 AI | 只在做了建站模块时 | [site-brief-method.md](site-brief-method.md) |
| `AGENTS.md` | 进入这个文件夹的任何 AI | 项目里没有时补上 | 本页 |

## 写入规则

- 生成每份文件前各问一次。用户只要求看内容时，在对话里给出，不写文件。
- 只写在用户指定的客户项目目录里；路径不明确就留在对话里，不猜目录。
- 不写回已安装的技能目录。不修改 `BRAND.md`、`MESSAGING.md` 或 `PROGRESS.md`：发现缺口或矛盾时，报告给用户并指回 `$brand-foundation`、`$brand-expression` 或 `$brand-journey`。
- 写完后重读文件头和状态标签，确认没有把候选写成已批准，没有引用不存在的编号。

## `COMPANY.md`

文件头：

```yaml
---
schema: company-context/v1
brand_id: ""
brand_name: ""
foundation_file: BRAND.md
foundation_version: ""
messaging_version: ""
generated: YYYY-MM-DD
allowed_use: internal
---
```

正文十二个小节，写法、顺序和规则见 [company-context.md](company-context.md)。模板见 [../assets/COMPANY-TEMPLATE.md](../assets/COMPANY-TEMPLATE.md)。

## `SITE-BRIEF.md`

文件头：

```yaml
---
schema: site-brief/v1
brand_id: ""
brand_name: ""
brief_status: concept
foundation_file: BRAND.md
foundation_version: ""
messaging_version: ""
design_file: ""
generated: YYYY-MM-DD
language: ""
primary_conversion: ""
platform: ""
---
```

- `brief_status`：`concept | working | approved`，判定条件见 [site-brief-method.md](site-brief-method.md)。
- `foundation_version`、`messaging_version`：生成时读到的两份文件的 `version`；没有 `MESSAGING.md` 时后者留空。
- `design_file`：项目里有 `output/DESIGN.md` 时填这个路径，没有就留空。
- `language`：网站的主语言，例如 `zh-CN`、`en`。
- `primary_conversion`：主转化动作，用一个短语，例如"提交询盘表单"。
- `platform`：客户已经定下的建站平台；没定就留空，不替客户选。

正文九个小节，写法见 [site-brief-method.md](site-brief-method.md)。模板见 [../assets/SITE-BRIEF-TEMPLATE.md](../assets/SITE-BRIEF-TEMPLATE.md)。

## `AGENTS.md`

客户项目根目录的指路文件。内容固定且很短，照 [../assets/AGENTS-TEMPLATE.md](../assets/AGENTS-TEMPLATE.md) 写，只有四条规则：

1. 开始任何任务前先读 `COMPANY.md`。
2. 事实以 `BRAND.md` 为准；两者不一致或 `COMPANY.md` 过期时，以 `BRAND.md` 为准并提醒重新生成。
3. 不把候选、假设写成事实；不公开没有放行的说法。
4. 网站相关的任务再读 `SITE-BRIEF.md` 和 `output/DESIGN.md`（存在时）。

项目里已经有 `AGENTS.md` 时不覆盖；缺哪条规则，告诉用户并问是否补上。

网站代码通常在另一个仓库。[../assets/AGENTS-SNIPPET.md](../assets/AGENTS-SNIPPET.md) 是一段可以粘贴进那个仓库的 `AGENTS.md` 或 `CLAUDE.md` 的文字，告诉那里的 AI 去哪里找这几份文件。

## 版本与过期

每份派生文件都在文件头记录生成时依据的版本。`BRAND.md` 的 `version` 更高时，派生文件即过期。`COMPANY.md` 和 `SITE-BRIEF.md` 还记录了 `messaging_version`：`MESSAGING.md` 的 `version` 比它高时，这两份文件同样过期。`scripts/check_brand_project.py <客户项目目录>` 会列出过期的文件，以及引用了不存在编号的地方。

## 与其他技能库的衔接

- `COMPANY.md` 的十二个小节覆盖了常见"产品营销上下文"文件的内容。网站仓库用了别的营销技能库时，可以把 `COMPANY.md` 当作它们的上下文来源。
- 要检查一段文案是否符合品牌声音，可以把 `MESSAGING.md` 的声音部分和 `COMPANY.md` 第 8、9 节交给已有的品牌审查技能，当作审查依据。
- 本技能不做格式转换。别的工具需要别的格式时，由那边读取这几份文件。
