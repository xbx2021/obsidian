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

### `/init`
初始化项目结构
通读项目，保存到CLAUDE.md文件，CC执行任务前先读取文件来了解项目，或添加自定义规则。

CC 会在每次对话开始时读取它，其中包含 Bash 命令、代码风格和工作流规则。这为 CC 提供了持续的上下文，这些上下文是它仅从代码中无法推断出来的。

一个是全局的 `CLUADE.md` 文件，位于用户主目录下。这个文件对你所有的项目都会生效。另一个是项目级别的 `CLUADE.md` 文件，位于当前项目的根目录下。这个文件只对当前项目生效。

### `/rename` 
给当前会话重新命名，重启CC后`/resume`可选择会话，也可进入历史会话，重新命名

###  `/clear`
清除当前会话，开启新会话，可以重新对当前会话命名，否则共用上次会话名称

###  `/rewind`
回滚版本

###  `/compact` 
压缩上下文

###  `/ide`  
先安装claude code 插件，再执行命令

###  `/cost` 
查看token消耗

###  `/memory` 
查看编辑 `CLAUDE.md` 文件，可选用户或项目级别

###  `!` 
进入 Shell 模式。在 Shell 模式下，可以直接输入 Bash 命令

 ###  `@` 
 选择文件，提供上下文

###  `截图` 
将截图发给CC，执行任务

### `安装 MCP` 
```
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

###  `/hooks` 
在特定的事件发生时，自动执行一些操作。
也可以直接在 `~/.claude/settings.json`、`.claude/settings.json` 或者 `.claude/settings.local.json` 文件中，手动添加 Hooks 的配置。
```json
{  
  "hooks": {  
    "Notification": [  
      {  
        "matcher": "*",  
        "hooks": [  
          {  
            "type": "command",  
            "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""  
          }  
        ]  
      }  
    ]  
}  
}
```

官方参考文档： https://code.claude.com/docs/en/hooks-guide

### `/skill` 
给大模型添加一些特定的技能，让大模型能够更好地完成任务。可以创建用户级别的 Agent Skills，也可以创建项目级别的 Agent Skills。
`~/.claude/skills`  用户级别
`.claude/skills` 项目级别

### `/agents`  
自定义子代理，子代理拥有独立的上下文和记忆，可以专注于特定的任务或领域。
`~/.claude/agents` 创建子代理目录

### `/plugin` 
可以把 Agent Skills、子代理、MCP 和 Hooks 结合起来，打包成一个插件，让其他人安装，也可以安装其他人分享的插件，轻松扩展 Claude Code 的功能。
	官方文档： https://code.claude.com/docs/en/plugins
	官方插件市场： https://claude.com/plugins

### `/review` 
评审改动的代码，或最佳文件路径，只评审单个文件

### `/context`
查看当前上下文使用信息


# 运行模式
## 概览
核心是一个循环运转的代理系统：
![427](assets/Claude%20Code/file-20260420094116189.png)
这个循环会一直转，直到任务完成。每一轮它都在做三件事：看当前有什么信息、决定下一步做什么、检查做得对不对。

## 分层级执行
最直观的理解方式，是把 Claude Code 拆成六层来看。每一层解决一个不同的问题：

- **第一层：CLAUDE.md / rules / memory —— 长期记忆**

告诉 Claude "你是谁、这个项目是什么、有哪些规矩"。每次开会话都会加载，相当于它的基础认知。

- **第二层：Tools / MCP —— 动作能力**

告诉 Claude "你能做什么"。读文件、改代码、跑命令、调用外部 API，这些都是工具层提供的。

- **第三层：Skills —— 按需加载的方法论**

告诉 Claude "遇到这类事该怎么做"。不是每次都加载，只在需要的时候才拉进来，像一个个方法包。

- **第四层：Hooks —— 强制执行的规则**

不依赖 Claude 自己判断，而是在特定时机强制执行某些操作。比如每次编辑完自动跑格式化，改了受保护文件直接拦住。

- **第五层：Subagents —— 隔离的工作者**

派一个独立的 Claude 去干一件具体的事，干完汇报结果。核心价值是隔离——不让中间过程污染主线程。

- **第六层：Verifiers —— 验证闭环**

让输出可验证、可回滚、可审计。没有这一层，Claude 只能"觉得自己完成了"，你没法确认它真的做对了。

这六层的关键在于：只强化其中一层，系统就会失衡。

CLAUDE.md 写太长，上下文先把自己污染了；工具堆太多，它选择困难了；Subagent 开得到处都是，状态就漂移了；验证这步跳过了，出了问题根本不知道哪里挂的。

## 上下文占用概况
- 系统指令：约 2K
- 所有启用的 Skill 描述：约 1-5K
- MCP Server 工具定义：约 10-20K（这是最大的隐形杀手）
- LSP 状态：约 2-5K
- CLAUDE.md 和 Memory：约 3-7K

## 最有效的策略是分层管理：
- **始终常驻**：CLAUDE.md 里放项目契约、构建命令、禁止事项
- **按路径加载**：`.claude/rules/` 里放语言、目录、文件类型相关的规则
- **按需加载**：Skills 里放工作流和领域知识
- **隔离加载**：Subagents 负责大量探索和并行研究
- **不进上下文**：Hooks 负责确定性脚本、审计、阻断

说白了，偶尔用的东西就不要每次都加载进来。

