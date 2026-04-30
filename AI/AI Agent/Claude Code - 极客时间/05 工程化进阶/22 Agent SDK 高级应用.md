上一讲我们学习了 Agent SDK 的基础用法，包括如何创建 Agent、发送查询、处理响应，以及单次调用模式的核心 API。有了这些基础，你已经可以让 Claude 在程序中跑起来了。但要在真实的工程环境中使用它，仅靠基础 API 还远远不够。你需要扩展 Agent 的能力边界，需要在关键节点插入安全控制，需要管理多轮交互的上下文状态，更需要一套完整的生产级运维策略。

这一讲，我们就来深入 Agent SDK 的高级特性。我会带你从自定义工具开始，逐步走过 Hooks 系统、四层权限管理、流式会话，最终完成一个完整的实战项目——自动化测试修复 Agent。这个 Agent 能自动运行测试、分析失败原因、提出修复方案，甚至在获得确认后自动修复代码。

一个中型电商项目在每次提交代码前，CI 会运行完整的测试套件，大约 200 个测试用例。大部分时候测试都能通过，但偶尔会有几个测试失败。问题是，测试失败的原因千奇百怪。有时是代码逻辑错误，有时是测试本身过时了，有时是环境配置问题，有时是 Mock 数据不对。

每次失败，我们都要重复后面的流程。
1. 阅读测试输出，找到失败的测试
2. 打开对应的测试文件，理解测试逻辑
3. 打开被测试的代码，分析失败原因
4. 决定是修复代码还是修复测试
5. 修改，重新运行，验证

这个过程短则十分钟，长则一小时。

那么能否构建一个测试修复 Agent，它能自动运行测试、分析失败原因、提出修复方案，甚至在获得确认后自动修复代码呢？这样一个曾经需要 30 分钟的修复工作，现在只需要 3 分钟的人工确认。

这一讲，我们就来构建这样一个 Agent。

# 在 Agent 中注入和使用自定义工具

Claude Agent SDK 内置了文件操作、命令执行、网络搜索等工具。但在实际项目中，你往往需要领域特定的能力：

- 查询数据库
- 调用内部 API
- 发送通知
- 执行特定的业务逻辑

这就是自定义工具的价值，让 Agent 能够调用你定义的函数。SDK 的自定义工具本质上是运行在你应用进程内的 MCP 服务器。与需要单独进程的常规 MCP 服务器不同，SDK 工具直接在你的 Python 应用中运行，消除了进程管理和 IPC 开销。这种设计让工具调用的延迟极低，同时还能共享应用的内存空间和数据库连接池等资源。
![](assets/22%20Agent%20SDK%20高级应用/file-20260429163253531.png)

上图中的架构就是 **Agent → MCP Server → Tools 的三层解耦调用链**。

左侧的 Agent（大模型 + 记忆 + 推理）并不直接调用具体工具，而是通过统一的 `tool_use` 请求，将意图表达为标准化的工具调用（如` mcp__{server}__{tool}`）。中间的 MCP Server 相当于一个“工具路由中枢”，负责根据命名规范解析请求、完成权限控制与路由分发，并调用对应的工具函数。

右侧的各类自定义工具只专注于执行具体能力（如查询、搜索、发送等），执行完成后将结果返回给 MCP Server，再统一回传给 Agent。通过标准命名 + 中间层路由，实现 Agent 与工具的解耦、可扩展和可治理，从而让系统可以像“插 USB 设备”一样动态接入新能力。

## 使用 @tool 装饰器定义工具

`@tool`  装饰器是定义自定义工具的最简单方式。你只需要指定工具名称、描述和参数，然后把业务逻辑写在函数体内。SDK 会自动将这个函数注册为一个可被 Agent 调用的工具，Agent 在推理过程中会根据工具描述决定何时调用它。

下面的例子定义了一个天气查询工具。注意返回值必须是包含  `content`  列表的字典，这是 MCP 协议要求的标准格式。

