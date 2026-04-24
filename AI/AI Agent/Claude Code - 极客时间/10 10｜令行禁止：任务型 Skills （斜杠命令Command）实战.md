任务型 Skill 的价值：**把重复的对话模式，变成可复用的快捷方式。**
![](assets/10%2010｜令行禁止：任务型%20Skills%20（斜杠命令Command）实战/file-20260424112422766.png)
# Skills vs Commands

早期，斜杠命令 /Comands 和 Skills 是两个独立组件。但在新版 Claude Code 中，Commands 已合并到 Skills，成为 Skills 的子集。

因此，在 .claude/commands/review.md  和  .claude/skills/review/SKILL.md  两个不同目录的文件，都会创建  /review。**Skills 目录的额外优势是支持辅助文件目录（模板、示例、脚本等）**。**如果同名 Skill 和 Command 共存，Skill 优先**。

下面的对比主要是帮助你理解历史演进和两种目录结构的差异。
![](assets/10%2010｜令行禁止：任务型%20Skills%20（斜杠命令Command）实战/file-20260424112712993.png)
# 任务型 Skill 的核心机制

简单来说，任务型 Skill 就是设了 disable-model-invocation: true 的 Skill。
```markdown
# 参考型——Claude 自动选择是否使用
name: api-conventions
description: API design patterns for this codebase. Use when writing or reviewing API endpoints.

# 任务型——必须用户手动触发
name: deploy
description: Deploy the application to production
disable-model-invocation: true
```
![](assets/10%2010｜令行禁止：任务型%20Skills%20（斜杠命令Command）实战/file-20260424112933306.png)
![](assets/10%2010｜令行禁止：任务型%20Skills%20（斜杠命令Command）实战/file-20260424113024977.png)


