上一讲我们学习了 Rules 规则系统，指令规则定义 Claude 该怎么做，权限规则定义 Claude 能做什么。两套规则协同运作，构成了完整的行为约束体系。但不管是 Headless 模式还是规则系统，本质上你还是在通过配置和命令行驱动 Claude Code，能做的事情有限：传一段 Prompt 进去，拿一段文本出来。

今天我们要更进一步，学习 Claude Agent SDK——它把 Claude Code 的所有能力封装成了可编程的接口。你可以用 Python 或 TypeScript 编写代码，像调用普通函数一样调用 AI Agent。

如果已经在 CI/CD 中大量使用 Claude Code：PR 自动审查、文档生成、代码分析。一切都运行得很好，有一天领导说：“我们想做一个功能，让用户在我们的产品里上传代码，然后 AI 自动分析并给出报告。”

思考思考，之前我们用的是命令行 + Headless 模式，但这次需要的是**在自己的应用里调用 Claude Code 的能力**。现在你需要的不是一个命令行工具，而是一个**可编程的 SDK**。命令行工具像一把螺丝刀，你手动拧一颗螺丝、拧两颗螺丝，够用。但当你要在流水线上每小时拧一千颗螺丝时，你需要的是一台电动螺丝机——**一个能被程序控制的接口**。

这就是 Claude Agent SDK 的价值——它把 Claude Code 的所有能力封装成了可编程的接口。你可以用 Python 或 TypeScript 编写代码，像调用普通函数一样调用 AI Agent。
![](assets/21%20通过Agent%20SDK%20掌控%20Claude%20Code/file-20260429144711977.png)
从配置驱动到代码驱动，是从“使用者”到“构建者”的关键一步。

# 什么是 Agent SDK

Claude Agent SDK 提供了**可编程的 Claude Code**。它不是一个新的模型 API，而是对 Claude Code 这个 Agent 系统的完整封装。你通过 SDK 调用的不是一个简单的文本生成接口，而是一个完整的 Agent 循环——Claude 会自主决定使用哪些工具、读取哪些文件、执行哪些命令，然后把结果返回给你。

正如 Anthropic 官方文档所述：

> Claude Agent SDK 让你能够构建自主运行的 AI Agent——它们可以读取文件、执行命令、搜索网络、编辑代码等。SDK 提供了驱动 Claude Code 的相同工具、代理循环和上下文管理能力。

简单来说，这三种方式形成了一个递进关系：**CLI 是手动操作，Headless 是自动化脚本，SDK 是可编程集成**。每一步都在降低人工干预的程度，提升集成的灵活性。
![](assets/21%20通过Agent%20SDK%20掌控%20Claude%20Code/file-20260429144929624.png)
![](assets/21%20通过Agent%20SDK%20掌控%20Claude%20Code/file-20260429144956116.png)

## Agent SDK 支持两种语言

**Python**：`pip install claude-agent-sdk`

**TypeScript**：`npm install @anthropic-ai/claude-agent-sdk`

两种语言的 API 设计保持一致，功能完全相同。这一讲以 Python 为主，同时提供 TypeScript 对照。选择哪种语言取决于你的技术栈——如果你的后端是 Django 或 FastAPI，用 Python；如果是 Express 或 Next.js，用 TypeScript。


# SDK 能力一览

下面这张表列出了 Agent SDK 赋予你的全部能力。每一项都对应 Claude Code 本身的一种工具，SDK 让你可以在自己的代码中精确控制这些工具的使用。
![](assets/21%20通过Agent%20SDK%20掌控%20Claude%20Code/file-20260429145225622.png)
理解了这张表，你就能回答前面问题了：用户上传代码后，Agent 可以用 Read 读取文件、用 Grep 搜索模式、用 Glob 遍历目录、用 Bash 运行测试——所有这些操作都在你的应用后端自动完成，用户只需要等待报告生成。

# 安装与环境配置

在开始编写代码之前，你需要安装 SDK 并配置好环境。这个过程很简单，但有几个关键点需要注意。

Python 安装要求 **Python 3.10** 及以上版本。之所以有这个版本要求，是因为 SDK 大量使用了`async/await`  语法和  `match/case`  模式匹配等现代 Python 特性。如果你的系统 Python 版本较低，建议使用  `pyenv`  或  `conda`  管理多个 Python 版本。
```bash
# 要求 Python 3.10+
pip install claude-agent-sdk
```

安装完成后，用一段简单的代码验证安装是否成功：
```python
from claude_agent_sdk import query
print("Claude Agent SDK installed successfully!")
```

TypeScript 方面，SDK 以 npm 包的形式分发，兼容 Node.js 18+ 环境：
```bash
npm install @anthropic-ai/claude-agent-sdk
```

