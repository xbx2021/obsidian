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
![](assets/03%20-%20子代理Sub-Agents/file-20260422135758784.png)
