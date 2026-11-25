# Branding Skills

一组 AI Skills：主持一场不跑偏的客户品牌访谈，把结论沉淀成一套档案，让之后任何 AI 读档案就能了解这家企业，不用再采访一遍。

## 功能

| Skill | 做什么 | 主要输出 |
|---|---|---|
| [`brand-journey`](skills/brand-journey/SKILL.md) | 总入口。分阶段主持访谈，记录进度，随时续接，按客户类型自动加问 | `PROGRESS.md`、客户确认报告 |
| [`brand-foundation`](skills/brand-foundation/SKILL.md) | 整理品牌事实、证据、受众、定位和关键决策；企业有多个品牌或名称时理清它们的关系；把客户的原话优化后交给客户确认 | `BRAND.md` |
| [`brand-expression`](skills/brand-expression/SKILL.md) | 把品牌基础转成定位表述、核心信息、品牌声音、渠道文案和网站页面文案；定一套各平台通用的标准说法，并比对各处现有的介绍 | `MESSAGING.md`、一致性体检报告 |
| [`brand-visual-board`](skills/brand-visual-board/SKILL.md) | 把品牌基础和表达转成视觉方向与品牌板 | `output/brand-board.html`、`output/DESIGN.md` |
| [`brand-handoff`](skills/brand-handoff/SKILL.md) | 把档案整理成给 AI 的速读文件和建站交接文件 | `COMPANY.md`、`SITE-BRIEF.md`、`AGENTS.md` |

`brand-foundation`、`brand-expression`、`brand-visual-board`、`brand-handoff` 可以各自单独使用。`brand-journey` 需要和 `brand-foundation` 一起安装，因为提问、取证和记录的方法都在后者里。`BRAND.md` 是唯一的事实源，其余文件都由它派生。

## 工作流

```text
客户资料（官网、画册、目录、聊天记录、问卷）
        │
        ▼
brand-journey ──────────── 进度文件 PROGRESS.md
  │  每个阶段调用 brand-foundation 的方法，写入 BRAND.md
  │  最后出客户确认报告，然后依次派生：
  ├─▶ brand-expression ───▶ MESSAGING.md
  ├─▶ brand-visual-board ─▶ 品牌板、output/DESIGN.md（可选）
  └─▶ brand-handoff ──────▶ COMPANY.md；要建站时再出 SITE-BRIEF.md
```

## 必选与可选

**必选主线**每个客户都走，产出完整的定位和品牌表述：

立项与预读 → 业务现状 → 客户与成交场景 → 竞争与替代 → 诊断与定位（关卡）→ 证明与信任 → 身份、声音与品牌表述 → 汇总确认（关卡）

**可选模块**按客户需要加开，可以事后再加，不用重走主线：

| 模块 | 内容 | 什么时候选 |
|---|---|---|
| 落地 `execution` | 产品与价格、渠道与推广 | 客户不只要定位，还要落到怎么卖 |
| 建站 `website` | 网站目标与约束 | 这次要建站或改版 |

访谈里有几条不变的规则：

- 每一轮都带进度行，随时说得出在第几阶段、还差什么。
- 客户说到别的事，先记进稍后处理清单，再回到当前问题。
- 客户的原话不直接当定稿：AI 先指出哪里弱，再给最多三个只用已有事实的优化稿，和原话并排，由客户确认。
- 关卡可以暂缓，不能跳过。操作者不能替客户批准。
- 事实、假设、候选和已批准的决定始终分开标注，不编造数字、案例或评价。

客户类型由细分包自动补充：外贸 B2B、国内 B2B、DTC 电商。哪一类都不像时只走通用主线。

### 多个品牌与统一说法

同一家企业在官网、平台店铺、画册和销售的口头介绍里常常各说各的，名字多的企业更容易乱。这部分不增加访谈阶段，在原有的阶段里顺带完成：

