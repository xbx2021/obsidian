https://github.com/huangjia2019/claude-code-engineering
# 开篇
## 为什么 Claude Code 这么强？

因为它直接把 Agent 和工程治理写进了产品架构里——Sub-Agents、Skills、Hooks，这些从 Claude Code 的设计过程中创建出来的概念，已经超越了“编程工具”本身，形成了通用智能体设计模式的一部分。

使用 Claude Code 等 AI Coding 工具编码，其实你不再只是把自然语言翻译成代码， 而是在做设计，具体来说是做三件更高级的事情：
- **拆解问题**
- **分配任务组织**
- **多个智能体协作完成目标**

这已经不是“编程工具”的范畴了，而是一种**新的工作范式**。

## Sub-Agents（子代理）
核心思想是：一个复杂任务可以拆解给多个专职角色。
![](assets/Claude%20Code%20-%20极客时间/file-20260421100425912.png)

Claude Code 把它做成了开箱即用的工程能力——你只需要写一个配置文件，就能创建一个有明确职责、受限权限的子代理。
![](assets/Claude%20Code%20-%20极客时间/file-20260421100610983.png)

## Skills（技能）
核心思想是：AI 应该知道什么时候用什么能力。

**“语义触发”** 的设计，让 AI 从执行命令的工具，升级为理解意图的工作伙伴。

Skills 的**渐进式披露架构**——不是把所有知识一股脑灌给 AI，而是按需加载，用到什么加载什么。这解决了 LLM 上下文窗口的根本限制。

![](assets/Claude%20Code%20-%20极客时间/file-20260421100857296.png)
这两个概念之所以重要，是因为它们可以迁移。不管你用的是 Claude Code 还是其他 Agent 框架，分工协作和按需加载的思想都是通用的。学会了这套方法论，你就获得了一种**可复用的 AI 工程能力**。

## Claude Code解决的工程痛点
从工程协作中的真实卡点出发，反推需要哪些机制。围绕真实工程中 Agent 协作常见的痛点，解决以下问题。

- **Memory**：解决 Agent 每次对话都“从零开始”、不理解项目背景的问题，让 AI 真正记住你的代码结构、约束和上下文。

- **Sub-Agents**：解决单一 Agent 角色混乱、上下文污染、又写代码又做审查的问题，通过职责拆分实现关注点分离。

- **Skills**：解决 Prompt 不可复用、经验无法沉淀、团队能力难以传承的问题，把个人技巧变成可组合的工程资产。

- **Hooks**：解决 Agent 执行过程不可控、缺乏检查点、容易“越权操作”的问题，在关键节点引入自动校验和人工兜底。

- **Headless**：解决 Agent 只能在 IDE 里交互、无法进入自动化流程的问题，让 AI 能在 CI/CD 中无人值守地运行。

- **Agent SDK**：解决只会用对话的方式使用 Agent，难以嵌入现有系统和工作流的问题，用代码驱动 Agent，构建可编排的工程流程。


# Harness
## 什么是 Harness？

Anthropic 官方文档里是怎么说的：
	Claude Code serves as the agentic harness around Claude: it provides the tools, context management, and execution environment that turn a language model into a capable coding agent.

Claude Code 是一个**智能体编排框架**，包裹在 Claude 模型外面。它提供工具、上下文管理和执行环境，把一个语言模型变成一个有能力的编码 Agent。

这个定义里有三个关键词，**工具、上下文管理、执行环境**。模型本身只会生成文本。是 Harness 给了它读文件的能力、写代码的能力、搜索代码库的能力、在终端执行命令的能力。没有 Harness，Claude 就是一个只会说话的大脑——有智力，没有手脚。

![](assets/Claude%20Code%20-%20极客时间/file-20260421103236177.png)

## Harness 的内部结构拆解
![](assets/Claude%20Code%20-%20极客时间/file-20260421103434707.png)


**Agent = Model + Harness。**  图中最核心的位置是  Model——那个蓝色芯片图标，代表 Claude 的大语言模型。但模型本身只是一个推理引擎，它不能独立行动。

真正让它变成 Agent 的，是包裹在它周围的五个 Harness 组件。

- **Tools（工具）**，模型的手脚。Read、Write、Edit、Bash、Grep……这些工具赋予模型与文件系统、终端、网络交互的能力。没有工具，模型只能说，不能做。

-  **Context（上下文）**，模型的记忆加载器。CLAUDE.md、系统提示词、对话历史、工具定义——这些上下文在每一轮循环中被注入模型，决定了模型看到什么、知道什么。上下文管理的精妙之处是，它不仅是被动的信息传递，还包括主动的压缩和重注入策略。

