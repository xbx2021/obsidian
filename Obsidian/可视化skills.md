https://github.com/axtonliu/axton-obsidian-visual-skills

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