```python
from claude_agent_sdk import tool

@tool(
    name="get_weather",
    description="Get current weather for a city",
    parameters={"city": str, "units": str}
)
async def get_weather(args):
    city = args["city"]
    units = args.get("units", "celsius")

    # 调用天气 API（示例）
    weather = await fetch_weather_api(city, units)

    return {
        "content": [
            {"type": "text", "text": f"Weather in {city}: {weather}"}
        ]
    }
```


下面是 ` @tool`  装饰器的三个核心参数，每个参数都直接影响 Agent 的调用行为。
![](assets/22%20Agent%20SDK%20高级应用/file-20260429163926139.png)
其中  `description`  尤为关键，它不是给人看的注释，而是给 AI 看的使用指南。写得清晰准确，Agent 才能在正确的时机调用正确的工具。

## 创建 SDK MCP 服务器承载工具

定义好工具函数之后，下一步是创建一个 MCP 服务器来承载它们。你可以把多个工具注册到同一个服务器中，服务器会统一管理这些工具的生命周期和调用路由。

下面的例子创建了一个包含两个工具的服务器。注意  `@tool`  装饰器的简写形式，当参数简单时，可以直接用位置参数传入名称、描述和参数字典。
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("greet", "Greet a user by name", {"name": str})
async def greet_user(args):
    return {
        "content": [
            {"type": "text", "text": f"Hello, {args['name']}!"}
        ]
    }

@tool("calculate", "Perform a calculation", {"expression": str})
async def calculate(args):
    try:
        result = eval(args["expression"])  # 生产环境请用安全的表达式解析器
        return {
            "content": [
                {"type": "text", "text": f"Result: {result}"}
            ]
        }
    except Exception as e:
        return {
            "content": [
                {"type": "text", "text": f"Error: {e}"}
            ],
            "isError": True
        }

# 创建 MCP 服务器
server = create_sdk_mcp_server(
    name="my-tools",
    version="1.0.0",
    tools=[greet_user, calculate]
)
```

服务器创建后，还不能直接使用。你需要把它注入到 Agent 的配置中，Agent 才能“看到”并调用这些工具。

## 注入并使用自定义工具

将 MCP 服务器注入 Agent 的方式很直观，通过  `mcp_servers`  选项传入服务器实例，然后在  `allowed_tools`  中声明允许使用的工具。工具名称遵循 ` mcp__{服务器名}__{工具名}`  的命名格式，这个双下划线的命名规则确保了不同服务器之间的工具名不会冲突。
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

options = ClaudeAgentOptions(
    mcp_servers={"tools": server},
    # 工具名称格式：mcp__{服务器名}__{工具名}
    allowed_tools=[
        "mcp__tools__greet",
        "mcp__tools__calculate"
    ]
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("Say hello to Alice and calculate 2 + 3 * 4")
    async for msg in client.receive_response():
        print(msg)
```

当 Agent 收到上面的提示时，它会自动识别出需要调用两个工具：先用  `greet`  向 Alice 打招呼，再用  `calculate`  计算表达式。这种自动编排能力正是 Agent SDK 的核心价值。

## 使用 Pydantic 进行参数验证

对于简单工具，字典式参数定义已经够用。但当参数变得复杂——比如有默认值、范围限制、可选字段时，Pydantic 模型是更好的选择。它不仅提供自动验证，还能生成更详细的 JSON Schema 供 Agent 参考，从而提高参数传递的准确性。

下面的例子定义了一个数据库查询工具。Pydantic 模型中的  `Field`  描述会被自动转换为工具参数说明，`ge`  和  `le`  约束则确保 Agent 传入的  `limit`  值在合理范围内。
```python
from pydantic import BaseModel, Field
from claude_agent_sdk import tool

class DatabaseQueryParams(BaseModel):
    """数据库查询参数"""
    table: str = Field(..., description="Table name")
    columns: list[str] = Field(default=["*"], description="Columns to select")
    where: str | None = Field(default=None, description="WHERE clause")
    limit: int = Field(default=100, ge=1, le=1000, description="Max rows")

@tool(
    name="query_database",
    description="Execute a SELECT query on the database",
    parameters=DatabaseQueryParams
)
async def query_database(args: DatabaseQueryParams):
    # args 已经通过 Pydantic 验证
    query = f"SELECT {', '.join(args.columns)} FROM {args.table}"
    if args.where:
        query += f" WHERE {args.where}"
    query += f" LIMIT {args.limit}"

    # 执行查询
    results = await db.execute(query)

    return {
        "content": [
            {"type": "text", "text": f"Query: {query}\nResults: {results}"}
        ]
    }
```

