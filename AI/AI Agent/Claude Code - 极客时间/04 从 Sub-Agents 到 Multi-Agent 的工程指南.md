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
在 Handoffs 模式下，不同 Agent 之间通过显式的交接机制完成角色切换，上下文并非整体共享，而是可以根据需要选择性地传递。这样能在保持必要信息连续性的同时，避免无关内容的扩散。系统状态在 Agent 切换过程中被持续保存和传递，使得多阶段流程能够自然推进而不会丢失关键信息。

由于各阶段之间存在明确的先后依赖关系，该模式采用严格的顺序执行，不支持并行展开。对用户而言，Agent 的切换过程通常是透明的，用户可以像与单一 Agent 交互一样完成整个流程。

在工程调试层面，这种模式的复杂度处于中等水平，需要重点关注状态在不同阶段之间的流转路径，以便在出现异常时准确定位问题发生的环节。

Handoffs 的典型应用是客服工单流程：
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422143155236.png)
在 Claude Code 中并不存在一个底层 API 叫 handoff()， Handoffs 是通过 **Prompt + 状态约束 + 工程结构模拟出来的**。

换句话说： **Handoffs 是一种“工程模式”，不是一个“框架特性”**。

在 Claude Code 中实现 Handoffs 的三大工程要素：

1. 明确的阶段状态（State）—— 你需要显式定义流程阶段。

2. 每个阶段都是一个“角色约束的 Agent 视角”，比如：阶段一：信息收集（前台接待）；阶段二：技术诊断；阶段三：执行与修复。

3. 显式的阶段完成条件（Handoff Trigger）。这是 Handoffs 能稳定运行的核心。每个阶段都必须有完成条件（Exit Criteria）， 否则就会“卡在阶段里出不来”。

“Claude Code 风格”的 Handoffs 示例：
```markdown
系统规则：
你将按照以下阶段顺序工作：
1. 信息收集（intake）
2. 问题诊断（diagnosis）
3. 解决方案（resolution）

当前阶段：intake

规则：
- 只能提问
- 不要给解决方案
- 当信息完整时，明确声明：`进入 diagnosis 阶段`
```

当 Claude 输出：
```markdown
信息已收集完成，进入 diagnosis 阶段。
```

系统（或你自己）再注入下一段 Prompt：
```markdown
当前阶段：diagnosis
你现在是技术支持 Agent……
```

这就是一次 handoff。

Handoffs 模式最适用于具有明确阶段划分的流程型场景，例如从信息收集到问题诊断再到解决方案输出的多阶段客服或工单系统，尤其适合那些需要在满足前置条件后才能逐步解锁能力的业务流程。在多轮对话中，该模式能够自然地完成角色切换而不打断用户体验，是对话连续性要求最高的架构选择。

Handoffs 模式的严格的顺序执行限制了并行能力，在涉及多个领域或多源查询时效率最低，但在强调流程完整性和交互自然度的场景中，往往是体验最优、可控性最强的方案。

## 模式四：Router（路由器 / 并行分发与合成）

Router 模式的核心在于**对输入进行语义拆分与职责分流**。系统首先由 Router 对用户请求进行分类和分解，然后将子查询并行分发给各自负责的专业 Agent，最后再将多个结果统一合成为一个对用户友好的响应。
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422143724564.png)
这种架构天然适合处理跨多个知识域或数据源的查询，例如在企业知识库场景中，用户一次提问可能同时涉及政策文档、业务数据和实时指标，Router 可以将“退货政策”交由政策文档 Agent 处理，将“销售数据”交由数据分析 Agent 处理，并在上层完成结果整合后统一返回。
```
用户提问：「我们的退货政策是什么？最近的销售数据如何？」

Router 分解：
├── 查询 1：退货政策 → 政策文档 Agent
├── 查询 2：销售数据 → 数据分析 Agent
└── 合成结果 → 统一回答
```

在 Claude Code 中，Router 通常以下面三种形态之一存在。

1. 主 Agent 中的一段路由决策逻辑（最常见）

2. 一个可调用的 Tool（Router-as-Tool）

3. 一个轻量的 Sub-Agent（只负责分类，不负责执行）

本质都是同一件事：**先判断“这是什么问题”，再决定“交给谁处理”。**

Router 模式的工程优势在于极强的并行能力和清晰的职责边界，各处理分支彼此独立、上下文完全隔离，既有利于扩展，也便于独立观测和调试。

其代价在于该模式通常是无状态的，无法充分利用历史对话上下文来减少重复计算；在需要连续对话的场景中，往往需要将 Router 作为一个工具嵌入到有状态的主 Agent 中，以在并行效率和对话连续性之间取得平衡。

# 性能、成本、可控性的量化对比

LangChain 对这四种模式做了实际的性能量化测试，分别从单任务请求的模型调用次数、重复请求的效率，和复杂问题的 Token 消耗三个方面进行了对比，结果非常有参考价值。

## 场景一：单任务请求（如“帮我修改函数支持分页查询”）
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422144114625.png)