- **Memory（记忆）**，模型的长期存储。跨会话的记忆持久化，让模型能“记住”你的偏好、项目规则和历史决策。CLAUDE.md 是显式记忆，自动记忆（~/.claude/memory/）是隐式记忆。没有 Memory，每次对话都从零开始。

- **Hooks（钩子）**，模型的神经反射。事件驱动的自动化机制，在工具执行前后触发自定义逻辑。比如每次保存文件前自动格式化，每次提交前自动运行 lint。Hooks 让 Harness 有了“条件反射”的能力——不需要模型主动决策，某些行为会自动发生。

- **Permissions（权限）**——模型的安全围栏。哪些工具可以自由使用，哪些需要人工审批，哪些完全禁止——权限系统是 Harness 的安全底线。它解决了一个核心矛盾：你希望 Agent 足够自主以提高效率，但又不希望它自主到失控。

注意图中的空间关系：**Model 在中心，五个组件围绕它排列，整体被一个名为 Harness 的边框包裹**。这不是随意的布局，它精确表达了一个架构事实：模型不直接接触外部世界，所有交互都通过 Harness 的组件中转。Harness 是模型和现实之间的唯一接口。

这五个组件也不是孤立的。Tools 的执行结果变成 Context 的一部分；Hooks 在 Tools 执行前后触发；Permissions 决定哪些 Tools 可以被调用；Memory 用于跨会话保留 Context 中的关键信息。它们构成了一个协同运转的系统，少了任何一个，Agent 的能力都会大打折扣。

## Harness 在整个系统中的层级位置

![](assets/Claude%20Code%20-%20极客时间/file-20260421104453020.png)

### **Agentic Loop——Harness 的心脏**

如果 Harness 是一台机器，Agentic Loop 就是它的发动机。整个 Claude Code 的运转，归根到底就是一个循环：
![](assets/Claude%20Code%20-%20极客时间/file-20260421104625524.png)
关键点在于**步骤 ② 和步骤 ④  之间的循环**。模型不是一次性给出最终答案的。它可能先读一个文件，看完结果后决定再搜索一下，搜索完又决定编辑某行代码，编辑完再运行测试——每一步都是一次循环。一个复杂任务可能跑几十轮循环。

循环什么时候结束？满足下面两个条件之一即可：
- **模型主动停止**——Claude 认为任务完成，生成纯文本回复，不再请求工具调用。API 返回  stop_reason: "end_turn"。

- **达到最大轮次**——Harness 设置了  --max-turns  限制，防止无限循环。
![](assets/Claude%20Code%20-%20极客时间/file-20260421105442145.png)

### **内置工具——Harness 的手脚**
Agentic Loop 是引擎，工具是车轮。Claude Code 内置了 20+ 个左右的工具，覆盖了软件工程的五个原子操作。
![637](assets/Claude%20Code%20-%20极客时间/file-20260421105536029.png)
工具设计背后有一个深刻的哲学，**少而精**。Claude Code 没有内置重构工具、测试工具、部署工具……它只给了最基础的原语。重构是 Read + Edit + Bash 的组合涌现；测试是 Bash + Read 的组合涌现；部署还是 Bash。

Harness 不需要为每种场景造一个工具，它只需要确保**基础工具的组合空间足够大**。

但 Bash 是个例外。Bash 工具是一个**图灵完备的逃逸舱**。通过它，Claude 可以执行任何 Shell 命令：安装依赖、运行测试、调用 API、操作数据库。这意味着 Claude Code 的能力上限，理论上等于操作系统的能力上限。

这也是为什么 Harness 需要**权限控制**的原因。

### **上下文管理——被忽视的关键能力**

Harness 最精巧的部分，其实是上下文管理。

Claude 的上下文窗口是有限的（200K tokens）。一个真实的编码任务——读 20 个文件、搜索 50 次、执行 30 条命令——产生的对话历史会迅速膨胀到几十万 tokens。如果不管理，要么爆掉上下文窗口，要么模型开始“遗忘”早期信息。

Claude Code 的解决方案是**自动压缩**。当对话历史接近上下文窗口的 92% 时，Harness 会触发一次压缩操作：
```markdown
对话历史（180K tokens）
    │
    ▼ 压缩触发
┌────────────────────────────┐
│ 保留：最近的消息（完整）      │
│ 压缩：早期消息 → 摘要        │
│ 重注入：CLAUDE.md 内容       │
│ 重注入：系统提示词            │
│ 重注入：工具定义              │
└────────────────────────────┘
    │
    ▼
压缩后对话历史（~80K tokens）
    │
    ▼ 继续工作
```

注意最后三行，**CLAUDE.md、系统提示词、工具定义**在每次压缩后都会重新注入。这意味着即使对话历史被截断了，模型仍然知道项目的规则、自己有哪些工具、应该遵循什么约定。

