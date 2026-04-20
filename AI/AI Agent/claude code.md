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

如果同时维护多个项目，可以把稳定的个人基线放在 `~/.claude/`，各项目的差异放在项目级 `.claude/`。避免不同项目之间互相污染。

## 配置示例
### CLAUDE.md
```markdown
# Project Instructions
- Use TypeScript strict mode
- Follow Airbnb code style
- All APIs return { data, error } shape
- Use Zod for validation
- Write unit tests for all functions
```

### settings.json
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-3-5-sonnet-20240620",
  "permissions": {
    "allow": [
      "bash(npm run*)",
      "bash(git*)",
      "read",
      "write",
      "edit",
      "list"
    ],
    "deny": [
      "bash(rm -rf*)",
      "bash(curl*)",
      "read(./.env*)",
      "write(./node_modules/**)"
    ]
  },
  "maxTokens": 8000,
  "temperature": 0.1
}
```

### rules/api-rules.md
```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/controllers/**/*.ts"
---
# API Design Rules
- Use RESTful conventions
- All responses: { data, error, meta? }
- Validate inputs with Zod
- Add JSDoc for all endpoints
```

### commands/review.md
```markdown
---
name: review
description: Code review for current file
---
Review this code for:
- Bugs & logic errors
- Performance issues
- Style violations
- Security risks
- Test coverage gaps

Provide specific fixes.
```

### ## agents/code-reviewer.md
```markdown
---
name: code-reviewer
description: Senior code reviewer
model: claude-3-5-sonnet-20240620
tools: [read, grep, glob, edit]
---
You are an expert code reviewer.
Focus only on:
- Correctness & reliability
- Maintainability & readability
- Performance & efficiency
- Security vulnerabilities
```


## CLAUDE.md
### **该放什么**
- 怎么 build、怎么 test、怎么跑（最核心的）
- 关键目录结构和模块边界
- 代码风格和命名约束
- 不明显的环境坑
- 绝对不能干的事（NEVER 列表）
- 压缩时必须保留的信息（Compact Instructions）

### **不该放什么**
- 大段背景介绍
- 完整 API 文档
- "写高质量代码"这种空泛原则
- Claude 读一下仓库就能推断出来的信息
- 低频任务的详细知识（这些放到 Skills 里）

### **实用模板**
```
# Project Contract  
  
## Build And Test  
- Install: `pnpm install`  
- Dev: `pnpm dev`  
- Test: `pnpm test`  
- Lint: `pnpm lint`  
  
## Architecture Boundaries  
- HTTP handlers live in `src/http/handlers/`  
- Domain logic lives in `src/domain/`  
- Do not put persistence logic in handlers  
  
## Safety Rails  
  
### NEVER  
- Modify `.env`, lockfiles, or CI secrets without approval  
- Commit without running tests  
  
### ALWAYS  
- Show diff before committing  
- Update CHANGELOG for user-facing changes  
  