验证安装：
```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';
console.log("Claude Agent SDK installed successfully!");
```

SDK 需要 Anthropic API Key 才能运行。这个 Key 是你与 Anthropic 服务器通信的凭证，所有的模型调用和 Token 消耗都会计入这个 Key 对应的账户。

最常见的配置方式是通过环境变量：
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

或者在代码中设置，适用于需要动态切换 Key 的场景（比如多租户 SaaS 应用，每个客户有自己的 Key）：
```python
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-api03-..."
```

如果你在 CI/CD 中使用，可以用 Secrets 管理：
```
env: 
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```


# 两种使用方式

Agent SDK 提供了两种使用方式，适用于不同场景。理解它们的区别是正确使用 SDK 的第一步。你可以把它们类比为 Python 中的  `requests.get()`  和  `requests.Session()`，前者是无状态的一次性调用，后者是有状态的会话管理。

## query() 函数：简洁高效

`query()`  是最简单的方式，适合轻量级用例。它接收一个 Prompt 字符串，返回一个异步迭代器，你可以逐条接收 Agent 产生的消息。整个过程不需要手动管理连接、配置选项或处理会话状态，SDK 帮你搞定一切。

这种设计的好处是显而易见的：当你只想快速验证一个想法、写一个脚本、或者做一次性的分析时，不需要写二十行初始化代码。一个函数调用就够了。

**Python**：
```python
from claude_agent_sdk import query
import asyncio

async def main():
    # 简单查询
    async for message in query("解释什么是递归"):
        if message.type == "text":
            print(message.text)

asyncio.run(main())
```

**TypeScript**：
```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

async function main() {
  for await (const message of query("解释什么是递归")) {
    if (message.type === 'text') {
      console.log(message.text);
    }
  }
}

main();
```

`query()`  的特点是：
- 一行代码即可调用
- 自动处理工具调用
- 循环适合单次、简单的任务

## ClaudeSDKClient 类：完整控制

当你需要更精细的控制时，比如限制 Agent 只能使用特定工具、设置最大执行轮次、管理多轮会话，就需要使用  `ClaudeSDKClient`。它提供了完整的配置能力，让你可以像搭积木一样组合 Agent 的行为。

与开箱即用的`query()`  不同，`ClaudeSDKClient`  要求你显式地创建客户端、配置选项、管理连接生命周期。这种显式性是刻意为之的，在生产环境中，你需要明确知道 Agent 能做什么、不能做什么、在什么条件下停止。隐式的默认值在生产中往往是 Bug 的温床。

**Python：**
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio

async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob"],
        max_turns=10,
        permission_mode="plan"  # 只读模式
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("分析 src/ 目录的代码结构")

        async for message in client.receive_response():
            if message.type == "text":
                print(message.text)
            elif message.type == "tool_use":
                print(f"Using tool: {message.tool_name}")

asyncio.run(main())
```

**TypeScript：**
```typescript
import { ClaudeSDKClient, ClaudeAgentOptions } from '@anthropic-ai/claude-agent-sdk';

async function main() {
  const options: ClaudeAgentOptions = {
    allowedTools: ['Read', 'Grep', 'Glob'],
    maxTurns: 10,
    permissionMode: 'plan'
  };

  const client = new ClaudeSDKClient(options);

  try {
    await client.connect();
    await client.query("分析 src/ 目录的代码结构");

    for await (const message of client.receiveResponse()) {
      if (message.type === 'text') {
        console.log(message.text);
      } else if (message.type === 'toolUse') {
        console.log(`Using: ${message.toolName}`);
      }
    }
  } finally {
    await client.disconnect();
  }
}