这就是为什么你在 CLAUDE.md 里写的东西那么“持久”——不是因为模型记住了它，而是 **Harness 在每次压缩后都重新塞给模型**。

![](assets/Claude%20Code%20-%20极客时间/file-20260421110159058.png)

### **Claude Agent SDK——可编程的 Harness**

虽然 Claude Code CLI 本身不开源，但 Anthropic 在 2025 年发布了  Claude Agent SDK——一套可编程的 Harness 接口。
```
# TypeScript 版本
npm install @anthropic-ai/claude-agent-sdk

# Python 版本
pip install claude-agent-sdk
```

Agent SDK 提供了与 Claude Code 完全相同的 Agentic Loop、内置工具、上下文管理、权限系统、Hooks、Sub-Agent 支持和 MCP 集成。区别在于，Claude Code 是面向终端用户的交互式产品，Agent SDK 是面向开发者的编程库。

用 Agent SDK，你可以构建自己的 Harness——一个定制化的 Agent 应用，嵌入到你自己的产品、工作流或 CI/CD 系统中。

```python
from claude_agent_sdk import AgentClient

client = AgentClient(api_key="...")

# 创建一个有工具能力的 Agent
result = client.run(
    prompt="审查这个 PR 的安全问题",
    tools=["Read", "Grep", "Glob", "Bash"],
    max_turns=20,
    allowed_tools={"Bash": ["npm test", "npm run lint"]}
)

print(result.text)
```

如果说 Claude Code 是一辆出厂配置的整车，Agent SDK 就是发动机总成——你可以把它装进任何车身里。
![](assets/Claude%20Code%20-%20极客时间/file-20260421110624111.png)
### **第三方 Harness 的崛起与冲突**
Claude Code 的成功证明了一件事：**模型 + Harness = 10× 生产力**。这个公式吸引了大量第三方工具来构建自己的 Harness。

**OpenCode**（前身 SST）是最成功的第三方 Harness。它用 Client-Server 架构解决了 Claude Code 的“单表面”局限——TUI、桌面 App、IDE 插件、Slack 机器人共享同一个后端。截至 2026 年 3 月，OpenCode 拿到了 119K GitHub stars，月活 65 万 +，超过了 Claude Code 本身的 star 数。

### **为什么 2026 年是 Harness 之年？**

2025 年的关键词是 Agent。2026 年的关键词是  Agent Harness。

为什么？因为行业已经意识到。模型本身正在商品化——Claude、GPT、Gemini、DeepSeek 的能力差距在缩小。但**同一个模型在不同 Harness 中的表现差距，远大于不同模型在同一个 Harness 中的差距**。

换句话说，**Harness 比模型更重要**。

几个数据点足以佐证：
- Claude Code 在 2025 年 11 月达到  10 亿美元年化收入——这是一个 Harness 产品的收入，不是模型本身的收入。
- Anthropic 在 2026 年 3 月收购了  Bun（JavaScript 运行时），明确表示要加强 Claude Code 的基础设施。收购一个运行时来加强一个 Harness——这说明 Anthropic 把 Harness 视为战略级资产。
- 开源社区出现了“Agent Harness“作为独立品类。GitHub 上以 “harness” 为关键词的新仓库数量在 2026 年 Q1 翻了三倍。

对于我们开发者来说，这意味着什么？**理解 Harness 比理解模型更重要**。

模型的能力由 Anthropic/OpenAI 决定，无法改变。
但 Harness 的配置——CLAUDE.md 怎么写、工具权限怎么设、Hooks 怎么接、MCP 怎么连——这些全在你手中，本质上都是在**调教 Harness**。

### **感受 Harness 的存在**
用裸 API 和 Claude Code 分别执行同一个任务：
```
# 方式一：裸 API 调用（没有 Harness）- 你可以换成Deepseek或GPT等任何模型
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-6-20260320",
    "max_tokens": 1024,
    "messages": [{"role":"user","content":"找出当前目录下所有 TODO 注释并列出文件名和行号"}]
  }'

# 方式二：通过 Harness（Claude Code）
claude -p "找出当前目录下所有 TODO 注释并列出文件名和行号" --output-format text
```

裸 API 会怎么回答？它会告诉你“你可以用 grep 命令来搜索”——因为它没有手脚，**只能说**。

Claude Code 会怎么做？它会直接执行  Grep  工具搜索 TODO，然后返回完整的文件名、行号和上下文——因为 **Harness 给了它行动的能力**。

同一个大脑，有没有 Harness，结果天壤之别。

我们从底层理解了 Claude Code 的真实身份——**它是一个  Harness，一个包裹在 Claude 模型外面的智能体编排框架**。

### **参考资料**
**Tier 1：AI 实验室一手资料**

**Anthropic**

- Effective Harnesses for Long-Running Agents：官方定义 harness 架构，Initializer + Coding Agent 两阶段设计。