- **多个品牌或名称**：访谈时把企业对外用着的名称列成清单。不止一个时，AI 按通行的四种关系（单一主品牌、主品牌带子品牌、背书品牌、各自独立）给出最多三个候选和各自的代价，由客户选。默认建议只用一个主品牌。只有一个名称的企业一句话带过。
- **标准说法**：在 `MESSAGING.md` 里固定名称的写法、品类的叫法、可以公开的数字，以及一句话、短介绍、标准介绍三档。各平台只换长短和语气，不换说法。平台的字数上限经常变，不写死，用的时候再查。
- **一致性体检**：把各处现有的介绍交给 AI，它并排比对，列出名称、数字、品类说法对不上的地方，以及各处该换成哪一档。数字对不上时，AI 不猜哪个对，交给客户确认。它只读，不登录也不修改任何平台。

单独做一次体检，可以这样说：

```text
使用 $brand-expression 把官网、店铺和画册上的公司介绍对一下，列出不一致的地方。
```

## 快速开始

### Claude Code

把本仓库装成插件：

```text
/plugin install branding-skills --marketplace wo9230/branding-skills
```

较早的版本分两步：

```text
/plugin marketplace add wo9230/branding-skills
/plugin install branding-skills@branding-skills
```

也可以不装插件，直接把需要的 Skill 复制到 `~/.claude/skills/`。

### Codex

把本仓库装成插件。Codex 读的是和 Claude Code 同一份插件清单：

```bash
codex plugin marketplace add wo9230/branding-skills
codex plugin add branding-skills@branding-skills
```

也可以不装插件，直接复制 Skill：

```bash
mkdir -p ~/.codex/skills
cp -R skills/brand-journey skills/brand-foundation skills/brand-expression skills/brand-visual-board skills/brand-handoff ~/.codex/skills/
```

两种装法都在 Codex CLI 0.166.0 上验证过。

### 建一个客户项目

客户资料不放在本仓库里。每个客户建一个独立目录：

```bash
python3 scripts/create_brand_project.py ../my-client
```

已经知道客户类型和要做的模块时，可以一起带上。多个模块用逗号分隔：

```bash
python3 scripts/create_brand_project.py ../my-client --segment export-b2b --modules execution,website
```

`--segment` 可取 `export-b2b`、`domestic-b2b`、`dtc-ecommerce`、`generic`；`--modules` 可取 `execution`、`website`。脚本会放好进度文件、指路文件，以及一份按客户类型和模块拼好的客户问卷（`intake/CLIENT-QUESTIONNAIRE.md`），可以直接发给客户预填。

### 开始访谈

在客户项目目录里对 AI 说：

```text
使用 $brand-journey 给这家客户开始建档。这次要定位，也要建站。
```

中断之后再回来，说一句"继续"即可，它会从 `PROGRESS.md` 记录的下一问接着问。只想整理现有材料、不走整套访谈时，直接用 `$brand-foundation`。

`$brand-journey` 这种写法指的是技能名。在 Codex 里输入 `$` 可以从列表里选技能；在 Claude Code 里直接说出技能名即可。

### Claude Code 和 Codex 共用一套

两个工具用的是同一套文件，不需要各维护一份：

- **技能**：两边装的都是本仓库的 `skills/` 目录。
- **客户项目里的规则**：只有一份 `AGENTS.md`。Codex 自动读它。Claude Code 从 v2.1.277 起，在没有别的文件挡住时也自动读它。
- **什么会挡住**：客户项目目录或任何一级上级目录里有 `CLAUDE.md`、`.claude/CLAUDE.md` 或 `CLAUDE.local.md`。有其中一份，Claude Code 就只读那些文件，不读 `AGENTS.md`。主目录下的 `~/.claude/CLAUDE.md` 不算。
- **被挡住时怎么办**：在客户项目根目录、和 `AGENTS.md` 同一个目录里，放一份 `CLAUDE.md`，里面写一行 `@AGENTS.md`。这个目录里已经有 `CLAUDE.md` 时，直接加这一行。不要把这一行加到上级目录的文件里：`@` 后面的路径从那个文件所在的目录算起，读不到客户项目里的这一份。更早版本的 Claude Code 也用这个办法。

## 客户项目里的文件

