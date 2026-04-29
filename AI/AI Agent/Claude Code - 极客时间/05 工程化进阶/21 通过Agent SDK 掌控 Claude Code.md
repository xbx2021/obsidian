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
```markdown
env: 
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