- Building Effective Agents：2024.12 发表的行业奠基性文章，Workflow vs Agent 区分，Harness 概念前身。

- Building Agents with the Claude Agent SDK：Agent SDK 官方文档，暴露 Claude Code 内部的 Agent Loop。

**OpenAI**

- Harness Engineering：2026.2，正式提出 “harness engineering” 概念，~1500 自动化 PR。Unrolling the Codex Agent Loop：Codex CLI agent loop 详解。Unlocking the Codex Harness：Codex harness 的 App Server 层实现。

**Tier 2: 学术论文**

- Building Effective AI Coding Agents（arXiv 2603.05344），这篇论文是学术界对 Harness 概念的首次严肃形式化——scaffolding vs harness 的边界定义是本文最大贡献。文中以“首次 prompt”为分界线。之前是 scaffolding（搭脚手架），之后是 harness（操控）。佳哥个人认为这个定义简洁有力，应该成为行业标准。

**Tier 3: 行业内高影响力文章**

- Simon Willison，How Coding Agents Work，提出 “Coding agent = harness for LLM” 的经典定义。

- Inngest，Your Agent Needs a Harness, Not a Framework，重点看 Harness vs Framework 的区分。

- Swyx / Latent Space，Is Harness Engineering Real?，行业讨论，核心观点是“竞争优势在 Harness 而非 Model”。

- LangChain，Deep Agents (GitHub)，开源 Harness 实现，仅调 Harness 就让 Terminal Bench 提升 13.7 分。

- Lilian Weng，LLM Powered Autonomous Agents，2023 年的奠基综述，虽未用 “harness”一词但定义了同一架构。

- Parallel.ai，What is an Agent Harness，最佳独立解释文，定义 Harness 6 大组件，区分 Harness/Framework/Orchestrator。

# 基础篇 - 底层技术全景导览

## 工具

CC Switch 管“用哪个模型 + 哪个 MCP”
CCS（Claude Code Switch）管“哪个账户 + 哪个代理”

核心功能都是改  settings.json。

## 底层技术全景图
Claude Code 的底层能力从技术上拆解可以分为四个层次：基础层、扩展层、集成层和编程接口层。
![](assets/Claude%20Code%20-%20极客时间/file-20260421134003058.png)

### **基础层：Memory（记忆系统）**

基础层也可以称为是 Claude Code 的长期记忆系统，它的核心文件是 CLAUDE.md。

强烈建议每一个人都为你的 Claude 创建 CLAUDE.md，以提供给它一系列最基本的信息。例如，当我们要开始一个新的电商项目，我创建了下面的 CLAUDE.md 文件。
```markdown
# Project: E-commerce Platform

## Tech Stack
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL

## Code Style
- Use functional components
- Prefer async/await over .then()
- Maximum line length: 100 characters

## Important Rules
- NEVER commit to main directly
- Always run tests before pushing
```

Claude 每次开始对话时，都会读取这个文件。这样它就“记住”了你的项目规范，不需要每次重复说明。

Claude Code 并不是只有一个CLAUDE.md记忆文件，全局、项目和项目的特定模块都可以拥有属于自己的记忆文件（或者也可以叫配置文件）。

```markdown
~/.claude/CLAUDE.md           # 全局（所有项目共用）
    ↓
项目根目录/.claude/CLAUDE.md    # 项目级（当前项目）
    ↓
项目根目录/.claude/rules/*.md # 模块级（特定目录）
```


### **扩展层：四大核心组件**
#### **Commands（斜杠命令）- 用户手动触发**

斜杠命令是 Claude Code **内置或用户自定义**的一系列核心能力，其**触发方式是用户手动输入**  /命令名称

Commands 适合标准化操作——团队统一的 commit 格式、固定的部署流程等。

#### **Skills（技能）- Claude 或用户触发**

技能则代表着 AI 的一系列专属能力组合，其**触发方式是 Claude 自动判断**（语义推理）是否激活相应技能。Skills 可以是 Claude Code 内置的，也可以由用户自己设定。

- **和 call tool 区别**
Tools 是外部能力接口，Skills 是模型内部的“行为模式 + 触发逻辑”。

如果 Tool 是函数调用，Skill 就是把 if-else、prompt、策略和调用顺序，全部折叠进一个文档的整体封装，是对一个专有能力集的全面定义。

Tool 解决的是我能不能做；而 Skill 解决的是我该不该做、怎么做、做到什么程度。

- 和**Commands 区别**
Commands 是显式、可复用、可审计、通过斜杠命令固定触发的操作指令集，是相对固化的标准流程。

当一个能力具备强烈的“领域感”（安全、架构、性能）、判断依赖上下文而非关键词 ，执行路径可能变化 ，需要“像专家一样行事”时，就用 Skill，而不是 Command。

