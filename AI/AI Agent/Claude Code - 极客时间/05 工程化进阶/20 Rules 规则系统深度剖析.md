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

假设你有一个 React + Express + PostgreSQL 的全栈项目，CLAUDE.md 膨胀到了 600 行（[示例参考](https://github.com/huangjia2019/claude-code-engineering/blob/main/02-Memory/projects/03-bloated-claude-md/CLAUDE.md)）。我们如何拆分呢？

## 拆分后的 CLAUDE.md（精简到 80 行以内）
```markdown
# 项目概述
全栈 TypeScript 项目。前端 React 18 + Tailwind，后端 Express + Prisma + PostgreSQL。

# 命令
- `pnpm dev` — 启动前后端开发服务器
- `pnpm test` — 运行全部测试
- `pnpm lint` — ESLint + Prettier 检查
- `pnpm db:migrate` — 执行数据库迁移

# 核心约定
- 包管理器用 pnpm，不用 npm 或 yarn
- commit message 用 conventional commits 格式
- 所有 API 返回 { success: boolean, data?: T, error?: string }
- 环境变量通过 .env 管理，不硬编码

# 详细规范
领域规范见 .claude/rules/ 目录，按文件类型自动加载。
```

## 拆分出的 rules 文件

### `.claude/rules/frontend.md`：

```markdown
---
paths:
  - "src/components/**"
  - "src/pages/**"
  - "src/hooks/**"
---

# 前端规范

## 组件
- 函数式组件，不用 class 组件
- Props 用 interface 定义，命名 XxxProps
- 组件文件和样式文件同名同目录

## 状态管理
- 局部状态用 useState
- 跨组件状态用 Zustand
- 服务端状态用 TanStack Query

## 样式
- Tailwind 优先，复杂样式用 CSS Modules
- 响应式断点：sm(640) md(768) lg(1024) xl(1280)
```

### `.claude/rules/backend.md`：

```markdown
---
paths:
  - "server/**"
  - "src/api/**"
  - "prisma/**"
---

# 后端规范

## 路由
- RESTful 风格，资源名用复数
- 路由文件放 server/routes/，一个资源一个文件

## 数据库
- 所有查询通过 Prisma ORM，不写原生 SQL
- 迁移文件不手动编辑
- 关联查询用 include，不用多次查询

## 错误处理
- 业务错误抛 AppError(code, message)
- 统一在 errorHandler 中间件中捕获
```

### `.claude/rules/testing.md`：

```markdown
---
paths:
  - "**/*.test.ts"
  - "**/*.test.tsx"
  - "**/*.spec.ts"
---

# 测试规范

## 工具
- 单元测试：Vitest
- 组件测试：Testing Library
- E2E：Playwright

## 结构
- Arrange-Act-Assert 模式
- 每个 describe 对应一个函数或组件
- Mock 外部依赖，不 mock 内部模块

## 覆盖率
- 业务逻辑 > 80%
- 工具函数 > 90%
- UI 组件关注交互，不关注快照
```


### `.claude/rules/security.md`：
（注意，没有 paths，全局生效）
```markdown
# 安全规范

- 用户输入在使用前必须 validate + sanitize
- SQL 参数化（Prisma 默认做到了）
- XSS 防护：不使用 dangerouslySetInnerHTML
- CORS 只允许白名单域名
- 敏感信息（API Key、数据库密码）只放 .env
- 认证 token 用 httpOnly cookie，不存 localStorage
```

拆完之后，CLAUDE.md 从 600 行变成 80 行，但规范一条都没少——**只是按需加载了**。当 Claude 在改前端组件时，它看到的是 CLAUDE.md + frontend.md + security.md。当它在写测试时，看到的是 CLAUDE.md + testing.md + security.md。精准、高效。
![](assets/20%20Rules%20规则系统深度剖析/file-20260429134306644.png)

# 权限规则——行为管控的硬约束

指令规则告诉 Claude“你应该怎么做”，权限规则告诉 Claude“你被允许做什么”。

权限规则写在  .claude/settings.json  或  .claude/settings.local.json  中，由 Claude Code 客户端在工具调用前**硬拦截**。Claude 根本看不到这些规则——它只知道某个操作被允许了或被拒绝了。

## 基本结构与评估逻辑

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Read"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(curl *)",
      "Edit(.env)"
    ]
  }
}
```

**评估顺序：deny → ask → allow**。  第一个匹配的规则胜出，deny 总是优先。就算你在 allow 里写了  Bash(rm -rf * )，如果 deny 里也有这条，deny 赢。安全规则应该有最高话语权。

## 权限规则覆盖的工具范围

```markdown
内置工具的权限控制：

  Bash(command pattern)      → 控制 Shell 命令的执行
  Read(file pattern)         → 控制文件的读取
  Edit(file pattern)         → 控制文件的编辑
  Write(file pattern)        → 控制文件的创建

  WebFetch(domain:pattern)   → 控制网页抓取的域名范围
  WebSearch                  → 控制是否允许网络搜索

  mcp__server__tool          → 控制 MCP 工具的使用
  Skill(skill-name)          → 控制 Skill 的调用
  Task(agent-name)           → 控制子代理的调用
```

## 配置层级体系

权限配置可以在四个层级设置，**高优先级覆盖低优先级**。
![](assets/20%20Rules%20规则系统深度剖析/file-20260429134812971.png)
**关键规则：高层级的 deny 不可被低层级覆盖**。  如果组织策略禁止了  Bash(curl * )，项目配置和个人配置都无法解除这个限制。这是企业级安全管控的基石。

## 权限规则在扩展机制中的渗透

权限规则不仅存在于 settings.json 中，它还渗透到了 Claude Code 的各个扩展机制里。

### **Skills 中的 allowed-tools**

Skill 被触发时只能使用白名单中的工具：
```markdown
---
name: code-reviewing
description: Review code for quality and security issues
allowed-tools:
  - Read
  - Grep
  - Glob
---
```

### **Sub-Agents 中的 tools**

子代理的工具集更加严格，甚至拿不到主对话的 CLAUDE.md。
```markdown
---
name: code-reviewer
tools: Read, Grep, Glob
model: sonnet
---
```

### **Hooks 中的动态拦截**

最灵活的权限控制，可以根据动态条件决定是否放行。
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./hooks/block-dangerous.sh"
          }
        ]
      }
    ]
  }
}
```

