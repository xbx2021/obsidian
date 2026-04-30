至此你基本上已经掌握了 Claude Code 全局的方方面面。而上两讲我们又通过 Agent SDK，先用 Python/TypeScript 代码驱动 Claude 执行任务，再深入探索了多轮对话和流式处理等高级模式。此时此刻，你已经掌握了从交互式使用到代码驱动的全部能力。

最后，还剩下一个问题我们还没有回答，**这些能力怎么传递给别人？**（课程群用户也提到了工作场景中这类困惑“我项目很多同事在维护， 一人好几个 Skill，工作流除了他们自己知道怎么用，别人都不知道”。）

你写了一个好用的  `/review`  命令，同事想用，你说“把这个文件复制到  `.claude/commands/`  下面”。你配了一个安全扫描代理，新人想用，你说“把  `agents/ ` 目录拷过去，然后再配一下 MCP 服务器”。你设了一套 Hooks 自动格式化，团队想统一，你说“把  `settings.json`  里的 hooks 配置合并进去”。

一个两个还行，十个八个就乱了。文件散落在各处，版本无法追踪，配置因人而异。**你从独行侠变成了布道者，但效率反而更低了**。这就是本讲要解决的问题。插件系统让你把所有的工具、命令、配置、规范打包成一个整体。新人入职时，只需要一条命令：
```
/plugin install @our-company/dev-toolkit
```

数据库连接、测试命令、代码审查规范、Git 工作流全部就位。**30 分钟的入职培训变成了 30 秒的安装命令。**

这就是插件的终极价值，**把知识变成资产，把重复变成复用，把个人经验变成团队能力**。

# 理解插件：Claude Code 的“应用商店“

如果说 Claude Code 是一把瑞士军刀，那么**插件就是可以插拔的工具模块**。插件是一种轻量级的打包和分享方式，可以组合斜杠命令、子代理、MCP 服务器和 Hooks。你可以用一条命令安装插件，在终端和 VS Code 中都能使用。

一个插件可以包含以下五类组件，每一类我们在前面的课程中都已经深入学习过。
![](assets/23%20Plugins%20插件打包与分发/file-20260430154726779.png)
插件的价值不在于它引入了新的机制，而在于它提供了一个标准化的打包和分发方式。你在前 20 讲里学到的所有扩展能力，都可以通过插件系统组合、封装、传递给他人。

在没有插件之前，团队协作依赖的是文档、脚本和口耳相传。让我们对比一下这两种方式的差异。
![](assets/23%20Plugins%20插件打包与分发/file-20260430154903422.png)
手动配置的根本问题不是麻烦——麻烦只是表象。**根本问题是不一致**。当 15 个人各自配置时，你得到的是 15 种微妙不同的开发环境。插件把“约定”变成了“约束”，从“应该这样做“变成“只能这样做”。