例如当用户问“帮我看看这段代码有没有安全问题”。Claude 的隐式判断流程是这样的。
```markdown
1️⃣ 这是代码吗？——是
2️⃣ 这是哪一类代码？——Node.js 后端
3️⃣ 上下文是否涉及用户输入？——是
4️⃣ 是否存在鉴权逻辑？——是
5️⃣ 是否值得深入做安全审查？——是
```
做完这些判断之后，就会自动激活 security-review Skill。

在 Skill 内部，是“像专家一样”的行为说明，它不会跑固定 checklist，而是根据语言选择重点、根据上下文跳过无关项、在发现高风险点时主动深挖、在安全风险低时明确告诉你“为什么没问题” —— 这不是流程执行，这是专家判断。

#### **SubAgents（子代理）- Claudu或用户触发**

子代理是除了 Skills 之外的另一个大杀器，用于独立完成专项任务。其**触发方式可以由 Claude 决定或用户指定**。
```markdown
主 Claude: 这个任务需要跑大量测试，让我创建一个子代理来处理。

子代理（test-runner）: 执行测试，只把结果汇报给主 Claude
```

SubAgents 适合**隔离执行**——高噪声任务（比如在大量日志中寻找出错信息，在大量文档中检索相关资源）、需要特定权限的任务。
![](assets/Claude%20Code%20-%20极客时间/file-20260421143119215.png)

#### **Hooks（钩子）- 事件自动触发**
钩子是在特定事件触发时自动执行的脚本，其**触发方式是事件自动触发**。
```markdown
事件: Claude 即将执行 Edit 工具

Hook: 自动检查是否有安全敏感内容

结果: 如果发现问题，阻止执行并警告
```

Hooks 适合**自动化检查**——格式化、安全检查、日志记录等。

### **集成层：连接外部世界**
上面这四大核心组件之上，是集成层，负责链接外部世界。集成层包含 Headless（无头模式）和 MCP（Model Context Protocol）两大技术。

- **Headless（无头模式）**
无头模式让 Claude Code 在没有人工交互的情况下运行，适合  CI/CD 集成——自动代码审查、自动修复、自动生成变更日志等。
```markdown
# GitHub Actions 中
- name: Auto-fix code issues
  run: claude --headless "Fix all linting errors in src/"
```

- **MCP（Model Context Protocol）**
MCP 让 Claude 连接外部工具和服务，适合工具连接——可以把任何外部系统变成 Claude 可调用的工具。
```markdown
Claude → MCP → 数据库
Claude → MCP → Jira
Claude → MCP → 自定义 API
```

### **编程接口层：Agent SDK**
当配置式的扩展不够用时，你可以用代码来驱动 Claude。这种方式适合**构建自定义 Agent**——完全控制执行流程、自定义工具、复杂工作流。
```python
from claude_sdk import ClaudeSDKClient

client = ClaudeSDKClient()

# 执行任务
result = client.query(
    prompt="Review this code for security issues",
    tools=["Read", "Grep"],
    max_turns=10
)
```


## 组件关系和技术选型指南

在真实的系统中，这些组件不是孤立存在的——它们相互协作，共同完成复杂任务。

### **触发方式**

首先看触发方式，也就是这些组件是怎么被激活的？不同组件的触发方式决定了它们的使用场景。
![](assets/Claude%20Code%20-%20极客时间/file-20260421144418045.png)
### **为什么“确定性”很重要？**

- 如果我们要设计一个生产系统：如果你需要“每次都必须执行”的操作（比如代码格式化），你需要 **100% 确定性**——选择 Commands 或 Hooks。

- 如果你希望 Claude “智能判断何时使用”（比如识别到安全问题时自动深入分析），你可以接受**概率性**——选择 Skills。

- 如果任务可能很重，你希望“既可以手动触发，也可以让 Claude 自己决定”，你需要**可控性**——选择 SubAgents。

### **数据流向**
数据是怎么在系统中流动的。这张图展示了一个典型请求的生命周期：
![](assets/Claude%20Code%20-%20极客时间/file-20260421145046081.png)
让我结合一个具体场景来解释这个流程——当用户输入“帮我修复 src/api.js 中的安全漏洞”之后，Claude 可能的处理流程如下。

1. Memory 层：Claude 首先加载  CLAUDE.md，了解到这是一个 Node.js 项目，团队要求所有安全修复必须附带测试。

2. 扩展层分发：

- a 用户没有输入斜杠命令，所以 Commands 不参与。

- b. Claude 识别出“安全漏洞”关键词，激活  security-review Skill。

- c. Skill 指示 Claude 创建一个子代理来执行测试。

3. Hooks 监控：Claude 准备执行  Edit  工具修改代码时，Hooks 自动运行预检查脚本，确保没有引入新的安全问题。