## Compact Instructions  
Preserve:  
1. Architecture decisions (NEVER summarize)  
2. Modified files and key changes  
3. Current verification status  
4. Open risks and TODOs
```

### **CLAUDE.md自我修正**
每次纠正 Claude 的错误后，直接告诉它
```
Update your CLAUDE.md so you don't make that mistake again
```

## Skills
### **渐进式披露**
Skill 的核心设计是"按需加载"——描述符常驻上下文（告诉 Claude 什么时候该用它），但完整内容只在真正需要的时候才拉进来。

这个设计背后的理念叫"渐进式披露"（progressive disclosure）：不是让模型一次性看到所有信息，而是先给索引和导航，再按需拉取细节。

### **好skill的特点**
- **描述要让模型知道"什么时候该用我"**，而不是"我是干什么的"。这两个差很多。
- **有完整的步骤、输入、输出和停止条件**。别写了个开头没有结尾。
- **正文只放导航和核心约束**，大资料拆到 supporting files 里。
- **有副作用的 Skill 要显式禁止自动调用**，不然 Claude 会自己决定要不要跑。

### **典型的 skill 类型**
**检查清单型**：发布前跑一遍，确保不漏项。比如 build 通过了没、版本号改了没、CHANGELOG 更新了没。

**工作流型**：标准化高风险操作。比如配置迁移，先备份、再 dry-run、确认后再执行、最后验证。内置回滚步骤。

**领域专家型**：封装决策框架。比如运行时出问题了，按固定路径收集日志、检查状态、匹配症状，不让 Claude 瞎猜。

### **实用策略**
高频使用的 Skill 保持自动调用，优化描述符；
低频的禁止自动调用，手动触发；
极低频的直接删掉，改成文档。

## Hooks
### **重要性**
Hooks 很容易被忽视，但它解决的问题非常关键：**有些事情不能靠 Claude 自己记得去做。** 比如：
- 每次编辑完 Rust 文件，自动跑一下编译检查
- 修改了受保护的配置文件，直接拦住不让动
- 任务完成后推送一个通知
这些事如果写在 CLAUDE.md 里，它经常当没看见。但如果做成 Hook，是在生命周期事件前后强制执行的，不依赖模型判断。

### **实用案例**
假设项目同时有 Rust 和 Lua 代码，可以按文件类型分别触发检查：
```json
{  
  "hooks": {  
    "PostToolUse": [  
      {  
        "matcher": "Edit",  
        "pattern": "*.rs",  
        "hooks": [{  
          "type": "command",  
          "command": "cargo check 2>&1 | head -30",  
          "statusMessage": "Checking Rust..."  
        }]  
      },  
      {  
        "matcher": "Edit",  
        "pattern": "*.lua",  
        "hooks": [{  
          "type": "command",  
          "command": "luajit -b $FILE /dev/null 2>&1 | head -10",  
          "statusMessage": "Checking Lua syntax..."  
        }]  
      }  
    ]  
  }  
}
```
Hook 的输出也会进入上下文。所以一定要加 `| head -30` 之类的截断，避免 Hook 输出反而污染了上下文。

## Subagents
### **说明**
Subagent 就是从主对话派出去的一个独立 Claude 实例。它有自己的上下文窗口，只能用你指定的工具，干完了汇报结果。核心价值不是"并行"，而是**隔离**。

扫代码库、跑测试、做审查这类会产生大量输出的事，交给 Subagent 做，主线程只拿摘要，不会被中间过程污染。

Claude Code 内置了三种 Subagent：
- **Explore**：只读扫库，跑 Haiku 模型省成本
- **Plan**：规划调研，不动文件
- **General-purpose**：通用型，什么都能干
### **关键配置**
不要给 Subagent 和主线程一样宽的权限，否则隔离就没有意义了。几个关键配置：
- **tools / disallowedTools**：限定能用什么工具
- **model**：探索任务用 Haiku/Sonnet，重要审查用 Opus
- **maxTurns**：防止跑飞
- **isolation: worktree**：需要动文件时隔离文件系统

### **什么时候不该用 Subagent**
子任务之间强依赖、频繁要共享中间状态的场景，用 Subagent 反而更麻烦。这种情况在主线程里顺序做就好。

# 命令

### `双击ESC`
回到上一条输入重新编辑，不用重新手打。Claude 走偏了，双击 ESC 修改后重发，比重新开会话省事

### `Ctrl+B` 
把长时间运行的命令移到后台，Claude 之后会自动查看结果，不阻塞主线程

### `/init`
初始化项目结构
通读项目，保存到CLAUDE.md文件，CC执行任务前先读取文件来了解项目，或添加自定义规则。

CC 会在每次对话开始时读取它，其中包含 Bash 命令、代码风格和工作流规则。这为 CC 提供了持续的上下文，这些上下文是它仅从代码中无法推断出来的。

一个是全局的 `CLUADE.md` 文件，位于用户主目录下。这个文件对你所有的项目都会生效。另一个是项目级别的 `CLUADE.md` 文件，位于当前项目的根目录下。这个文件只对当前项目生效。

###  `/rewind`
回滚版本

###  `/ide`  
先安装claude code 插件，再执行命令

###  `截图` 
将截图发给CC，执行任务

### `/review` 
评审改动的代码，或最佳文件路径，只评审单个文件

### `Shift+Tab`
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

## 会话管理

###  `!` 
进入 Shell 模式。在 Shell 模式下，可以直接输入 Bash 命令

 ###  `@` 
 选择文件，提供上下文

### `/resume` 
历史会话列表，或启动时还原上次会话信息
```
# 还原上一次的会话信息
claude -c
```

### `/rename` 
给当前会话重新命名，重启CC后`/resume`可选择会话，也可进入历史会话，重新命名

### 启动时直接追加命令
- `claude --continue` —— 恢复最近会话，隔天接着做
- `claude --resume` —— 打开选择器恢复历史会话
- `claude --continue --fork` —— 从已有会话分叉，同一起点不同方案
- `claude -p "prompt"` —— 非交互模式，接入 CI 或脚本

### `/insight`
让 Claude 分析当前会话，提炼出哪些内容值得沉淀到 CLAUDE.md。是迭代优化配置的好手段

## **能力与治理**
### `/mcp` 
管理 MCP 连接，检查 token 成本，断开闲置 server

### MCP 安装
```
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