![](assets/22%20Agent%20SDK%20高级应用/file-20260429165612360.png)

下面是一个存在 SQL 注入风险的工具调用示例以及相应的调整。
```python
# 危险：直接执行 SQL
@tool("run_sql", "Run any SQL", {"sql": str})
async def run_sql(args):
    return await db.execute(args["sql"])  # SQL 注入风险！
```

```python
# 安全：限制操作类型
@tool("query_users", "Query user table", {"user_id": int})
async def query_users(args):
    return await db.execute(
        "SELECT * FROM users WHERE id = ?",
        [args["user_id"]]
    )
```

这个安全示例的核心在于，**不要把工具当“能力接口”，而要当“受控权限边界”来设计**。

危险版本把任意 SQL 执行权直接暴露给 Agent，相当于让一个不完全可信的系统拥有数据库 root 权限，一旦被误导或注入就可能造成严重破坏；而安全版本通过限制操作范围（只允许查询特定表）、使用参数化查询、防止注入，并对参数进行类型约束，把“无限能力”收敛为“可控动作”。本质上，这体现的是 Agent 系统的一个关键原则，**模型可以自由推理，但工具必须严格受限。**


# Agent SDK Hooks 系统概述

Hooks 让你能够在 Agent 执行的各个阶段插入自定义逻辑。如果说自定义工具是扩展了 Agent 能做什么，那么 Hooks 就是控制 Agent 怎么做。它们提供对 Agent 行为的确定性控制——不是建议 Agent 遵守某个规则，而是在系统层面强制执行。

下表列出了 SDK 支持的所有 Hook 事件。每个事件对应 Agent 执行流程中的一个关键节点，你可以在这些节点插入安全检查、日志记录、数据转换等逻辑。
![](assets/22%20Agent%20SDK%20高级应用/file-20260430142037800.png)
## PreToolUse Hook：执行前拦截

PreToolUse 是最常用的 Hook，它在工具执行前触发。你可以在这里做三件事，允许执行、拒绝执行、或修改输入参数。这给了你对 Agent 行为的完全控制权。

下面的例子展示了一个 Bash 命令安全检查器。它会拦截所有 Bash 工具调用，检查命令是否包含危险模式（如  rm -rf、sudo），如果发现危险则拒绝执行。对于不在白名单中的命令，它会要求用户手动确认。
```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

async def check_bash_command(input_data, tool_use_id, context):
    """检查 Bash 命令是否安全"""
    tool_name = input_data["tool_name"]
    tool_input = input_data["tool_input"]

    if tool_name == "Bash":
        command = tool_input.get("command", "")

        # 阻止危险命令
        dangerous_patterns = ["rm -rf", "sudo", "chmod 777", "> /dev/"]
        for pattern in dangerous_patterns:
            if pattern in command:
                return {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"Blocked dangerous command: {pattern}"
                    }
                }

        # 只允许特定命令
        allowed_prefixes = ["npm", "python", "git", "pytest", "ls", "cat"]
        if not any(command.strip().startswith(p) for p in allowed_prefixes):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": f"Command requires approval: {command}"
                }
            }

    return {}  # 允许执行

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[check_bash_command])
        ]
    }
)
```

注意  `HookMatcher`  的  `matcher`  参数，它指定这个 Hook 只对  `Bash`  工具生效。你也可以用  `"*"`  来匹配所有工具。

## PreToolUse Hook：修改输入参数

从 Claude Code v2.0.10 开始，PreToolUse Hook 获得了一个强大的新能力——修改工具输入。这意味着你可以在工具执行前对参数进行转换、规范化或补充，而 Agent 对此完全无感知。

