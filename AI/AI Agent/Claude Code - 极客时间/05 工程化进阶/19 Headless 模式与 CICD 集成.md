之前，我们庖丁解牛，深入剖析了 Claude Code 的工具系统——十几个精选的原语工具覆盖五个原子操作，通过涌现产生无限复杂能力。工具系统回答了一个核心问题：**Claude Code 能做什么**。但不管工具有多强大，有一个前提始终没变：你得坐在终端前面，实时和 Claude 对话。

这一讲，我们要打破这个前提。我们要让 Claude Code 在完全没有人工干预的情况下自动运行——在 CI/CD 流水线中审查代码，在 pre-commit hook 里检查提交，在定时任务中生成报告。这就是 Headless 模式的核心：从“有人值守”到“无人值守”。

# 凌晨三点的代码审查

这是一个分布在三个时区的远程团队：美国西海岸、欧洲、亚洲。当亚洲的小王在早上 9 点提交 PR 时，美国的 Tech Lead 还在睡觉。当美国的同事审查完代码时，小王已经下班了。每个 PR 的审查周期动辄 24-48 小时，不是因为审查本身需要那么长时间，而是因为人的作息时间不同步。

有一天，团队配置了一个 GitHub Action：每当 PR 创建或更新时，Claude Code 会自动进行初步审查——检查代码风格、潜在 Bug、安全问题。当人类审查者醒来时，他们看到的不是一片空白的 PR，而是已经有一份详细的 AI 审查报告。

**PR 的平均审查周期从 36 小时缩短到了 8 小时。**

这就是 Headless 模式的价值：让 Claude Code 在没有人工干预的情况下自动工作。它并不是取代人类审查者，而是在人类不在线的时候先行一步，把基础工作做好。这样我们打开 PR 时，就可以直接从 AI 的审查报告出发，聚焦于需要人类判断力的高层问题——**架构合理性、业务逻辑正确性、团队规范一致性**——而不是把时间花在检查缩进和命名规范上。


# Headless 模式核心机制

在前面的章节中，我们一直在终端里与 Claude 对话——你输入一句话，Claude 响应，你再输入，它再响应。这是**交互模式**。交互模式的好处是灵活，你可以随时调整方向、追问细节、确认操作。但它有一个根本限制——需要一个人类一直坐在屏幕前面。

然而，软件工程中有大量任务天然不需要实时对话。CI/CD 流水线在每次提交时自动运行，Pre-commit Hook 在提交前自动检查，定时任务在每天凌晨自动生成报告。这些场景需要的是**非交互模式**，也就是 Headless 模式。

