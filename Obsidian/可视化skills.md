https://github.com/axtonliu/axton-obsidian-visual-skills/blob/main/README_CN.md
让 Claude Code 在 Obsidian 里生成 Canvas / Excalidraw / Mermaid 的可视化三件套。

### 安装步骤（Windows）

1. 先装好：Obsidian + Excalidraw 插件 + Claude Code CLI
2. 下载技能包：
```bash
git clone https://github.com/axtonliu/axton-obsidian-visual-skills.git
```
3. 复制到 Claude 技能目录：
```bash 
# 复制3个核心技能
cp -r axton-obsidian-visual-skills/excalidraw-diagram ~/.claude/skills/
cp -r axton-obsidian-visual-skills/mermaid-visualizer ~/.claude/skills/
cp -r axton-obsidian-visual-skills/obsidian-canvas-creator ~/.claude/skills/
```
4. 重启 Claude Code，触发关键词：`Canvas`、`mind map`、`Excalidraw`、`Mermaid`、`visual diagram`

## 包含的 Skills
### 1. Excalidraw 图表生成器

生成手绘风格图表，支持三种输出模式：

| 模式               | 输出            | 用途                                                                         |
| ---------------- | ------------- | -------------------------------------------------------------------------- |
| **Obsidian**（默认） | `.md`         | 在 Obsidian 中直接打开                                                           |
| **标准**           | `.excalidraw` | 在 excalidraw.com 打开/编辑/分享                                                  |
| **动画**           | `.excalidraw` | 用 [excalidraw-animate](https://dai-shi.github.io/excalidraw-animate/) 生成动画 |

**支持的图表类型：**

| 类型       | 适用场景             |     |
| -------- | ---------------- | --- |
| **流程图**  | 步骤说明、工作流程、任务执行顺序 |     |
| **思维导图** | 概念发散、主题分类、灵感捕捉   |     |
| **层级图**  | 组织结构、内容分级、系统拆解   |     |
| **关系图**  | 要素之间的影响、依赖、互动    |     |
| **对比图**  | 两种以上方案或观点的对照分析   |     |
| **时间线图** | 事件发展、项目进度、模型演化   |     |
| **矩阵图**  | 双维度分类、任务优先级、定位   |     |
| **自由布局** | 内容零散、灵感记录、初步信息收集 |     |

**核心特性：**

- 三种输出模式适应不同场景
- 手绘美学风格，使用 Excalifont（fontFamily: 5）
- 完美支持中文，正确处理特殊字符
- 动画支持，可自定义元素出现顺序

**触发词：**

- Obsidian：`Excalidraw`、`画图`、`流程图`、`思维导图`
- 标准：`标准Excalidraw`、`standard excalidraw`
- 动画：`Excalidraw动画`、`动画图`、`animate`

### 2. Mermaid 可视化器

将文本内容转换为专业的 Mermaid 图表，适用于演示和文档。内置语法错误预防机制，避免常见陷阱。

**支持的图表类型：**

- **流程图** (graph TB/LR) - 工作流、决策树、AI Agent 架构
- **循环图** - 迭代过程、反馈循环、持续改进
- **对比图** - 前后对比、A vs B 分析、传统 vs 现代
- **思维导图** - 层级概念、知识组织
- **时序图** - 组件交互、API 调用、消息流
- **状态图** - 系统状态、状态转换、生命周期

**核心特性：**

- 内置语法错误预防（列表冲突、子图命名、特殊字符）
- 可配置布局：垂直/水平、简洁/标准/详细
- 语义化配色方案
- 兼容 Obsidian、GitHub 等 Mermaid 渲染器

**触发词：** `Mermaid`、`可视化`、`流程图`、`时序图`、`visualize`

### 3. Obsidian Canvas 创建器

创建交互式 Obsidian Canvas（`.canvas`）文件，支持思维导图和自由布局。输出有效的 JSON Canvas 格式，可直接在 Obsidian 中打开。

**布局模式：**

|模式|结构|适用场景|
|---|---|---|
|**思维导图**|从中心向外的放射状层级|头脑风暴、主题探索、层级内容|
|**自由布局**|自定义位置、灵活连接|复杂网络、非层级内容、自定义排列|

**核心特性：**

- 根据内容长度智能调整节点大小
- 自动创建带标签的关系连线
- 颜色编码节点（6 种预设颜色 + 自定义 hex）
- 合理的间距算法，防止节点重叠
- 支持节点分组，增强视觉组织

**触发词：** `Canvas`、`思维导图`、`可视化图表`、`mind map`
## 使用方法
```
# Excalidraw
"创建一个展示 CI/CD 流程的 Excalidraw 流程图"
"画一个关于机器学习概念的思维导图"
"用 Excalidraw 画一个商业模式关系图"

# Mermaid
"用 Mermaid 图表可视化这个流程"
"为 API 认证流程创建时序图"
"把这个工作流程转成 Mermaid 图表"

# Canvas
"把这篇文章转换成 Obsidian Canvas"
"创建一个项目规划的思维导图 Canvas"
"把这篇文章整理成 Canvas 思维导图"
```