main();
```

`ClaudeSDKClient`的特点是：
- 完整的配置控制
- 支持自定义工具
- 支持 Hooks
- 支持会话恢复

选择哪种方式取决于你的具体场景。下面这张表可以帮你快速判断。
![](assets/21%20通过Agent%20SDK%20掌控%20Claude%20Code/file-20260429150620666.png)

一个简单的经验法则是，如果你在终端里用一行命令就能完成的事情，用`query()`；如果你需要在代码里做任何“配置”或“控制”，用  `ClaudeSDKClient`。

在实际项目中，常见的演进路径是先用  `query()`  快速验证想法，然后在功能成型后迁移到  `ClaudeSDKClient`  进行工程化。两种方式的消息格式完全兼容，迁移成本很低。

### **ClaudeAgentOptions 配置详解**

`ClaudeAgentOptions`  是控制 Agent 行为的核心配置类。你可以把它理解为 Agent 的“说明书”，它告诉 Agent 该用什么模型、能用什么工具、最多跑几轮、在什么目录下工作。每一个配置项都会直接影响 Agent 的行为和成本。

下面是完整的配置项。不需要一次记住所有配置，你可以先关注最常用的四个：`allowed_tools`、`permission_mode`、`max_turns`、`model`。其余的在需要时查阅即可。
```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # === 模型选择 ===
    model="sonnet",  # "sonnet" | "opus" | "haiku"

    # === 工具控制 ===
    allowed_tools=["Read", "Write", "Bash", "Grep", "Glob"],
    disallowed_tools=["Task"],

    # === 权限模式 ===
    permission_mode="default",  # "default" | "acceptEdits" | "plan" | "bypass"

    # === 执行控制 ===
    max_turns=20,
    cwd="/path/to/project",

    # === 输出格式 ===
    output_format="stream-json",  # "text" | "json" | "stream-json"

    # === 会话管理 ===
    continue_conversation=True,
    resume="session-id",

    # === 系统提示 ===
    system_prompt="You are a helpful coding assistant.",

    # === MCP 服务器 ===
    mcp_servers={
        "my-server": {...}
    },

    # === Hooks ===
    hooks={
        "PreToolUse": [...],
        "PostToolUse": [...]
    }
)
```


### **权限模式详解**

权限模式决定了 Agent 执行操作时的确认行为。这是安全性与自动化程度之间的一个权衡——你给 Agent 越多的自主权，它就能越快地完成任务，但风险也越高。

选择权限模式时，问自己一个问题：如果 Agent 做了一件错事，最坏的结果是什么？如果最坏结果“改错了一个文件，我  `git checkout`  恢复一下”，那可以放宽权限；如果最坏结果是“删除了生产数据库”，那必须严格控制。
![](assets/21%20通过Agent%20SDK%20掌控%20Claude%20Code/file-20260429151546645.png)

下面的代码展示了两种典型场景下的权限配置。代码审查只需要读取代码，不需要任何修改能力，所以用  `plan`  模式加上只读工具；自动修复则需要编辑文件的能力，但不需要执行任意命令，所以用  `acceptEdits`  模式搭配  `Read/Write/Edit`  工具。
```python
# 代码审查场景：只读
options = ClaudeAgentOptions(
    permission_mode="plan",
    allowed_tools=["Read", "Grep", "Glob"]
)

# 自动修复场景：接受编辑
options = ClaudeAgentOptions(
    permission_mode="acceptEdits",
    allowed_tools=["Read", "Write", "Edit"]
)
```

你可以精确控制 Agent 能使用哪些工具。SDK 提供了两种控制方式，白名单（`allowed_tools`）和黑名单（`disallowed_tools`）。

白名单是“只允许这些”，黑名单是“除了这些都允许”。在安全敏感的场景中，推荐使用白名单，明确列出 Agent 能用的工具，而不是试图列出所有它不能用的工具。

**内置工具列表：**
![](assets/21%20通过Agent%20SDK%20掌控%20Claude%20Code/file-20260429151811369.png)

下面展示了三种不同的工具限制策略。注意第三个例子——你可以用  Bash(git:* )  这样的语法来限制 Bash 工具只能执行特定前缀的命令，这比完全禁用 Bash 更加灵活。
```python
# 只允许读取操作
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob"]
)

# 禁用危险工具
options = ClaudeAgentOptions(
    disallowed_tools=["Bash", "Write"]
)

# 限制 Bash 命令（只允许 git 和 npm）
options = ClaudeAgentOptions(
    allowed_tools=["Bash(git:*)", "Bash(npm:*)"]
)
```

![](assets/21%20通过Agent%20SDK%20掌控%20Claude%20Code/file-20260429151940709.png)


### **消息类型与响应处理**

理解消息类型是正确处理 Agent 响应的关键。Agent 不是一次性返回结果的——它是一个**异步流**，在执行过程中会源源不断地产生不同类型的消息。你的代码需要根据消息类型分别处理，就像处理不同类型的网络事件一样。

Agent 在执行过程中会产生五种类型的消息。

`text`  是 Claude 生成的文本内容，比如分析结论、代码解释；`tool_use`  表示 Agent 正在调用某个工具；`tool_result`  是工具执行后返回的结果；`error`  表示执行过程中遇到了错误；`result`  是最终的汇总消息，包含执行时间、成本等元数据。
```python
async for message in client.receive_response():
    match message.type:
        case "text":
            # 文本响应
            print(message.text)

        case "tool_use":
            # 工具调用（Agent 正在使用工具）
            print(f"Tool: {message.tool_name}")
            print(f"Input: {message.tool_input}")

        case "tool_result":
            # 工具执行结果
            print(f"Result: {message.result}")

        case "error":
            # 错误信息
            print(f"Error: {message.error}")

        case "result":
            # 最终结果（任务完成）
            print(f"Final: {message.result}")
            print(f"Cost: ${message.total_cost_usd}")
```

