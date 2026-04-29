上一讲我们学习了 Headless 模式，让 Claude Code 在无人值守的情况下嵌入 CI/CD 流水线自动运行。Headless 解决了没有人盯着的问题，但也让一个追问变得更加尖锐，**没人盯着的时候，谁来定规矩？**

这就引出了今天的主题——**规则系统**。

# 两种规则，两个世界

Claude Code 中的“规则”分布在两个完全不同的层面：
![](assets/20%20Rules%20规则系统深度剖析/file-20260429113001710.png)
我用一个比喻来帮你区分它们，指令规则像公司的员工手册，写着“代码提交前必须跑测试”，员工可以遵守，也可以偷懒。权限规则像门禁系统——没有卡就进不了机房，系统不给你选择。
![](assets/20%20Rules%20规则系统深度剖析/file-20260429113124632.png)

**指令规则是 Claude 的认知约束，权限规则是客户端的行为约束。**
![](assets/20%20Rules%20规则系统深度剖析/file-20260429113242155.png)

# 指令规则——.claude/rules/ 完全指南

## 它到底是什么？

`.claude/rules/`  目录下的每个  .md  文件，本质上就是一段会被注入 System Prompt 的文本。**它和 CLAUDE.md 没有本质区别——都是 Claude 在每轮 API 调用中“看到”的指令**。**唯一的结构化优势是，它可以按主题拆分成多个文件，还支持条件加载**。
```markdown
.claude/
└── rules/
    ├── typescript.md       # TypeScript 编码规范
    ├── testing.md          # 测试规范（有 paths 条件）
    ├── api-design.md       # API 设计规范（有 paths 条件）
    └── security.md         # 安全规范（全局生效）
```

## 两种加载模式

这是 rules 最重要的设计细节，也是最多人搞错的地方。

### **模式一：全局加载（无 paths** 字段）
```markdown
# security.md —— 没有 YAML 头部，或有头部但不含 paths

## 安全规范
- 不在代码中硬编码密码或 API Key
- 所有用户输入必须做 sanitize
- SQL 查询使用参数化，不拼接字符串
```

这种 rule 在会话启动时就加载进上下文，行为和写在 CLAUDE.md 里完全一样。拆出来的唯一好处是文件组织更清晰。


### **模式二：条件加载（有 paths 字段）**
```markdown
---
paths:
  - "src/**/*.test.ts"
  - "tests/**/*.ts"
---

# 测试规范

## 命名
- 单元测试: `*.test.ts`
- 集成测试: `*.integration.test.ts`

## 结构
使用 Arrange-Act-Assert 模式
```

这种 rule **在会话启动时不加载**。只有当 Claude 读取或编辑匹配  `paths`  模式的文件时，才会被注入上下文。

这个设计很精妙——如果你的测试规范有 50 行，而你这次只是在改一个 CSS 样式，那这 50 行规范就不会浪费上下文空间。

但有一个关键细节，**一旦加载，就不会卸载**。paths 控制的是何时加载，不是何时生效。如果你在会话中先编辑了一个测试文件，testing.md 被加载了，然后你去改 CSS，testing.md 仍然在上下文里。
```markdown
会话开始
  → 加载全局 rules（无 paths 的）
  → testing.md 未加载 ✗

用户：帮我改一下 src/utils/format.ts
  → Claude 读取 format.ts
  → paths 不匹配，testing.md 仍未加载 ✗

用户：帮我给这个函数写个测试
  → Claude 创建 src/utils/format.test.ts
  → paths 匹配！testing.md 加载 ✓

用户：再帮我改一下 CSS
  → Claude 读取 styles.css
  → testing.md 仍在上下文中 ✓（不会卸载）
```



# 什么时候该从 CLAUDE.md 拆到 rules？

判断标准很简单，我们可以根据长度决策。
```markdown
CLAUDE.md 的总长度如何？
│
├── < 200 行 → 不用拆，CLAUDE.md 一把梭
│               简单就是好，不要为了组织而组织
│
├── 200-500 行 → 考虑拆
│   │
│   └── 有没有"只和特定文件类型相关"的内容？
│       ├── 有 → 拆出来，加 paths
│       │       （如测试规范、前端规范、API 规范）
│       └── 没有 → 拆出来，不加 paths
│                 （纯粹为了文件组织清晰）
│
└── > 500 行 → 必须拆
                CLAUDE.md 太长会稀释重要信息的权重
                把领域规范拆到 rules，CLAUDE.md 只留核心约定
```


# 实战：一个全栈项目的 rules 拆分

假设你有一个 React + Express + PostgreSQL 的全栈项目，CLAUDE.md 膨胀到了 600 行（示例参考）。我们如何拆分呢？
