# Branding Skills

一组用于建立品牌基础、生成品牌表达和探索视觉方向的 AI Skills。

## 功能

| Skill | 功能 | 主要输出 |
|---|---|---|
| [`brand-foundation`](skills/brand-foundation/SKILL.md) | 整理品牌事实、证据、受众、定位和关键决策 | `BRAND.md` |
| [`brand-expression`](skills/brand-expression/SKILL.md) | 将品牌基础转成定位、核心信息、品牌声音和渠道文案 | `MESSAGING.md` |
| [`brand-visual-board`](skills/brand-visual-board/SKILL.md) | 将品牌基础和表达转成视觉方向与品牌板 | `output/brand-system.md`、`output/brand-board.html` |

## 工作流

```text
品牌资料
   ↓
brand-foundation
   ↓
BRAND.md
   ↓
brand-expression
   ↓
MESSAGING.md
   ↓
brand-visual-board
   ↓
Brand Board
```

`BRAND.md` 保存品牌事实与决策；表达和视觉文件由它派生。

## 快速开始

将需要的 Skill 复制到 Agent 的 Skill 目录。以 Codex 为例：

```bash
mkdir -p ~/.codex/skills
cp -R skills/brand-foundation ~/.codex/skills/
cp -R skills/brand-expression ~/.codex/skills/
cp -R skills/brand-visual-board ~/.codex/skills/
```

创建独立品牌项目：

```bash
python3 scripts/create_brand_project.py ../my-brand
```

依次调用：

```text
使用 $brand-foundation，读取当前品牌资料并生成 BRAND.md。

使用 $brand-expression，基于 BRAND.md 生成 MESSAGING.md。

使用 $brand-visual-board，基于 BRAND.md 和 MESSAGING.md 生成品牌视觉板。
```

## 运行虚构 Demo

Demo 只使用 `examples/fictional-b2b/` 中明确标记的虚构数据：

```bash
python3 scripts/run_demo.py --output /tmp/branding-skills-demo
```

运行成功后，输出目录包含一份虚构输入、`BRAND.md` 和 `MESSAGING.md`，可用于查看文件关系和状态字段。

## 验证

```bash
python3 scripts/verify_release.py .
python3 scripts/validate_skills.py .
python3 -m unittest discover -s tests -v
```

## 文档

- [架构](docs/ARCHITECTURE.md)
- [安全使用资料](docs/PRIVACY.md)
- [开源范围](OSS-SCOPE.md)
- [贡献指南](CONTRIBUTING.md)
- [安全政策](SECURITY.md)

## License

[MIT](LICENSE)
