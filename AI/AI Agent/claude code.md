# 安装
```
npm install -g @anthropic-ai/claude-code
```

C:\Users\54310\.claude 目录下创建配置文件 `seetings.json`，配置调用的模型
```json
{
	"env":{
		"ANTHROPIC_AUTH_TOKEN":"sk-jd3n5toNYZ2IuoiMN1ZGAjtDVt0SfeduJfm6oDr83rXbWTnH",
		"ANTHROPIC_BASE_URL":"https://api.moonshot.cn/anthropic",
		"ANTHROPIC_MODEL":"kimi-k2.5"
	}
}
```

# .claude目录结构
## 项目级
```
# 项目级 .claude/
your-project/
└── .claude/
    ├── CLAUDE.md
    ├── CLAUDE.local.md
    ├── settings.json
    ├── settings.local.json
    ├── rules/
    │   ├── code-style.md
    │   ├── api-rules.md
    │   └── testing.md
    ├── commands/
    │   ├── review.md
    │   ├── fix-issue.md
    │   └── deploy.md
    ├── skills/
    │   ├── auto-test.md
    │   └── code-gen.md
    ├── agents/
    │   ├── code-reviewer.md
    │   ├── test-specialist.md
    │   └── architect.md
    ├── hooks/
    │   ├── pre-write.js
    │   └── post-command.sh
    ├── templates/
    │   ├── react-component.md
    │   └── api-controller.md
    ├── plugins/
    ├── tools/
    ├── context/
    └── cache/
```

## 全局级
```
# 全局 ~/.claude/
~/.claude/
    ├── CLAUDE.md
    ├── settings.json
    ├── settings.local.json
    ├── history.jsonl
    ├── .mcp.json
    ├── projects/
    │   ├── project-1/
    │   └── project-2/
    ├── commands/
    ├── skills/
    ├── agents/
    ├── rules/
    ├── plugins/
    ├── file-history/
    ├── todos/
    ├── debug/
    └── cache/
```


# 使用
## 权限模式
通过 `Shift+Tab` 键来切换权限模式
- **默认权限模式（? for shortcuts）**
编辑文件时需确认权限

- **编辑模式 (accept edits on)**
整个会话期间自动接受所有后续的文件编辑，不再询问。如果执行 Shell 命令，会询再次询问是否允许操作。

想让 Claude Code 自动执行所有操作，在启动 时，加上
`--dangerously-skip-permissions` 

- **计划模式 (plan mode on)**
如果任务复杂，无法确定 Claude Code 是否符合你的要求，那么可以进入计划模式。计划模式下，它会先读取和分析你的代码，它不会修改文件。

规划任务完成后，Claude Code 会给出 4 个选择：
1. "Yes, clear context and auto-accept edits (shift+tab)"：它会清除没有必要的上下文，并自动接受所有后续的文件编辑，不再询问。如果选择这个选项，就会进入编辑模式。

2. "Yes,auto-accept edits"：和上面选项一样，但不会清除上下文。

3. "Yes, manually approve edits"：和上面选项一样，但每次都要手动批准文件编辑。

4. 最后，一个是输入框，如果你对它给出的建议不满意，可以在这里和它继续对话，让它重新规划任务。

如果你觉得 Claude Code 的规划不太合理了，按 "Esc" 键中断当前任务，然后规划任务。

如果有一些细节需要调整，直接在输入框中继续进行对话，告诉它你需要调整的细节。这样它就会根据你的反馈来调整规划任务的步骤，不需要中断当前任务。

## 命令
- `/resume` 历史会话列表，或启动时还原上次会话信息
```
# 还原上一次的会话信息
claude -c
```

- `/init`  初始通读项目，保存到CLAUDE.md文件，cc执行任务前先读取文件来了解项目。

CC 会在每次对话开始时读取它，其中包含 Bash 命令、代码风格和工作流规则。这为 CC 提供了持续的上下文，这些上下文是它仅从代码中无法推断出来的。

一个是全局的 `CLUADE.md` 文件，位于用户主目录下。这个文件对你所有的项目都会生效。另一个是项目级别的 `CLUADE.md` 文件，位于当前项目的根目录下。这个文件只对当前项目生效。

- `/rename` 给当前会话重新命名，重启CC后`/resume`可选择会话，也可进入历史会话，重新命名

- `/clear`清除当前会话，开启新会话，可以重新对当前会话命名，否则共用上次会话名称

- `/rewind` 回滚版本

- `/compact` 压缩上下文

- `/ide`  先安装claude code 插件，再执行命令

- `/cost` 查看token消耗