根据  [Claude Plugins 社区](https://claude-plugins.dev/)的统计，目前已有超过 10,000 个插件和 50,000 个 Agent Skills 可供使用。插件来源包括三个层级。

1. **官方市场**：Anthropic 维护的  [claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
2. **社区市场**：开发者贡献的公开插件
3. **企业市场**：公司内部的私有插件

![](assets/23%20Plugins%20插件打包与分发/file-20260430155205827.png)

有人说，Claude Code 的插件市场就像是 AI 辅助开发工作流的 npm。去中心化的来源，任何人都可以托管市场，一条命令安装。这个类比非常精准。npm 改变了 JavaScript 生态的协作方式，让开发者不再重复造轮子。Claude Code 的插件系统正在对 AI 辅助开发做同样的事情，把个人的最佳实践变成社区的公共资产。

# 插件的目录结构

根据[官方文档](https://code.claude.com/docs/en/plugins)，插件的标准结构如下。理解这个结构是创建插件的第一步，因为 Claude Code 依赖固定的目录约定来发现和加载各类组件：
```markdown
my-plugin/
├── .claude-plugin/
│   └── plugin.json        # 插件元数据（必需）
├── commands/              # 斜杠命令（可选）
│   ├── review.md
│   └── deploy.md
├── agents/                # 子代理（可选）
│   ├── security-scanner.md
│   └── code-reviewer.md
├── skills/                # Agent Skills（可选）
│   └── react-patterns/
│       └── SKILL.md
├── hooks/                 # Hooks 配置（可选）
│   └── hooks.json
├── .mcp.json              # MCP 服务器配置（可选）
└── README.md              # 插件文档
```

**咖哥发言**：只有  `plugin.json`  放在  `.claude-plugin/`  目录内，其他所有目录（commands、agents、skills、hooks）都在插件根目录下。注意不要把 commands 等目录也放进  `.claude-plugin/`  里。

## plugin.json：插件的身份证

每个插件必须有  .claude-plugin/plugin.json  文件。这个文件的作用类似于 npm 的  package.json——它定义了插件的身份、版本和描述信息，是 Claude Code 识别和管理插件的唯一入口：
```json
{
  "name": "team-toolkit",
  "version": "1.0.0",
  "description": "团队标准开发工具包：代码审查、测试、部署一体化",
  "author": "DevOps Team",
  "repository": "https://github.com/our-company/team-toolkit",
  "license": "MIT",
  "keywords": ["team", "devops", "workflow", "code-review"]
}
```

各字段的含义和说明如下表。
![](assets/23%20Plugins%20插件打包与分发/file-20260430155739180.png)
![](assets/23%20Plugins%20插件打包与分发/file-20260430155754177.png)


## 添加斜杠命令

命令是插件中用户感知最直接的组件。在  `commands/ ` 目录下创建 Markdown 文件，文件名（不含  .md）即为命令名。命令文件的格式与我们在第 10 讲中学习的 Slash Commands 完全一致，frontmatter 定义元数据，正文定义行为指令。

**commands/review.md**
```markdown
---
name: review
description: 对当前文件或目录进行代码审查
---

当用户运行 `/review [target]` 时，执行代码审查。

## 审查流程

1. 如果指定了 target，审查该文件或目录
2. 如果没有指定，审查当前打开的文件
3. 如果没有上下文，询问用户

## 审查要点

- 代码质量：命名规范、DRY 原则、复杂度
- 潜在 Bug：边界条件、空值处理、类型错误
- 安全问题：输入验证、敏感数据、注入风险
- 性能问题：不必要的循环、内存泄漏
- 最佳实践：框架惯例、设计模式

## 输出格式

```markdown
## 代码审查报告

**文件**: {file_path}
**审查时间**: {timestamp}

### 发现的问题

🔴 **严重** (必须修复)
- [问题描述] (行号)

🟡 **警告** (建议修复)
- [问题描述] (行号)

🔵 **建议** (可选改进)
- [问题描述] (行号)

### 总结

[1-2 句总结]
```

安装插件后，命令会带上插件名称作为**命名空间**，避免不同插件的命令冲突。这个机制与编程语言中的模块命名空间是同一个思路。

- 插件名：team-toolkit
- 命令文件：commands/review.md
- 实际命令：/team-toolkit:review

如果只有一个命令或命令名唯一，也可以直接用  `/review`。Claude Code 会自动解析，优先匹配唯一命令名。

命令可以接受**参数**，使用  `$ARGUMENTS`  占位符接收用户输入。在 Markdown 中说明参数格式，让 Claude 知道如何解析。下面这个 TODO 命令展示了如何设计一个支持优先级和指派人的参数化命令：

**commands/todo.md**
```markdown
---
name: todo
description: 添加 TODO 注释，支持优先级和指派人
---

用法：`/todo [优先级] [消息] [@指派人]`

## 参数

- `优先级`（可选）：
  - `!` 或 `high` → 高优先级
  - `?` 或 `discuss` → 待讨论
  - 默认 → 普通优先级

- `消息`：TODO 的内容

- `@指派人`（可选）：指定负责人

## 示例
/todo 修复登录验证 → // TODO: 修复登录验证
/todo ! 紧急修复安全漏洞 → // TODO [HIGH]: 紧急修复安全漏洞
/todo ? 是否需要缓存 @john → // TODO [DISCUSS @john]: 是否需要缓存

## 行为

1. 自动检测当前文件的语言，使用正确的注释格式
2. 插入到光标位置或相关代码附近
3. 如果没有文件上下文，询问位置
```