```text
客户项目/
  AGENTS.md       指路文件：告诉任何 AI 先读 COMPANY.md
  PROGRESS.md     访谈进度：已选模块、阶段状态、下一问、稍后处理清单
  BRAND.md        事实与决策，唯一事实源
  MESSAGING.md    对外表达（派生）
  COMPANY.md      一两页 AI 速读（派生）
  SITE-BRIEF.md   建站交接（派生，做了建站模块才有）
  intake/         客户问卷和工作簿
  sources/        已授权、已脱敏的资料
  reports/        给客户确认的报告、一致性体检报告、日期快照
  output/         品牌板、DESIGN.md
```

企业情况变了，不用重新访谈：更新 `BRAND.md` 并升版本号，然后检查哪些派生文件过期了，重新生成即可。

```bash
python3 scripts/check_brand_project.py ../my-client
```

这个脚本只读不写。它会报告过期的派生文件、引用了不存在编号的地方、被跳过的必选阶段，以及没有写审批人或日期的批准。它还会提醒两件事：各文件里的品牌名不一致；派生文件里用了已经停用的名称写法。

## 与其他技能库的衔接

- 网站代码仓库里用了别的营销或建站技能库时，把 `COMPANY.md` 当作它们的企业上下文来源，把 `SITE-BRIEF.md` 和 `output/DESIGN.md` 交给建站的 AI。`skills/brand-handoff/assets/AGENTS-SNIPPET.md` 是一段可以贴进网站仓库 `AGENTS.md` 或 `CLAUDE.md` 的说明。
- 要检查一段文案是否符合品牌声音，可以把 `MESSAGING.md` 和 `COMPANY.md` 的"不能说的话""声音"两节交给已有的品牌审查技能，作为审查依据。
- 本项目不做投放、SEO 运营、邮件发送和网站代码生成，只提供它们能读的上下文。

## 运行虚构 Demo

`examples/fictional-b2b/` 是一套完全虚构的完整档案，走完了全部阶段和两个模块。

```bash
python3 scripts/run_demo.py --output /tmp/branding-skills-demo
```

运行后输出目录里有全部文件，并已通过项目自检。各文件的说明见 [examples/README.md](examples/README.md)。

## 验证

```bash
python3 scripts/verify_release.py .
python3 scripts/validate_skills.py .
python3 -m unittest discover -s tests -v
python3 scripts/check_brand_project.py examples/fictional-b2b
```

`evals/` 里是用虚构材料写的行为场景，用来检查一个没有任何背景的 AI 只凭 Skill 文件能不能做对。它们不进 CI，运行方法见 [evals/README.md](evals/README.md)。

## 文档

- [架构](docs/ARCHITECTURE.md)
- [安全使用资料](docs/PRIVACY.md)
- [开源范围](OSS-SCOPE.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)
- [安全政策](SECURITY.md)

## 致谢

本项目的方法借鉴了下列公开的思路和项目。只借鉴做法，没有复制其中的文字。

方法来源：

- 理查德·鲁梅尔特的"战略内核"：诊断、指导方针、连贯行动。
- April Dunford 的定位五要素。
- "待办任务"（Jobs to Be Done）与切换访谈。
- David Aaker 与 Erich Joachimsthaler 的"品牌关系谱"：单一主品牌、子品牌、背书品牌、独立品牌四种关系。

参考过的开源项目：

- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)：用一份共享的上下文文件让多个技能了解同一家企业。
- [wondelai/skills](https://github.com/wondelai/skills)：带进度文件、可续接、有关卡的分阶段流程。
- [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills)：直接、间接、维持现状三层竞争。
- [cofoundy/brand-skills](https://github.com/cofoundy/brand-skills)：把品牌产物组织成一套带清单的文件包。
- [afadtc/afa-dtc-skills](https://github.com/afadtc/afa-dtc-skills)：数据不足时照实留白。
- [noique/cross-border-ecommerce-skills](https://github.com/noique/cross-border-ecommerce-skills)：按业务类型路由。
- [google-labs-code/design.md](https://github.com/google-labs-code/design.md)：给编码代理读的 `DESIGN.md` 开放格式。
- [arnabbagxd/Brand-building-skills](https://github.com/arnabbagxd/Brand-building-skills)：发给客户预填的问卷。

## License

[MIT](LICENSE)