4. 工具执行：通过 Read、Edit 等工具完成代码修改。

5. MCP 连接：如果配置了 Jira MCP，还可以自动更新相关的 ticket 状态。

**Memory 是基础设施，始终存在；扩展层是能力中心，按需激活；Hooks 是守门人，监控一切。**

## Plugins：打包容器

当你开发了一套好用的 Commands、Skills、Hooks 组合，想要分享给团队或社区时，就需要 Plugins。

**Plugins 不是一种新能力，而是打包机制**——就像 npm 包把一堆 JavaScript 文件打包在一起，Plugin 把一组相关的 Claude Code 扩展打包在一起。

```markdown
my-team-plugin/
├── commands/           # 斜杠命令
│   └── review.md
├── skills/             # 技能
│   └── security-check/
│       └── SKILL.md
├── agents/             # 子代理
│   └── test-runner.md
├── hooks/              # 钩子
│   └── pre-edit.sh
└── plugin.json         # 插件配置
```

一个典型的 Plugins 使用场景：
	你是团队的技术 Lead，花了两周时间打磨出一套完美的代码审查流程：一个  /review  命令触发审查，一个  code-quality Skill 自动分析代码质量，一个  test-runner  子代理执行测试，还有一个 Hook 确保所有修改都有对应的测试。
	与其让团队成员手动复制这些文件，不如打包成一个 Plugin，新成员只需一条命令就能获得完整的工作流。

**Plugin 的价值在于可复用、可版本化、可分发。**

## 技术选型指南

当你面对一个真实需求时，如何选择正确的技术？下面这是我总结的决策流程：

![](assets/Claude%20Code%20-%20极客时间/file-20260421150226357.png)
用几个真实问题来演示这个决策树的使用。

问题 1：我希望团队成员都用统一的 commit message 格式。
- 这是一种“能力”吗？是的，是生成规范 commit message 的能力。

- 希望手动触发还是自动识别？手动触发更合适，因为不是每次对话都需要 commit。

- 答案：**适合用 Commands**（创建一个  /commit  命令）。

问题 2：每当 Claude 要修改代码时，我想自动检查是否符合我们的安全规范。

- 这是一种“能力“吗？不是，这是一种“检查机制”。

- 需要在工具执行时自动检查？ 对，在 Edit 工具执行前检查。

- 答案：**适合用 Hooks**（创建一个 pre-Edit hook）

问题 3：我想让 Claude 能够查询我们内部的知识库。

- 这是一种“能力”吗？ 不完全是，这是“连接外部数据源”。

- 需要连接外部系统？ 知识库是一个外部系统。

- 答案：**适合用 MCP**（创建一个知识库 MCP server）。

### **场景 VS 方案的速查表**
![](assets/Claude%20Code%20-%20极客时间/file-20260421150826181.png)
### **组合使用**
真实世界的问题很少能用单一技术解决。Claude Code 的强大之处在于组件可组合——每个组件做好自己的事，组合起来完成复杂任务。

假设你想实现这样一个流程：每当有人提交 PR，自动进行代码审查，发现问题就评论，没问题就通过。这需要组合多种技术：

```markdown
1. Headless 模式在 CI 中触发
   └── GitHub Actions 监听 PR 事件，调用 claude --headless

2. 调用 code-review SubAgent
   └── 隔离审查任务，避免污染主流程上下文

3. SubAgent 使用 security-check Skill
   └── 自动识别安全相关代码，应用专业审查规则

4. Hooks 记录审查日志
   └── 每次工具调用都记录，便于审计和调试

5. 结果通过 MCP 发送到 Slack
   └── 审查完成后通知相关人员
```

这五个步骤涉及五种不同的技术，但组合在一起就是一个完整的自动化流程。这就是可组合的威力。
![](assets/Claude%20Code%20-%20极客时间/file-20260421151240405.png)

### **Claude Code 扩展层 · 四大核心组件对照表** 
![](assets/Claude%20Code%20-%20极客时间/file-20260421151335830.png)


# 基础篇 - 记忆系统与CLAUDE.md

## Claude Code 记忆系统的工作原理
在项目目录启动 Claude Code 时，发生的“记忆系统初始化”过程如下图所示。
![](assets/Claude%20Code%20-%20极客时间/file-20260421154659441.png)
Claude Code 有多种方式获取项目相关知识，它们的区别如下表所示：
![](assets/Claude%20Code%20-%20极客时间/file-20260421154816613.png)
**CLAUDE.md 的内容会每次对话都加载**，所以要精简。把“每次都需要”的内容放这里，把“偶尔需要”的内容放到 Skills 或文档里。

