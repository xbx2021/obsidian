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
有两种类型的命令。**内置命令**是 Claude Code 自带的，用于控制会话和工具，你无法修改。 **自定义命令**是你创建的任务型 Skill，用于执行特定的工作流程，完全由你掌控。
![](assets/10%2010｜令行禁止：任务型%20Skills%20（斜杠命令Command）实战/file-20260424113157286.png)
任务型 Skill 可以放在两个目录下：
```markdown
.claude/skills/<name>/SKILL.md      # 推荐：Skills 目录（完整能力）
.claude/commands/<name>.md           # 兼容：Commands 目录（简单命令）
```
![](assets/10%2010｜令行禁止：任务型%20Skills%20（斜杠命令Command）实战/file-20260424113241196.png)
任务型 Skill 作用域如下：
```
项目级：  .claude/skills/   或 .claude/commands/       → 随项目 git 分发
用户级：  ~/.claude/skills/  或 ~/.claude/commands/      → 跨项目个人使用
```

# 通过 ARGUMENTS 给 Skill 传参

当你通过  /skill-name args  调用 Skill 时，args  会通过  $ARGUMENTS  注入到 Skill 内容中。

举例来说，当运行  /fix-issue 123  时，Claude 收到的内容是“Fix GitHub issue 123 following our coding standards…”。
```markdown
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```
注意，传参并不仅仅限于任务型 Skill，但是，需要明确传参的场景，对于任务型 Skill 自然是显得更加常见。

## Skill 支持两种参数传递方式。
### **单参数**——$ARGUMENTS  接收所有参数。
```markdown
---
description: Quick git commit
argument-hint: [commit message]
disable-model-invocation: true
---

Create a git commit with message: $ARGUMENTS
```

### **多参数**—— $1，$2 接收位置参数：
```markdown
---
description: Create a pull request
argument-hint: [title] [description]
disable-model-invocation: true
---

Title: $1
Description: $2
```

用法示例如下。
```markdown
/commit fix login bug           # $ARGUMENTS = "fix login bug"
/pr-create "Add auth" "JWT"     # $1 = "Add auth", $2 = "JWT"
```

可以用 $ARGUMENTS[N]   或简写  $N  访问特定位置的参数：
```markdown
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```
例如，/migrate-component SearchBar React Vue 中，$0 被替换为 SearchBar,  $1 为 React, $2 为 Vue。

Claude Code 是非常灵活的，如果 Skill 中根本就没有定义 $ARGUMENTS，而你在调用 Skill 的时候又偏偏传递了参数进去。那也不怕，Claude Code 会自动在内容末尾追加  ARGUMENTS: <用户输入>，确保参数不会丢失。

此外，还可以通过 ${CLAUDE_SESSION_ID} 变量传入当前会话 ID，可用于把日志关联到当前会话。

# ! `command` 动态上下文注入

Skills 中那么多文字和信息，其实归根结底还是 Prompt，需要 Claude Code（工具）发给 Claude 或者 GLM/Qwen 等模型来处理。而模型启动时并不知道和当前技能相关的上下文，这一功能刚好可以解决该问题。