一个典型的应用场景是路径规范化。Agent 生成的文件路径有时是相对路径，但你的工具可能要求绝对路径。通过 PreToolUse Hook，你可以在调用发生前自动完成转换，避免工具报错。
```python
async def normalize_file_paths(input_data, tool_use_id, context):
    """规范化文件路径"""
    tool_name = input_data["tool_name"]
    tool_input = input_data["tool_input"]

    if tool_name in ["Read", "Write", "Edit"]:
        file_path = tool_input.get("file_path", "")

        # 将相对路径转为绝对路径
        if not file_path.startswith("/"):
            import os
            absolute_path = os.path.abspath(file_path)

            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "updatedInput": {
                        **tool_input,
                        "file_path": absolute_path
                    }
                }
            }

    return {}

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="*", hooks=[normalize_file_paths])
        ]
    }
)
```

返回值中的  `updatedInput`  字段就是修改后的工具输入。SDK 会用它替换原始输入，然后继续执行工具。

## PostToolUse Hook：执行后处理

PostToolUse 在工具执行成功后触发，适合做日志记录、结果格式化、自动化后处理等工作。与 PreToolUse 不同，PostToolUse 无法改变已经发生的工具调用，但它可以基于调用结果执行额外操作。

下面展示了两个实用的 PostToolUse Hook。第一个记录所有工具的使用日志，用于审计和调试。第二个在文件写入后自动运行代码格式化工具，确保 Agent 生成的代码符合团队代码风格规范。
```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def log_tool_usage(input_data, tool_use_id, context):
    """记录工具使用日志"""
    tool_name = input_data["tool_name"]
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})

    logger.info(f"[{datetime.now().isoformat()}] Tool: {tool_name}")
    logger.info(f"  Input: {tool_input}")
    logger.info(f"  Response: {str(tool_response)[:200]}...")

    return {}

async def auto_format_code(input_data, tool_use_id, context):
    """文件写入后自动格式化"""
    tool_name = input_data["tool_name"]
    tool_input = input_data.get("tool_input", {})

    if tool_name in ["Write", "Edit"]:
        file_path = tool_input.get("file_path", "")

        # 根据文件类型运行格式化
        if file_path.endswith(".py"):
            import subprocess
            subprocess.run(["black", file_path], capture_output=True)
        elif file_path.endswith((".ts", ".js")):
            import subprocess
            subprocess.run(["prettier", "--write", file_path], capture_output=True)

    return {}

options = ClaudeAgentOptions(
    hooks={
        "PostToolUse": [
            HookMatcher(matcher="*", hooks=[log_tool_usage]),
            HookMatcher(matcher="Write", hooks=[auto_format_code]),
            HookMatcher(matcher="Edit", hooks=[auto_format_code])
        ]
    }
)
```

自动格式化这个 Hook 特别实用。Agent 生成的代码虽然逻辑正确，但缩进、换行、引号风格可能不符合项目规范。有了这个 Hook，你再也不需要手动跑格式化了。

# canUseTool 回调：运行时权限控制

除了 Hooks，SDK 还提供了  `canUseTool`  回调作为另一种权限控制方式。它比 Hooks 更简单，只负责回答一个问题：“这个工具调用是否被允许？”不涉及输入修改、日志记录等复杂逻辑，适合纯粹的权限判断场景。

下面的例子展示了一个保护敏感文件和限制网络操作的  `canUseTool`  回调。当 Agent 试图读写受保护的文件或执行网络命令时，回调会返回拒绝并附带原因说明。
```python
# 受保护的文件列表
PROTECTED_FILES = [
    ".env",
    "secrets.json",
    "config/production.yaml",
    "database/migrations/"
]

async def can_use_tool(tool_name: str, tool_input: dict) -> dict:
    """运行时权限检查"""

    # 检查文件操作
    if tool_name in ["Write", "Edit", "Read"]:
        file_path = tool_input.get("file_path", "")

        for protected in PROTECTED_FILES:
            if protected in file_path:
                return {
                    "allowed": False,
                    "reason": f"Access to {protected} is not allowed"
                }

    # 检查 Bash 命令
    if tool_name == "Bash":
        command = tool_input.get("command", "")

        # 禁止网络操作
        network_commands = ["curl", "wget", "nc", "ssh"]
        for cmd in network_commands:
            if cmd in command:
                return {
                    "allowed": False,
                    "reason": f"Network command '{cmd}' is not allowed"
                }

    return {"allowed": True}

options = ClaudeAgentOptions(
    can_use_tool=can_use_tool
)
```