## Claude Code 的五层记忆架构
Claude Code 支持五个层级的记忆，就像洋葱一样，从外到内，按**层级结构**组织——高层级的文件优先加载，为底层文件提供基础：
![](assets/Claude%20Code%20-%20极客时间/file-20260421155134524.png)
完整记忆类型表如下：
![](assets/Claude%20Code%20-%20极客时间/file-20260421155632449.png)
## 企业策略级记忆设定
企业策略级记忆设定的作用是组织范围内的指令，由 IT/DevOps 统一管理和部署组织。适合内容是，公司编码标准、安全策略、合规要求以及禁止使用的库或模式。通过配置管理系统（MDM、Group Policy、Ansible 等）部署，确保在所有开发者机器上一致分发。

位置：
- macOS: /Library/Application Support/ClaudeCode/CLAUDE.md

- Linux: /etc/claude-code/CLAUDE.md

- Windows: C:\ProgramFiles\ClaudeCode\CLAUDE.md

示例：
```markdown
# 公司开发策略

## 安全要求
- 禁止在代码中硬编码任何密钥或敏感信息
- 所有 API 调用必须使用 HTTPS
- 用户输入必须经过验证和清理

## 合规要求
- 所有日志必须排除 PII（个人身份信息）
- 数据库连接必须使用加密传输

## 禁止项
- 禁止使用未经审批的第三方库
- 禁止直接访问生产数据库
```

如果你是个人或小团队，可以直接跳过企业级设定这一层，不影响任何使用。

## 用户级内容设定
用户级内容设定承载的是你的全局偏好，即跨所有项目生效的个人偏好，如个人代码风格，沟通语言设置，通用工作习惯等。比如说我希望所有的 PPT 都是 16:9，黑体字。这种设置就应该放在此处。

位置：
~/.claude/CLAUDE.md

示例：
```markdown
# 个人偏好

## 沟通方式
- 使用中文回复
- 代码注释使用英文
- 解释简洁直接，不要过多铺垫

## 通用代码风格
- 缩进使用 2 空格
- 优先使用 async/await
- 变量命名使用 camelCase
- 常量命名使用 UPPER_SNAKE_CASE

## 我的常用工具
- 包管理器: uv
- 编辑器: VS Code
- 终端: zsh
```

用户级记忆会被项目级覆盖。如果你个人喜欢 2 空格缩进，但项目要求 4 空格，那就用 4 空格。

## 项目级团队共享规范
团队共享规范是团队共享的项目知识，应该提交到 Git。适合存放的内容包括项目架构和技术栈、团队编码规范、重要的设计决策和常用命令。

位置：
项目根目录的  ./CLAUDE.md

示例（一个后端 API 项目）：
```markdown
# 项目：订单服务 API

## 技术栈
- Node.js 20 + TypeScript
- Fastify（Web 框架）
- Prisma（ORM）
- PostgreSQL + Redis
- Zod（数据验证）

## 目录结构
src/ 
├── routes/ # 路由定义 
├── controllers/ # 请求处理 
├── services/ # 业务逻辑 
├── repositories/ # 数据访问 
├── schemas/ # Zod schemas 
└── types/ # 类型定义

## API 响应格式
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: { code: string; message: string };
}
编码规范
- TypeScript strict 模式
- 禁止使用 any，使用 unknown + 类型守卫
- 所有 API 端点必须有 Zod schema 验证
- 业务错误使用自定义 Error 类
常用命令
- pnpm dev - 启动开发服务器
- pnpm test - 运行测试
- pnpm prisma migrate dev - 运行数据库迁移
```

## 本地级个人工作空间
个人工作空间用于记载个人工作笔记，不提交到 Git，适合内容包括本地环境配置、个人调试技巧、当前工作备注，敏感信息（测试账号等）。

位置：
项目根目录的./CLAUDE.local.md

示例：
```markdown
# 本地开发笔记

## 我的环境
- 本地 API: http://localhost:3000
- 测试数据库: order_service_dev
- Redis: localhost:6379

## 测试账号
- admin@test.com / test123
- user@test.com / test123

## 当前工作
- 正在重构支付模块
- 参考 PR #234 的讨论
- 周五前完成

## 调试技巧
- 订单状态机日志: LOG_LEVEL=debug pnpm dev
- 查看 Redis 缓存: redis-cli KEYS "order:*"
```

这里重点强调一下：记得把  CLAUDE.local.md  加入  .gitignore！
```bash
echo "CLAUDE.local.md" >> .gitignore
```

## 规则目录：分类组织
rules 是按主题组织的规则文件，支持**条件作用域**（也就是视情况来确定是否加载该记忆内容），适合场景包括 CLAUDE.md 变得太长时，不同文件类型需要不同规范时，以及前后端分离的项目。

