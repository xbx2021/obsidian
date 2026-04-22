# 何时该升级到多 Agent？

在 AI Agent 的工程实践中，有一个经典的误区——**过早引入多 Agent 架构**。

LangChain 在其架构选型指南中给出了明确建议：
	“Start with a single agent. Add tools before adding agents. Graduate to multi-agent patterns only when encountering clear architectural limits.” （先从单 Agent 起步，优先通过引入工具扩展能力； 只有当系统确实触及单 Agent 的架构边界时， 才考虑采用多 Agent 的设计模式。）

这不是保守，而是工程智慧。每增加一个 Agent，你就增加了一层调试复杂度、一份 token 成本、和一个潜在的失败点。但当你的任务真的跨越了单 Agent 的能力边界时，正确的多 Agent 架构会带来巨大性能提升——Anthropic 的多 Agent 研究系统在内部评测中，比单 Agent Claude Opus 4 性能提升了 90.2%。

## 两个核心触发条件

LangChain 在 Choosing the Right Multi-Agent Architecture 这篇文章中总结了两个让多 Agent 成为必要选择的工程信号。

### **信号一：上下文管理挑战**

当多个能力领域的专业知识无法舒适地塞进单一 prompt 中时——你需要**策略性地分发上下文**，而不是把所有东西堆在一起。当 Agent 的上下文窗口接近满载时，模型在任务完成上的表现会显著下降，进入所谓的  dumb zone（迟钝区）。

### **信号二：分布式开发需求**

当多个团队需要**独立拥有和维护**各自的 Agent 能力时。比如安全团队维护审计 Agent，测试团队维护测试 Agent，各团队可以独立迭代而不互相干扰。
```markdown
单 Agent 的困境：
┌─────────────────────────────────────────────────┐
│ System Prompt:                                  │
│   - 你是代码专家（200行指令）                    │
│   - 你也是测试专家（150行指令）                  │
│   - 你还是安全审计专家（180行指令）              │
│   - 你同时是文档撰写专家（100行指令）            │
│   ...                                           │
│   Token 爆炸，模型注意力分散                     │
└─────────────────────────────────────────────────┘
```

# 四种核心设计模式
综合 LangChain（这是下面 4 种多智能体模式的主要来源）、Anthropic、Google 和 OpenAI 等前沿公司的最佳实践，多 Agent 系统可以归纳为四种核心架构模式。它们不是互斥的——实际项目中经常组合使用。

## 模式一：Sub-Agents（子代理委派 / 集中式编排）

Sub-Agents 的核心设计思想是一个 Supervisor Agent 充当老板，将任务分解后委派给专门的 Sub-Agent。每个 Sub-Agent 解决一个特定的任务。
![](assets/03%20子代理Sub-Agents/file-20260422142730810.png)
在 Sub-Agent 架构中，上下文隔离能力非常强，每个 Sub-Agent 都拥有独立的上下文窗口，从根本上避免了信息相互污染。Sub-Agent 本身通常设计为无状态组件，专注于完成被委派的单次任务，而整体对话状态与流程控制则由 Supervisor 统一维护。

这种结构天然支持并行执行，多个 Sub-Agent 可以同时展开工作，从而显著提升复杂任务的吞吐效率。用户并不直接与各个 Sub-Agent 交互，而是始终通过 Supervisor 间接沟通，由其负责任务拆解、结果汇总与最终输出。

在调试和可控性层面，该模式的复杂度处于中等水平，工程上需要重点关注 Supervisor 的委派逻辑与决策路径，以便在出现偏差时能够准确定位问题来源。
```markdown
# Claude Agent SDK 中的 Sub-Agent 定义（概念示例）
subagent_config = {
    "name": "research-agent",
    "description": "Research specific topics by searching the web. "
                   "Use when user asks factual questions requiring "
                   "up-to-date information.",
    "system_prompt": "You are a research specialist...",
    "tools": ["WebSearch", "WebFetch", "Read"],
    "model": "sonnet"  # 用更快的模型降低成本
}
```

Claude Code 中内置就有很多子代理（Explore、Plan、General-purpose），非常容易实现这种架构。

