如果我们只停留在“怎么写好一个 SKILL.md”，就会错过一个更大的故事。

- 2025 年 10 月，Anthropic 在 Claude Code 里上线了 Skills。那时候没人觉得这是什么大事——不过是一个 Markdown 文件里写写指令嘛。
- 2026 年 2 月，27+ Agent 平台原生支持这个格式。52,000+ Skills 被注册。Top Skills 单个安装量突破 180,000。

**从一个产品特性到行业开放标准，Skills 只用了不到百天。**

这一讲，我们来回答三个问题：第一，发生了什么；第二，为什么偏偏是 Skills 能出圈；第三，这对你作为 AI 工程师意味着什么。

我们先用一张图来完整复盘这些天里发生的事情。
![](assets/14%20从Claude%20Code到行业开放标准/file-20260427133956345.png)
整个故事的转折点是 12 月 18 日——不是技术突破，而是一个战略决策：Anthropic 选择把 Skills 开放。

在此之前，Skills 是 Claude Code 的竞争优势。开放意味着竞争对手可以免费使用它、甚至用它来对抗你。为什么 Anthropic 愿意这样做？

**因为标准的价值大于独占的价值。**

独占 Skills，只有 Claude Code 的用户可以用；开放 Skills，所有 Agent 平台上创建的 Skills 都兼容 Claude Code。这是典型的平台经济学——当你的格式成为行业标准，每个人创建的内容都在增强你的生态。就像 USB 标准，Intel 发明了它，但开放后全世界都在用，Intel 反而获益最大。

# 谁在用：四层采纳矩阵

知道了时间线，接下来看采纳范围。截至 2026 年为止的 27+ 平台并不是简单的堆砌数字，它们呈现出清晰的分层结构。
![](assets/14%20从Claude%20Code到行业开放标准/file-20260427134243395.png)
当 OpenAI 的 Codex CLI 和 Google 的 Antigravity 都支持你的格式时，这已经不是“一家公司的功能”了——它是事实标准。
```markdown
                    Agent Skills 采纳全景图

    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │   Anthropic                    OpenAI               │
    │   ├─ Claude Code ★(创始者)     ├─ Codex CLI         │
    │   └─ Claude.ai                └─ ChatGPT(测试中)    │
    │                                                     │
    │   Google                      Microsoft             │
    │   ├─ Antigravity              ├─ VS Code            │
    │   ├─ Gemini CLI               └─ GitHub Copilot     │
    │   └─ Gemini                                         │
    │                                                     │
    │   Block        Cursor         Windsurf    Trae      │
    │   └─ Goose     (原生支持)     (原生支持)   (原生支持) │
    │                                                     │
    │   Manus        Amp            Roo Code    Letta     │
    │   OpenCode     Kiro CLI       Droid       Kilo      │
    │                                                     │
    │                  共 27+ 平台                         │
    └─────────────────────────────────────────────────────┘
```

与此同时，Anthropic 还在  claude.com/connectors  上线了 Skills 目录，第三方合作伙伴发布了官方 Skill 包：
![](assets/14%20从Claude%20Code到行业开放标准/file-20260427134403352.png)
企业级管理方面，Anthropic 的 Team/Enterprise 计划支持管理员集中配置 Skills——控制哪些 Skills 可用，同时让员工自定义自己的工作流。

# Skills 出圈的三个本质属性

刚刚我们了解了“发生了什么”，更重要的问题是“为什么”。为什么是 Skills 出圈，而不是 SubAgents、不是 Hooks、不是 Plugins？

**第一，声明式（Declarative）**。 Skills 的载体是纯 Markdown 文件——YAML frontmatter 加 Markdown 正文。没有编程语言，没有 import/require，没有编译和构建步骤。这意味着什么？任何能读 Markdown 的系统都能理解一个 Skill。不需要 Python 运行时，不需要 Node.js 环境。Claude 能读，GPT 能读，Gemini 也能读——因为它们都能读 Markdown。

如果 Skills 是用 Python 类定义的（像 LangChain 的 Tool），那每个平台都需要一个 Python 运行时、兼容的 SDK、和特定的加载逻辑。切换平台就等于重写代码。

**第二，自包含（Self-contained）**。  一个 Skill 就是一个文件夹。它不依赖任何外部注册中心，不需要在某个平台注册，不需要安装特定的 runtime，不需要配置 API key，不需要连接外部服务。复制这个文件夹到任何支持 Skills 的 Agent 环境，它就能工作。这就是为什么 Git 是 Skills 的天然分发渠道——git clone  就是“安装”。

**第三，知识本位（Knowledge-centric）**。Skills 的价值不在格式——格式只是 Markdown；不在工具——工具是 Agent 自带的；不在运行时——运行时是 Agent 平台提供的。价值在内容本身，在“怎么做某件事”的知识，在可操作的领域智慧。一份好的“如何做代码审查”的 SOP，不管是 Claude 读还是 GPT 读还是 Gemini 读，知识本身都是有价值的。

这三个属性合在一起，天然具备跨平台复用的属性：
```markdown
声明式     → 任何 LLM 都能读
自包含     → 任何文件系统都能存
知识本位   → 知识的价值不绑定平台 
```
![](assets/14%20从Claude%20Code到行业开放标准/file-20260427135008404.png)

# 为什么 SubAgents 不能出圈