###  `/hooks` 
在特定的事件发生时，自动执行一些操作。
可以在
`~/.claude/settings.json`、
`.claude/settings.json` 、
`.claude/settings.local.json` 文件中，手动添加 Hooks 的配置。
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

### `/model`
切换模型：Opus 深度推理，Sonnet 常规，Haiku 快速探索

### `/plugin` 
可以把 Agent Skills、子代理、MCP 和 Hooks 结合起来，打包成一个插件，让其他人安装，也可以安装其他人分享的插件，轻松扩展 Claude Code 的功能。
	官方文档： https://code.claude.com/docs/en/plugins
	官方插件市场： https://claude.com/plugins

### `/agents`  
自定义子代理，子代理拥有独立的上下文和记忆，可以专注于特定的任务或领域。
`~/.claude/agents` 创建子代理目录

### `/permissions`
查看或更新权限白名单

## **上下文管理**

###  `/cost` 
查看token消耗

### `/context`
查看 token 占用结构，排查 MCP 和文件读取占比

### `/clear`
清除当前会话，开启新会话，可以重新对当前会话命名，否则共用上次会话名称

###  `/compact` 
压缩但保留重点，配合 Compact Instructions 使用

###  `/memory` 
查看编辑 `CLAUDE.md` 文件，可选用户或项目级别。确认哪些 CLAUDE.md 真的被加载了

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

# Prompt Caching提示词缓存
Claude Code 的整个架构都是围绕 Prompt 缓存构建的。缓存命中率高，不只降低成本，还能获得更宽松的速率限制。

## 缓存是按前缀匹配的
Claude Code 的 Prompt 按这个顺序排列：
1. System Prompt → 静态，锁定
2. Tool Definitions → 静态，锁定
3. Chat History → 动态
4. 当前用户输入 → 最后

从头到尾，前面不变的部分会被缓存。所以**破坏前面的内容 = 破坏缓存**。

## **常见的缓存杀手**
- 在系统 Prompt 里放带时间戳的内容（每次都变）
- 非确定性地打乱工具定义顺序
- 会话中途增删工具
那动态信息怎么办？比如当前时间。答案是：别动系统 Prompt，放到用户消息里传进去。Claude Code 自己也是这么做的。

## **会话中途不要切换模型**
Prompt 缓存是模型唯一的。假如你已经和 Opus 对话了 100K tokens，想问个简单问题切到 Haiku——实际上比继续用 Opus 更贵，因为要为 Haiku 重建整个缓存。

确实需要切换的话，用 Subagent 交接：让 Opus 准备一条交接消息给另一个模型就行。

# 验证闭环
决定了你能不能真正信任 Claude 的输出。
"Claude 说完成了"其实没什么用。你得能知道它做没做对、出了问题能退回来、过程还能查，这才算数。
## 验证的三个层级
- **最低层**：命令退出码、lint、typecheck、单元测试
- **中间层**：集成测试、截图对比、contract test、smoke test
- **更高层**：生产日志验证、监控指标、人工审查清单

## 在 CLAUDE.md 和 Skill 里提前写好验收标准
```markdown
## Verification  
  
For backend changes:  
- Run `make test` and `make lint`  
- For API changes, update contract tests  
  
For UI changes:  
- Capture before/after screenshots  
  
Definition of done:  
- All tests pass  
- Lint passes  
- No TODO left behind unless explicitly tracked
```
假如一个任务你都说不清楚"什么叫做完"，那它大概率也不适合直接丢给 Claude 自动完成。


# Claude Code使用阶段
用 Claude Code 大概会经历三个阶段：

- **第一阶段：工具使用者。** 关注的是"这个功能怎么用" 。有帮助，但有限。

- **第二阶段：流程优化者。** 开始写 CLAUDE.md 和 Skills，关注"如何让协作更顺"。效率明显提升。

- **第三阶段：系统设计者。** 关注"如何让 Agent 在约束下自主运作"。这时候关注点悄悄变了——从功能层面升到了治理层面。

大部分人停在第一阶段，把 Claude Code 当一个更强的对话框用。
少部分人到了第二阶段，开始有意识地组织上下文和工作流。
真正到第三阶段的人，已经在思考怎么设计一套系统，让 Claude 在明确的边界内自己跑起来。