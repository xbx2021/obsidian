https://github.com/axtonliu/axton-obsidian-visual-skills/blob/main/README_CN.md
让 Claude Code 在 Obsidian 里生成 Canvas / Excalidraw / Mermaid 的可视化三件套。

### 安装步骤（Windows）

1. 先装好：Obsidian + Excalidraw 插件 + Claude Code CLI
2. 下载技能包：
```bash
git clone https://github.com/axtonliu/axton-obsidian-visual-skills.git
```
3. 复制到 Claude 技能目录：
```bash 
# 复制3个核心技能
cp -r axton-obsidian-visual-skills/excalidraw-diagram ~/.claude/skills/
cp -r axton-obsidian-visual-skills/mermaid-visualizer ~/.claude/skills/
cp -r axton-obsidian-visual-skills/obsidian-canvas-creator ~/.claude/skills/
```
4. 重启 Claude Code，触发关键词：`Canvas`、`mind map`、`Excalidraw`、`Mermaid`、`visual diagram`

### 使用方法
```
# Excalidraw
"创建一个展示 CI/CD 流程的 Excalidraw 流程图"
"画一个关于机器学习概念的思维导图"
"用 Excalidraw 画一个商业模式关系图"

# Mermaid
"用 Mermaid 图表可视化这个流程"
"为 API 认证流程创建时序图"
"把这个工作流程转成 Mermaid 图表"

# Canvas
"把这篇文章转换成 Obsidian Canvas"
"创建一个项目规划的思维导图 Canvas"
"把这篇文章整理成 Canvas 思维导图"
```
