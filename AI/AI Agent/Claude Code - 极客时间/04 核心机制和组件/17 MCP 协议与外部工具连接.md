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
这个架构的关键组件如下表所示。
![](assets/17%20MCP%20协议与外部工具连接/file-20260428143021906.png)
MCP 复用了  [Language Server Protocol (LSP)](https://en.wikipedia.org/wiki/Language_Server_Protocol)  的消息流思想。如果你用过 VS Code，你已经间接体验过这种架构——编辑器的智能提示、跳转定义等功能，都是通过 LSP 与语言服务器通信实现的。MCP 做了同样的事情，只不过它服务的不是代码编辑器，而是 AI Agent。

MCP Server 并不只是简单地“暴露一个函数”。它可以向 Client 提供三种不同类型的能力。
![](assets/17%20MCP%20协议与外部工具连接/file-20260428143144239.png)
Tools 是最常用的能力类型——它让 Claude 能够“做事情“。Resources 提供只读数据，让 Claude 能够“看到东西”而不仅仅依赖你粘贴的文本。Prompts 则是一种便捷机制，让服务器预定义好特定场景的交互模板。

Claude Code 会在启动时自动发现所有配置的 MCP Server 及其提供的能力。当你说“帮我查一下数据库里的用户数量”时，Claude 会自动找到数据库 MCP Server，调用对应的查询工具，解析结果并返回给你。整个过程对用户完全透明。

# MCP 的三种传输方式

MCP 支持三种传输方式，适用于不同场景。

## Stdio 传输（本地进程）

Stdio 传输（本地进程）是最简单的方式。MCP Server 作为本地子进程启动，通过标准输入（stdin）接收请求，通过标准输出（stdout）返回响应。零网络开销、零配置复杂度，适合本地工具和开发测试：
```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    }
  }
}
```

## HTTP 传输（推荐用于远程）

当 MCP Server 运行在远程服务器上时的推荐方式。通过标准 HTTP 请求 / 响应通信，支持 TLS 加密和 Bearer Token 认证。GitHub、Notion、Sentry 等云服务通常直接提供 HTTP 类型的 MCP 端点：
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    }
  }
}
```

## SSE 传输（Server-Sent Events）

基于 HTTP 的单向推送技术，建立持久连接，服务器可以主动向客户端推送数据。适合实时监控和流式数据场景。在实践中使用较少，大多数场景用 stdio 或 HTTP 就够了。

这几种方式怎么选呢？原则是，**本地用 stdio，远程用 HTTP，实时用 SSE**。如果你拿不定主意，先试 stdio（本地服务器）或 HTTP（远程服务），这两个覆盖了 95% 的场景。
![](assets/17%20MCP%20协议与外部工具连接/file-20260428143709994.png)
![](assets/17%20MCP%20协议与外部工具连接/file-20260428143734787.png)

# MCP 的配置与管理

MCP 配置可以放在多个位置，每个位置的作用域和可见性不同。
![](assets/17%20MCP%20协议与外部工具连接/file-20260428143823803.png)
**团队共享的服务**配置放到  `.mcp.json`——提交到 git，团队成员共享
**敏感凭证**放到  `.claude/settings.local.json`——不提交，本地保存
**个人常用服务**放到  `~/.claude/settings.local.json`——跨项目可用

不论使用哪种传输方式，MCP 配置都遵循同一个 JSON 结构。`mcpServers`  是顶层键，每个子键是服务器名称（可自由命名）。`type`  指定传输方式，剩余字段根据传输类型不同——stdio 需要  `command`  和  `args`，HTTP/SSE 需要  `url`  和  `headers`：
```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio | sse | http",
      "command": "...",        // stdio 专用
      "args": ["..."],         // stdio 专用
      "url": "...",            // sse/http 专用
      "headers": {},           // sse/http 专用
      "env": {}                // 环境变量
    }
  }
}
```

Claude Code 里面的 MCP 配置示例
![](assets/17%20MCP%20协议与外部工具连接/file-20260428144526573.png)

在配置文件中硬编码敏感信息是危险的。MCP 配置支持通过  `${}`  语法引用环境变量：`${VAR_NAME}` 直接引用，变量不存在会报错；`${VAR_NAME:-default}`  在变量不存在时使用默认值：
```json
{
  "mcpServers": {
    "secure-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}",
        "X-API-Key": "${API_KEY:-default-key}"
      }
    }
  }
}
```

Claude Code 提供了命令行工具来管理 MCP 服务器，这比手动编辑 JSON 更方便。
```markdown
# 添加 HTTP 服务器
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# 添加 stdio 服务器
claude mcp add filesystem -- npx @modelcontextprotocol/server-filesystem /path

# 添加到用户级别（所有项目可用）
claude mcp add --transport http --scope user github https://api.githubcopilot.com/mcp/

# 带认证头添加
claude mcp add --transport http --header "Authorization: Bearer ${TOKEN}" api https://api.example.com/mcp

# 列出所有服务器
claude mcp list

# 查看服务器详情
claude mcp get github

# 移除服务器
claude mcp remove github
```