# Hooks 与 canUseTool 的选择

Hooks 和 canUseTool 都能控制工具的使用权限，但它们的能力范围差异很大。理解这个差异对于选择合适的机制至关重要。
![](assets/22%20Agent%20SDK%20高级应用/file-20260430143607857.png)

简单来说，只需要权限检查，用  `canUseTool`；需要修改输入、记录日志、执行后处理，用 Hooks。在实际项目中，两者经常配合使用，`canUseTool`  负责快速的权限判断，Hooks 负责更复杂的拦截和处理逻辑。

# Agent SDK 权限管理：四道防线

安全是构建生产级 Agent 的核心议题。Agent SDK 提供了四种互补的权限控制机制，**权限模式、canUseTool 回调、Hooks、settings.json 中的权限规则**。它们构成了一个分层防御体系。

## 权限模式：全局基调

权限模式是最粗粒度的控制，它设定了整个会话的安全基调。一共有四种模式可选，从宽松到严格，你需要根据使用场景选择合适的模式。
```python
options = ClaudeAgentOptions(
    permission_mode="acceptEdits"  # 自动接受文件编辑
)
```
![](assets/22%20Agent%20SDK%20高级应用/file-20260430143924424.png)
## 工具白名单与黑名单

第二道防线是工具级别的准入控制。通过  `allowed_tools`  和  `disallowed_tools`，你可以精确控制 Agent 能使用哪些工具。这比权限模式更细粒度，你可以允许文件读取但禁止网络搜索，或者只允许运行特定的 Bash 命令。
```python
options = ClaudeAgentOptions(
    # 只允许这些工具
    allowed_tools=["Read", "Grep", "Glob", "Bash(pytest:*)"],

    # 禁用这些工具
    disallowed_tools=["Task", "WebSearch"]
)
```

注意  `Bash(pytest:*)`  这个语法，它表示只允许以  pytest  开头的 Bash 命令。这种细粒度的 Bash 命令过滤是生产环境中非常实用的安全特性。

## 动态权限检查

第三道防线是运行时动态权限检查（`canUseTool`）

## Hooks 控制

第四道防线是最细粒度的 Hooks 控制。

## 项目综合使用

在实际项目中，这四道防线应该配合使用，形成纵深防御。下面的代码展示了一个完整的四层安全配置。请注意每一层防线各司其职：**权限模式设定基调，白名单限制工具集，canUseTool  保护敏感资源，Hooks 提供细粒度控制和审计**。
```python
options = ClaudeAgentOptions(
    # 第一道：权限模式
    permission_mode="acceptEdits",

    # 第二道：工具白名单
    allowed_tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
    disallowed_tools=["WebSearch"],  # 禁止网络搜索

    # 第三道：运行时检查
    can_use_tool=can_use_tool,

    # 第四道：Hooks
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[check_bash_command]),
            HookMatcher(matcher="*", hooks=[log_all_tools])
        ],
        "PostToolUse": [
            HookMatcher(matcher="Write", hooks=[auto_format])
        ]
    }
)
```

# 流式会话：为什么以及怎么用

到目前为止，我们的示例都使用的是单次查询模式——发送一个请求，接收一个响应。但在生产环境中，你往往需要多轮对话、中途干预、动态调整参数。这就是流式会话（Streaming Session）的价值。流式输入模式是使用 Claude Agent SDK 的首选方式。它允许 Agent 作为长时间运行的进程，接收用户输入、处理中断、显示权限请求、管理会话。

下表清晰展示了两种模式的差异。
![](assets/22%20Agent%20SDK%20高级应用/file-20260430144531972.png)

**流式会话的核心优势是保持上下文**。在同一个  `async with`  块内，你可以发送多次查询，每次查询都能“看到”之前的对话历史。这让 Agent 能够执行复杂的多步骤任务，而不需要你手动管理上下文。
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def streaming_session():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="default"
    )

    async with ClaudeSDKClient(options=options) as client:
        # 第一轮对话
        await client.query("列出当前目录的 Python 文件")
        async for msg in client.receive_response():
            if msg.type == "text":
                print(msg.text)

        # 继续对话（保持上下文）
        await client.query("分析第一个文件的代码质量")
        async for msg in client.receive_response():
            if msg.type == "text":
                print(msg.text)

        # 再次继续
        await client.query("修复发现的问题")
        async for msg in client.receive_response():
            print(msg)