在 Anthropic 的真实生产系统中，[Research](https://www.anthropic.com/engineering/multi-agent-research-system) 功能采用的就是一种典型的 Sub-Agent 架构。

Anthropic 的 Research 功能采用了经典的 Sub-Agent 模式：
1. LeadResearcher（Claude Opus 4）分析查询、制定策略
2. 并行派出  3-5 个 SubAgent（Claude Sonnet 4），各自独立搜索
3. 每个 SubAgent 执行 3+ 个并行工具调用
4. CitationAgent  处理引用和来源归属
5. 结果汇聚回 LeadResearcher 综合输出

工程评测显示，并行化的 Sub-Agent 执行方式可将复杂查询的整体研究时间最多缩短约 90%，但其代价是相较普通对话约 15 倍的 token 消耗；在高价值研究任务中，这一成本换来了高达 90.2% 的整体性能提升。
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422142736574.png)

为了在不同复杂度任务中控制资源消耗，Anthropic 在 Prompt 层引入了明确的“努力分配规则（Effort Scaling）”，例如对简单问题仅启用单个 Agent 和有限次数的工具调用，而在复杂研究场景下则调度更多 Sub-Agent 全面并行执行。
```markdown
简单查询：1 个 Agent，3-10 次工具调用
中等研究：3-5 个 SubAgent，各 3+ 次并行工具调用
复杂研究：10+ 个 SubAgent，全面并行执行
```

这一架构特别适用于需要并行检索多个信息源、跨多个知识领域协同工作的研究系统，个人助手协调日历、邮件、CRM 等，同时也通过上下文隔离显著降低了信息串扰和泄漏风险。

不过，因为在每次交互中都会引入额外的模型调用和结果回传过程，Sub-Agent 架构会增加一定的延迟和 token 成本，但换来的则是更强的集中控制能力和可预测的工程行为。

## 模式二：Skills（技能 / 渐进式能力加载）

LangChain 把 Skills 也视为一种多智能体模式。其实此时仍然是单个 Agent（或 SubAgent），但**通过 SKILL.md 文件（或类似配置）实现能力的渐进式加载**。Agent 一开始只知道技能的名称和描述，当判断需要某个技能时，才加载完整的指令。

这是一种“准多 Agent”方案——用更轻量的 prompt 切换替代完整的 Agent 切换。
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422142736554.png)
在 Skills 模式下，系统仍然由单一 Agent 负责全部推理与执行，所有技能共享同一个上下文窗口，因此在上下文隔离能力上相对较弱，但换来的好处是对话状态可以自然连续地保留在同一个 Agent 内部，无需额外的状态协调机制。

由于不存在多个 Agent 的并行调度，整体执行过程以顺序方式展开，并行能力相对有限，但在多数交互式场景下已经足够。用户始终与同一个 Agent 直接交互，交互路径最短，体验也最为流畅。
```markdown
.claude/skills/           
├── deploy/
│   └── SKILL.md          # 部署技能的完整指令
├── review-pr/
│   └── SKILL.md          # PR 审查技能的指令
└── database-migration/
    └── SKILL.md          # 数据库迁移技能的指令
```

在 Claude Code 的配置中，每个 SKILL.md 包含 YAML frontmatter（元数据）和详细的步骤指令：
```markdown
---
name: deploy
description: "Deploy application to production environment"
allowed-tools: ["Bash", "Read", "Edit"]
---

## 部署步骤

1. 检查当前分支是否为 main
2. 运行完整测试套件
3. 构建生产版本
4. 执行部署脚本
5. 验证部署结果
```

Skills 模式特别适合那些能力种类繁多、但单次任务只需要调用少量能力的场景，例如需要同时支持十余种操作模式的编码助手，或在写作、设计、排版等多种创意形态之间切换的创意工具。在这类系统中，Agent 可以在保持连续对话体验的前提下，按需加载对应技能，避免在一开始就引入过多指令。

这种模式的复杂度最低，执行路径清晰、因果关系明确，非常适合早期系统，在需要频繁迭代的情况下，能快速定位问题。其工程代价在于，对话上下文会随着历史交互逐步累积，后续调用的 token 成本可能持续膨胀；但相应地，这种模式在首次调用时几乎没有额外调度开销，响应延迟最低，同时也为用户提供了最自然、最直观的交互体验。

概括 Skills 模式与 Sub-Agent 模式的关键区别：
```markdown
Sub-Agent：独立的上下文 → 适合大量信息过滤
Skill：共享的上下文 → 适合需要连贯对话的场景
```

## 模式三：Handoffs（交接 / 状态驱动的 Agent 切换）

Handoffs 的核心思想是活跃的 Agent 根据对话状态动态切换。Agent A 完成自己的阶段后，通过调用  handoff()  工具将控制权（和上下文）传递给 Agent B。
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422143024968.png)

