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


## 什么是 Harness？
Anthropic 官方文档里是怎么说的：
	Claude Code serves as the agentic harness around Claude: it provides the tools, context management, and execution environment that turn a language model into a capable coding agent.

Claude Code 是一个**智能体编排框架**，包裹在 Claude 模型外面。它提供工具、上下文管理和执行环境，把一个语言模型变成一个有能力的编码 Agent。

这个定义里有三个关键词，**工具、上下文管理、执行环境**。模型本身只会生成文本。是 Harness 给了它读文件的能力、写代码的能力、搜索代码库的能力、在终端执行命令的能力。没有 Harness，Claude 就是一个只会说话的大脑——有智力，没有手脚。

![](assets/Claude%20Code%20-%20极客时间/file-20260421103236177.png)

**Harness 的内部结构拆解**
![](assets/Claude%20Code%20-%20极客时间/file-20260421103434707.png)


**Agent = Model + Harness。**  图中最核心的位置是  Model——那个蓝色芯片图标，代表 Claude 的大语言模型。但模型本身只是一个推理引擎，它不能独立行动。

