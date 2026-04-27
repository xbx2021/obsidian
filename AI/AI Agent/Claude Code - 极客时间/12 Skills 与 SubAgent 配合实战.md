# 两个组合方向：谁包含谁

**Skills 解决的是“怎么做”的问题，本质是知识注入**——它让同一个 Agent 学会新的能力，就像给一个员工发了一本操作手册，员工还是那个人，只是掌握了更多方法与规范。

**SubAgents 解决的是“谁来做”的问题，本质是任务委托**——它创建一个独立的执行者去完成某件事，就像把任务交给另一位同事，对方拥有自己的上下文、职责边界和决策空间。
![](assets/12%20Skills%20与%20SubAgent%20配合实战/file-20260427092241178.png)

当你犹豫到底是用 Skill 还是用 SubAgent 的时候，做出选择的核心判断标准在于：**这件事到底需要“另一个人”来承担，还是只需要“多一本手册”来指导？**

而更常见的情况是：结合起来使用。当你把两者组合时，本质上只有两个原子方向——**是 SubAgent 内部加载 Skills，还是由主 Agent 通过 Skills 去编排和调用 SubAgents。**


## 方向 A：SubAgent 包含 Skill（skills  字段）

此时，你定义子代理的角色，通过  skills  字段给它预加载领域知识。**SubAgent 是老板，Skill 是工具书。**
```markdown
# .claude/agents/api-doc-generator.md
---
name: api-doc-generator
description: Generate API documentation by scanning Express route files.
tools: [Read, Grep, Glob, Write, Bash]
skills:
  - api-generating           # ← 关键：预加载 Skill 作为领域知识
---

You are an API documentation specialist.

## Your Mission
Generate or update API documentation for Express.js routes.
```

这种情况下，Claude Code 的执行流程如下：
```markdown
Claude 主对话: "用 api-doc-generator 为 src/ 生成 API 文档"

主对话                              SubAgent (api-doc-generator)
  │                                    │
  ├─ 创建子代理 + 注入 Skill ──────→     │
  │                                    ├─ 上下文中已有：角色定义 + SKILL.md全文
  │                                    ├─ 按 SKILL.md 步骤执行任务
  │                                    ├─ 使用 Skill 提供的脚本和模板
  │                                    ├─ 生成文档
  │  ←──── 返回结果摘要 ────────────     │
  ├─ 继续对话                          （子代理结束）
```
SubAgent 包含 Skill 是最常见的情况，适用场景包括子代理需要特定领域的专业知识来完成任务，同一个 Skill 可以被不同角色的 SubAgent 复用，以及需要长期维护的专家型 Agent。

## 方向 B：Skill 包含 SubAgent（context: fork）

在这种情况下，Skill 自带任务指令，通过  context: fork  配置自动“派遣”一个子代理去执行。**Skill 是老板，SubAgent 是执行者。**
```markdown
---
name: deep-research
description: Research a topic thoroughly in the codebase
context: fork           # ← 关键：让 Skill 在独立子代理中执行
agent: Explore          # ← 子代理类型
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

此时的 Claude Code 执行流程如下：
```
用户: /deep-research authentication flow

主对话                              子代理（Explore）
  │                                    │
  ├─ 创建隔离上下文 ────────────────→ │
  │                                    ├─ 收到任务："Research authentication flow..."
  │                                    ├─ Glob/Grep 搜索相关文件
  │                                    ├─ Read 分析代码
  │                                    ├─ 生成结构化摘要
  │  ←──── 返回结果摘要 ──────────── │
  ├─ 继续对话（上下文干净）            （子代理结束）
```
子代理看不到你之前的对话历史，因此 SKILL.md 的内容成为子代理的任务指令。agent  字段决定子代理类型：Explore（只读探索）、Plan（规划）、general-purpose（通用，省略  agent  时默认使用)。

这种应用方式的适用场景是**研究型任务**（深度探索代码库，不污染主对话），**重型生成**（批量生成文档，中间过程不需要用户看到），以及**安全隔离**（Skill 的操作不应影响主对话状态）。
![](assets/12%20Skills%20与%20SubAgent%20配合实战/file-20260427093318140.png)

下面是两个方向的对照说明表。
![](assets/12%20Skills%20与%20SubAgent%20配合实战/file-20260427093328639.png)
![](assets/12%20Skills%20与%20SubAgent%20配合实战/file-20260427093515602.png)

# 构建 Skill：参照着用

这个配套项目位于：04-Skills/projects/05-api-generator/

一个生产级的 Skill 的完整架构应该包含这些组件：
```markdown
.claude/skills/api-generating/          # 标准 Skill 目录
├── SKILL.md                            # 入口：路由 + 核心逻辑
├── PATTERNS.md                         # 知识：框架识别模式
├── STANDARDS.md                        # 规范：文档编写标准
├── EXAMPLES.md                         # 示例：输入输出案例
├── templates/
│   ├── index.md                       # 模板：API 索引页
│   ├── endpoint.md                    # 模板：端点文档
│   └── openapi.yaml                   # 模板：OpenAPI 规范
└── scripts/
    ├── detect_routes.py               # 脚本：路由检测
    └── validate_openapi.sh            # 脚本：规范验证
```

每个组件都有明确的职责。
![](assets/12%20Skills%20与%20SubAgent%20配合实战/file-20260427094000913.png)
也许你觉得只不过设计个 API 而已，为什么需要这么多组件？

但其实一位 API 文档专家，当有人请你写文档时，你需要：
**识别技术栈**（Express? FastAPI? Spring?）→ PATTERNS.md、

**遵循规范**（字段命名、格式要求）→ STANDARDS.md、

**参考案例**（不确定时看例子）→ EXAMPLES.md、

**使用模板**（保证一致性）→ templates/、

**批量处理**（几十个端点不可能手写）→ scripts/。