```

这三轮对话共享同一个会话上下文。Agent 在第二轮能引用第一轮列出的文件，在第三轮能基于第二轮的分析结果执行修复。

## 处理权限请求

在流式模式中，当 Agent 试图执行需要权限的操作时，SDK 不会自动处理，而是将权限请求发送给你的代码。你可以根据工具类型、命令内容等信息做出自动决策，也可以将决策权交给用户。

下面的例子展示了一种混合策略：对于测试命令自动批准，对于其他命令则询问用户。
```python
async def handle_permission_request(request):
    """处理权限请求"""
    tool_name = request.get("tool_name")
    tool_input = request.get("tool_input")

    print(f"\nPermission Request:")
    print(f"   Tool: {tool_name}")
    print(f"   Input: {tool_input}")

    # 自动决策或询问用户
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if command.startswith("npm test") or command.startswith("pytest"):
            return {"approved": True}

    # 询问用户
    response = input("   Approve? (y/n): ")
    return {"approved": response.lower() == "y"}

async with ClaudeSDKClient(options=options) as client:
    await client.query("运行测试并修复失败的测试")

    async for msg in client.receive_response():
        if msg.type == "permission_request":
            decision = await handle_permission_request(msg)
            await client.respond_to_permission(msg.id, decision)
        else:
            print(msg)
```

## 中断和取消

流式会话支持在任意时刻中断 Agent 的执行。这在 Agent 陷入无意义循环、执行时间过长、或用户改变主意时非常有用。调用  `client.interrupt()`  后，Agent 会停止当前操作，但会话上下文仍然保留，你可以继续发送新的查询。
```python
import asyncio

async def interruptible_session():
    async with ClaudeSDKClient(options=options) as client:
        await client.query("分析整个代码库")

        try:
            async for msg in client.receive_response():
                print(msg)

                # 检查是否需要中断
                if should_interrupt():
                    await client.interrupt()
                    print("Task interrupted by user")
                    break

        except asyncio.CancelledError:
            print("Session cancelled")
```

## 动态切换设置

流式模式还有一个独特的能力：在会话中途动态切换设置。最典型的场景是“先分析后执行”模式，先用只读模式让 Agent 分析问题并制定计划，用户确认后再切换到可编辑模式执行修改。这种两阶段工作流在生产环境中非常常见，它既保证了安全性，又保持了效率。
```python
async with ClaudeSDKClient(options=options) as client:
    # 开始时使用只读模式
    await client.update_options(permission_mode="planMode")
    await client.query("分析代码并制定修复计划")
    async for msg in client.receive_response():
        print(msg)

    # 用户确认后，切换到可编辑模式
    await client.update_options(permission_mode="acceptEdits")
    await client.query("执行刚才的修复计划")
    async for msg in client.receive_response():
        print(msg)
```
![](assets/22%20Agent%20SDK%20高级应用/file-20260430145724723.png)

# 实战项目：自动化测试修复 Agent

现在，让我们把前面学到的所有高级特性组合起来，构建开篇故事中的测试修复 Agent。这个项目会用到自定义工具（运行测试）、Hooks（安全控制）、流式会话（两阶段工作流）和四层权限管理。

这个项目的项目需求是构建一个 Agent 来完成下面的任务。

1. 运行测试套件，捕获失败信息
2. 分析失败原因
3. 提出修复方案
4. 在确认后执行修复
5. 重新运行测试验证

## 自定义工具：测试运行器

首先，我们需要一个能够运行测试并返回结构化结果的自定义工具。这个工具会调用 pytest，解析 JSON 报告，提取失败测试的详细信息（测试名称、错误信息），然后以标准 MCP 格式返回给 Agent。

Agent 拿到这些结构化数据后，就能精确定位需要分析的文件和代码行。



