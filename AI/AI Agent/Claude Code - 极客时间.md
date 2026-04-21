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

# 基础篇

## 工具

CC Switch 管“用哪个模型 + 哪个 MCP”
CCS（Claude Code Switch）管“哪个账户 + 哪个代理”

核心功能都是改  settings.json。

## 底层技术全景图
Claude Code 的底层能力从技术上拆解可以分为四个层次：基础层、扩展层、集成层和编程接口层。
![](assets/Claude%20Code%20-%20极客时间/file-20260421134003058.png)

### 基础层：Memory（记忆系统）

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
项目根目录/CLAUDE.md          # 项目级（当前项目）
    ↓
项目根目录/.claude/rules/*.md # 模块级（特定目录）
```