## 场景二：重复请求效率（第二轮相同类型的请求）
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422144154679.png)
## 场景三：多领域查询（如“对比 Python/JS/Rust 的性能”）
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422144236697.png)
比较上面几个表的结论，可以看出，简单任务中，Sub-Agent 模式有额外开销。多轮对话中，有状态模式效率优势明显。而在多领域查询中，上下文隔离的模式（Sub-Agent、Router）在 token 效率上优势显著——节省 40% 以上的 token 成本。

Anthropic 在工程博客中公开了他们的[多 Agent 研究系统的完整设计](https://www.anthropic.com/engineering/multi-agent-research-system)，其中也涉及到性能和成本的权衡。Anthropic 认为多 Agent 系统中的性能差异在很大程度上是可解释的，其中约 95% 的性能波动可以归因于三个因素：Token 使用量占据主导地位，其影响约为 80%；工具调用次数与模型选择共同贡献约 15%；其余因素的影响则相对有限。

一个关键发现是，选择更合适的模型（如 Claude Sonnet 4）所带来的性能提升，往往超过单纯将 token 预算翻倍的效果，这意味着在多 Agent 架构中，模型选型的重要性显著高于无节制地增加上下文规模。

从“Token 经济学”的角度看，多 Agent 系统普遍存在约 15 倍的 token 成本放大效应，因此只适合用于高价值、高复杂度的任务；对于需要所有 Agent 共享完整上下文的场景、强耦合且高度顺序化的工作流、大多数难以并行拆解的编码任务，以及依赖 Agent 之间实时协调的系统，多 Agent 架构往往得不偿失，反而会引入不必要的成本和复杂度。

同时，从可控性和工程调整的角度，Anthropic 也分享了它们在将多 Agent 系统推向生产时，遇到了四个关键挑战。

1. 状态性带来的复杂度。Agent 在多轮对话中维持状态，微小的失败会级联放大。一个 SubAgent 的轻微错误可能导致后续所有 Agent 的行为偏离。这种情况的应对策略是在每个 Agent 的输出端设置“检查点”，验证输出质量再传递。

2. 非确定性调试。Agent 的动态决策使得传统的日志分析不够用。你需要完整的生产链路追踪（Production Tracing），记录每个 Agent 的输入、决策过程和输出。可以引入 Observability 工具，记录完整的 Agent 调用链。

3. 部署复杂度。多 Agent 系统的部署不能简单地“停机更新”。因为 Agent 可能正在执行中，打断它会导致不可预测的行为。可以考虑采用新旧版本共存迁移的渐进式部署策略（Rainbow Deployment），让旧版本的 Agent 完成当前任务后自然退出，新版本接管后续请求。

4. 同步瓶颈。当前大多数 SubAgent 是同步执行的，SubAgent 之间的信息流受限。未来的方向是打通异步执行 + Agent 间消息通道，让 SubAgent 在执行过程中可以相互共享发现。


# 从 Sub-Agent 到 Multi-Agent 的架构演进路径

理解了四种模式，并且清晰的理解了各种模式的性能、成本、可控性差异后，让我们看看一个项目的 Agent 架构通常如何演进。

首先给出一个升级决策树，也就是先回答这个问题——我的项目或者说任务是不是已经复杂到需要引入多 Agent 架构的程度了。
```markdown
你的任务需要多 Agent 吗？
├─ 单一领域、工具 < 5 个、上下文 < 50K tokens
│  └─→ 不需要。用单 Agent + 好的 prompt 即可
│
├─ 单一领域、但工具 > 10 个
│  └─→ 考虑 Skills 模式（渐进式能力加载）
│
├─ 多领域、各领域需要独立上下文
│  └─→ 使用 Sub-Agents 模式
│
├─ 需要多步骤状态流转（如客服工单流程）
│  └─→ 使用 Handoffs 模式
│
└─ 需要跨多个数据源并行查询
   └─→ 使用 Router 模式
```

下面是一个典型的项目架构演进路径。
## 第一阶段：单 Agent + Tools

适合大多数初期场景。不要过早引入多 Agent。
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422145050912.png)
## 第二阶段：单 Agent + Skills

当工具数量增多、prompt 变得臃肿时，用 Skills 实现渐进式加载。
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422145136669.png)
## 第三阶段：Supervisor + Sub-Agents

当不同领域需要独立的上下文空间和专业知识时引入。
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422145159671.png)
## 第四阶段：混合架构

成熟系统中，不同类型的任务流可能采用不同的模式。Router 处理分类，Sub-Agent 处理并行研究，Handoff 处理顺序流程。
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422145225273.png)
个人的项目实践中，我一般上来先做简单 Demo，不用什么设计模式，SubAgent 和 Skills，到了两三个礼拜后，感觉认知过载了，有点吃不消了，我才开始考虑上面的架构决策树。这是我个人习惯，你也可以在项目一开始就开始全局性的考量，根据具体项目性质和任务的复杂度而定，对整体架构进行详细的设计和规划。

# 总结

模式选择速查表
![](assets/04%20从%20Sub-Agents%20到%20Multi-Agent%20的工程指南/file-20260422145355753.png)
从单一 Agent 到复杂智能体系统设计的一系列黄金法则：
```

```