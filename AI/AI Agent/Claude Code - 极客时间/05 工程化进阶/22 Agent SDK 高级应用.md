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