位置：.claude/rules/*.md

目录结构：
```markdown
.claude/
└── rules/
    ├── typescript.md      # TypeScript 规范
    ├── testing.md         # 测试规范
    ├── api-design.md      # API 设计规范
    └── security.md        # 安全规范
```

条件作用域示例：.claude/rules/testing.md
```python
---
paths:
  - "src/**/*.test.ts"
  - "tests/**/*.ts"
---

# 测试规范

## 命名
- 单元测试: `*.test.ts`
- 集成测试: `*.integration.test.ts`

## 结构
使用 Arrange-Act-Assert 模式：

```typescript
describe('OrderService', () => {
  describe('createOrder', () => {
    it('should create order when stock is available', async () => {
      // Arrange
      const mockProduct = createMockProduct({ stock: 10 });

      // Act
      const order = await orderService.createOrder(mockProduct.id, 1);

      // Assert
      expect(order.status).toBe('created');
    });
  });
});

## 覆盖率要求
- 业务逻辑: > 80%
- 工具函数: > 90%
- 路由/控制器: 可以较低
```

此处的关键特性是**paths字段让这个规则只在编辑测试文件时生效**，不会浪费其他场景的上下文空间。

## 编写高效的 CLAUDE.md

### **核心原则 1：Less is More**

CLAUDE.md 的每一行，都会在每一次对话开始时被自动注入上下文。这意味着一件事：冗余不是无害的，而是持续消耗的。所以保持精简不是建议，而是必须。

### **核心原则 2：具体优于泛泛**

一个非常常见、但几乎没有任何效果的写法。
```markdown
# 项目规范
## 代码质量
请写出高质量的代码。代码应该是可读的。使用有意义的变量名。
保持代码整洁。遵循最佳实践。不要写重复的代码。
```

真正有价值的 CLAUDE.md，应该长这样。
```markdown
# 项目规范

## TypeScript
- 使用 `interface` 定义对象结构，`type` 用于联合类型
- 禁止 `any`，使用 `unknown` + 类型守卫
- 函数参数 > 3 个时，使用对象参数

## 错误处理
```typescript
// 业务错误
throw new BusinessError('ORDER_NOT_FOUND', '订单不存在');

// 验证错误（Zod 自动抛出）
const data = orderSchema.parse(input);

// controller 中不要 try-catch
// 由全局错误中间件统一处理
```

有个简单的判断标准——如果你不写，Claude 也大概率会做对，那就不要写。

### **核心原则 3：关键三问题 WHY / WHAT / HOW**

一份真正“能用”的 CLAUDE.md，通常都在回答三个问题。不是一次性回答，而是在**关键地方给出明确指引**。

**WHY —— 为什么要这样做？**
```markdown
## 为什么使用 Zod？
- TypeScript 只有编译时类型检查
- API 输入需要运行时验证
- Zod 可以同时生成 TS 类型和验证逻辑
- 错误信息自动生成，对用户友好
```
这一部分的作用，不是让 Claude “记住一个库”，而是让它理解背后的决策逻辑。当 Claude 明白了为什么，它在面对相似但不完全相同的场景时，才更可能做出一致的判断。

**WHAT —— 具体要做什么，不要做什么？**
```markdown
## 数据库操作规范
- 所有查询通过 Prisma ORM
- 复杂查询封装在 `src/repositories/`
- 禁止在 controller/service 中直接写 SQL
- 事务使用 `prisma.$transaction()`
```
这一部分的重点是边界。什么是允许的，什么是禁止的，决策应该发生在哪一层？对 Claude 来说，这比“最佳实践”四个字重要得多。

**HOW —— 按什么步骤去做？**
```markdown
## 创建新 API 端点

1. 在 `src/schemas/` 创建请求/响应 Zod schema
2. 在 `src/routes/` 添加路由定义
3. 在 `src/controllers/` 实现请求处理
4. 在 `src/services/` 实现业务逻辑
5. 在 `tests/` 添加测试用例

示例参考: `src/routes/orders.ts`
```
当步骤清晰、路径明确、还有参考文件时，Claude 才会稳定复用同一套工作流，而不是每次自由发挥。

### **核心原则 4：渐进式披露：不要把一切都塞进 CLAUDE.md**
CLAUDE.md 的职责是定义默认决策，而不是承载全部知识。对于非核心、但可能被用到的内容，正确的做法是引用，而不是复制。
```markdown
# 项目规范

## 核心
[精简的核心规范]

## 详细文档
- 数据库设计: 见 `docs/database.md`
- API 规范: 见 `docs/api-spec.md`
- 部署流程: 见 `docs/deployment.md`
```
这样做有两个好处：
- CLAUDE.md 保持轻量，启动成本低 。
- 当 Claude 需要进一步的细节信息时，可以按需读取引用文件。

## CLAUDE.md 实战演练
### **场景一：为新项目创建记忆**
