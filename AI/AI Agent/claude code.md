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
- 默认权限模式（? for shortcuts）
- 编辑模式 (accept edits on)
- 计划模式 (plan mode on)