> [Anthropic 官方文档](https://code.claude.com/docs/en/headless)说：Claude Code 包含 Headless 模式，用于 CI、pre-commit hooks、构建脚本和自动化等非交互式场景。

Headless 这个词来自“无头浏览器”（Headless Browser）的概念——没有图形界面，但功能完整。同样，Headless 模式下的 Claude Code 没有交互式终端界面，但拥有和交互模式完全相同的代码分析能力、工具调用能力和推理能力。唯一的区别是：**输入变成了一次性的 prompt，输出变成了 stdout 上的文本或 JSON，不再有来回对话**。

启用 Headless 模式的关键是  `-p`（或  `--print`）标志。这个标志的名字很直观，print，意思是“把结果打印出来就行，不要打开交互界面”。理解这一点很重要，因为  `-p`  不只改变了输出方式，更重要的是它改变了 Claude Code 的整个运行模型——**从“持续对话”变成了“单次执行”**。
```markdown
# 基本 headless 执行
claude -p "解释这段代码是做什么的"

# 从 stdin 读取输入
cat code.py | claude -p "分析这段代码"

# 结合文件内容
claude -p "找出这个文件中的 Bug" < buggy.js
```

`-p`  告诉 Claude Code：不要打开交互界面，直接执行任务，把结果输出到 stdout，然后退出。这种“执行即退出”的模式，正是脚本和流水线所需要的——它们不需要等待用户输入，只需要一个确定性的输入 - 输出流程。

下表清晰地展示了两种模式在各个维度上的差异。理解这些差异，有助于你判断什么场景适合用交互模式，什么场景应该切换到 Headless。我给你一个简单的判断标准：**如果任务需要人类在过程中做决策，用交互模式**；**如果任务的输入和期望输出在启动前就能完全确定，用 Headless**。
![](assets/19%20Headless%20模式与%20CICD%20集成/file-20260429092141467.png)

Headless 模式提供了一组命令行参数来精细控制执行行为。这些参数是你在自动化脚本和 CI 配置中最常用的控制手段。特别值得注意的是  `--allowedTools`  和  `--max-turns`  这两个参数，它们是**安全防护的第一道防线**，能有效限制 Claude 在无人监管环境中的行为边界。
![](assets/19%20Headless%20模式与%20CICD%20集成/file-20260429092717381.png)
![](assets/19%20Headless%20模式与%20CICD%20集成/file-20260429092845294.png)

# 输出格式与管道集成

Headless 模式支持三种输出格式，适用于不同的自动化场景。选择哪种格式，取决于你的下游消费者是谁——是人类读者、是程序解析器、还是实时监控系统。

## Text 格式

**Text 是默认格式**，也是最简单的格式。适用场景为日志记录、简单脚本、人工审查。它直接输出 Claude 的回复文本，没有任何元数据包装。如果你只是想在终端里看结果，或者将结果写入日志文件，Text 格式就够了。
```bash
claude -p "生成一个 Python hello world 函数" --output-format text
```

输出：
```python
Here's a simple hello world function:

def hello_world():
    print("Hello, World!")
```

## JSON 格式

当你需要在程序中解析 Claude 的输出时，JSON 格式是更好的选择。它不仅包含回复文本本身，还包含执行的元数据——耗时多久、花了多少钱、用了多少 tokens。这些元数据对于成本监控和性能调优至关重要。在生产环境的 CI/CD 流水线中，你几乎总是应该使用 JSON 格式，因为它让你能够用程序化的方式验证执行结果、追踪成本、检测异常。
```bash
claude -p "列出当前目录文件" --output-format json
```

输出：
```json
{
  "type": "result",
  "subtype": "success",
  "session_id": "abc123",
  "is_error": false,
  "duration_ms": 1500,
  "duration_api_ms": 1200,
  "num_turns": 1,
  "total_cost_usd": 0.005,
  "usage": {
    "input_tokens": 150,
    "output_tokens": 200
  },
  "result": "文件列表：\n- file1.py\n- file2.js\n..."
}
```

下面是一个 Python 解析示例。这段代码展示了如何在脚本中调用 Claude Code 并提取结构化结果。注意  `subprocess.run`  的用法——它是在 Python 中调用外部命令的标准方式，`capture_output=True`  确保我们能拿到 stdout 的内容。
```python
import subprocess
import json

result = subprocess.run(
    ["claude", "-p", "列出文件", "--output-format", "json"],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
print(f"结果: {data['result']}")
print(f"耗时: {data['duration_ms']}ms")
print(f"费用: ${data['total_cost_usd']}")
```

## Stream-JSON 格式

对于长时间运行的任务，你可能不想等到执行完成才看到输出，因此这种格式适用于实时进度显示、长时间任务监控、流式处理。Stream-JSON 格式以 JSONL（每行一个 JSON 对象）的方式实时输出执行过程中的每个事件——Claude 的每段回复、每次工具调用、每个工具返回结果。

这种格式特别适合需要实时进度显示的场景，比如在 CI 日志中实时展示 Claude 正在做什么。
```bash
claude -p "分析代码" --output-format stream-json
```

输出里（每行一个事件）：
```json
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"正在分析..."}]}}
{"type":"tool_use","tool":"Read","input":{"file_path":"/path/to/file"}}
{"type":"tool_result","tool":"Read","result":"file content..."}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"分析完成。"}]}}
{"type":"result","session_id":"abc123","is_error":false,"result":"最终结果"}
```

下面这段 Bash 脚本展示了如何逐行读取 Stream JSON 输出，并根据事件类型做出不同响应。你可以在此基础上扩展，比如在检测到  tool use  事件时，更新进度条，在检测到  result  事件时触发下游通知。
```bash
claude -p "分析代码" --output-format stream-json | while IFS= read -r line; do
  type=$(echo "$line" | jq -r '.type')
  if [ "$type" = "result" ]; then
    echo "最终结果: $(echo "$line" | jq -r '.result')"
  elif [ "$type" = "tool_use" ]; then
    echo "正在使用工具: $(echo "$line" | jq -r '.tool')"
  fi
done
```


# Unix 管道集成

Claude Code 的一个独特优势是它可以无缝融入 Unix 管道，成为你工具链中的一环。这不是一个附加功能，而是一种**设计哲学**——**Claude Code 遵循 Unix“小工具、大组合”的传统，通过标准输入输出与其他命令行工具互联互通**。

基本管道用法如  [Anthropic 工程博客](https://code.claude.com/docs/en/best-practices)所述：

> “Claude Code 可以作为 Unix 风格的工具，允许你直接将数据管道到它（如  `cat foo.txt | claude -p "query"`），这对于处理日志或 CSV 特别有用。”

管道的核心思想是：前一个命令的输出，成为后一个命令的输入。当 Claude Code 站在管道中间时，它接收上游数据，用 AI 理解和处理这些数据，然后把结果传给下游。这意味着你**可以把 Claude 插入到任何现有的 Shell 工作流中，而不需要改变工作流的结构**。
```bash
# 分析日志文件
cat server.log | claude -p "找出所有错误并总结原因"

# 解析 JSON
curl https://api.example.com/data | claude -p "提取所有用户的邮箱地址"

# 代码转换
cat old-code.js | claude -p "将这段 JavaScript 转换为 TypeScript"
```

管道的真正威力在于**组合**。下面这些例子展示了 Claude Code 如何与  find、git、grep  等经典 Unix 工具协作。每个组合都解决了一个真实的开发场景——批量检查类型提示、总结提交变更、将散落的 TODO 转换为规范的 Issue 格式。
```bash
# 结合 find 和 xargs 批量处理
find src -name "*.py" | xargs -I {} claude -p "检查 {} 中的类型提示是否完整"

# 结合 git 工作流
git diff HEAD~1 | claude -p "总结这次提交的变更"

# 结合 grep 预过滤
grep -r "TODO" src/ | claude -p "将这些 TODO 转换为 GitHub Issue 格式"
```
![](assets/19%20Headless%20模式与%20CICD%20集成/file-20260429094941377.png)

Claude 不仅可以接收管道输入，它的输出同样可以**通过管道流向下游**。这样你就能构建完整的自动化链路：**数据获取 -> AI 分析 -> 结果处理 -> 通知或存储**。

下面的例子展示了三种典型的下游处理模式——用  jq  解析 JSON 结果、直接写入文件以及发送邮件通知。
```bash
# Claude 输出 -> jq 解析 -> 下游处理
claude -p "列出所有函数名" --output-format json | jq -r '.result' | sort | uniq

# Claude 生成代码 -> 直接写入文件
claude -p "生成一个 Express 路由处理函数" --output-format text > routes/user.js

# Claude 分析 -> 发送通知
claude -p "检查是否有安全漏洞" --output-format json | \
  jq -r '.result' | \
  mail -s "安全扫描报告" security@company.com
```


# 批量处理模式

当你需要对大量文件执行相同的 AI 分析任务时，批量处理模式就派上用场了。[SmartScope 博客](https://smartscope.blog/en/generative-ai/claude/claude-code-batch-processing/)详细介绍了这种模式：

> Claude Code 的批处理（headless 模式）允许你直接从命令行执行 AI 功能，无需使用交互式 UI。通过集成到 CI/CD 流水线和自动化脚本中，你可以高效执行大规模处理任务。


