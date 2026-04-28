前面两讲我们学习了 Hooks——事件驱动自动化的安全闸门。Hooks 让我们能在 Claude 执行工具前后插入自定义检查，解决了“能不能做”的问题。但即使有了 Memory 的记忆、SubAgents 的分工、Skills 的领域能力、Commands 的标准流程、Hooks 的安全防护，Claude Code 的所有能力，始终被锁在一个边界内——本地文件系统。今天我们就来打破这个边界。

Claude 能读文件、写代码、执行命令，这些你已经非常熟悉。但面对下面这些需求时，它就无能为力了：

- 帮我查一下数据库里上个月的销售数据
- 把这个 Issue 同步到 GitHub
- 从 Notion 里读取产品需求文档
- 检查一下 Sentry 上最近的错误日志

这不是 Claude 不够聪明，而是它缺少与外部世界连接的通道。读代码、写代码、跑命令——本质都是本地文件系统交互。而企业开发的真实场景中，数据库、版本控制系统、项目管理平台、监控系统才是日常主战场。如果 Claude 无法触及这些系统，它就只能做一个聪明但孤立的本地助手。

2024 年 11 月，Anthropic 推出了一项开源协议，彻底改变了这个局面——Model Context Protocol (MCP)，AI 时代的 USB-C 接口（参见佳哥之前推出的专栏《[MCP & A2A 前沿实战》](https://time.geekbang.org/column/intro/101053801?tab=catalog)）。


# MCP——AI 的 USB-C 接口

在 MCP 出现之前，如果你想让 AI 助手连接外部服务，通常有两种选择：

1. **自定义开发**：为每个服务写专门的集成代码
2. **平台绑定**：依赖特定平台提供的插件（如 ChatGPT Plugins）

这带来了严重的碎片化问题。假设市场上有 M 个 AI 助手和 N 个外部服务，那么理论上需要 M × N 个专用适配器。每一对组合都需要单独开发、单独维护、单独调试：
![](assets/17%20MCP%20协议与外部工具连接/file-20260428140729131.png)
MCP 的出现改变了这一切。正如  [Anthropic 官方博客](https://www.anthropic.com/news/model-context-protocol)所描述的：

> 把 MCP 想象成 AI 应用的 USB-C 接口。就像 USB-C 提供了连接设备与各种外设的标准化方式，MCP 提供了连接 AI 模型与各种数据源和工具的标准化方式。 有了 MCP，M × N 的问题变成了 M + N：
![](assets/17%20MCP%20协议与外部工具连接/file-20260428140838339.png)

一个协议，通用连接。每个 AI 助手只需要实现一次 MCP Client，每个服务只需要实现一次 MCP Server，然后任意组合即可工作。
![](assets/17%20MCP%20协议与外部工具连接/file-20260428141028770.png)
MCP 的诞生源于一个简单的痛点。据  [Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)  记载，MCP 协议由 Anthropic 的两位工程师 David Soria Parra 和 Justin Spahr-Summers 构思并开发：

> 2024 年 7 月，我在做内部开发工具…作为一个开发工具背景的人，我很快就欣赏到 Claude Desktop 的强大——比如 Artifacts 功能——但也对它功能集有限、无法扩展感到沮丧。这个痛点在当时并非个例。每一个试图将 AI 助手集成到真实工作流中的工程师都面临同样的困境。David 和 Justin 的洞察在于：这个问题不应该由每个开发者各自解决，而应该由一个开放协议统一解决——就像 HTTP 统一了 Web、LSP 统一了 IDE 语言支持那样。

MCP 发布后，迅速获得了行业认可：
- 2025 年 3 月：OpenAI 正式采纳 MCP，将其集成到 ChatGPT 桌面应用和 Agents SDK 中
- 2025 年 9 月：Google 宣布为 Gemini 提供官方 MCP 支持
- 2025 年 12 月：Anthropic 将 MCP 捐赠给 Linux 基金会下的 Agentic AI Foundation (AAIF)
- AAIF 创始成员：OpenAI、Google、Microsoft、Amazon Web Services、Cloudflare、Bloomberg

截至 2025 年底，MCP 生态已经达到惊人的规模。
- 9700 万月度 SDK 下载量
- 10000+  公开 MCP 服务器（PulseMCP 目录收录 10,400+，MCP.so 收录 18,500+）
- 75+  官方 Claude 连接器
![](assets/17%20MCP%20协议与外部工具连接/file-20260428141349851.png)

# MCP 架构与核心概念

MCP 采用经典的客户端 - 服务器架构。Claude Code 充当 MCP Client，负责发现和调用工具；MCP Server 则暴露工具和资源，作为外部服务的代理。两者之间通过 JSON-RPC 2.0 协议通信。
![](assets/17%20MCP%20协议与外部工具连接/file-20260428141445713.png)
