---
title: "Claude Skills： 从指令到资产的系统化构建指南"
source: "https://www.axtonliu.ai/newsletters/ai-2/posts/claude-agent-skills-maps-framework"
author:
  - "[[重构个体：AI时代如何打造个人竞争力]]"
published: 2026-01-01
created: 2026-04-16
description: "深度拆解 Claude Agent Skills 的本质、架构与渐进式披露机制，对比 MCP、Subagent 与 Project，结合 MAPS 与 5A+ 方法论，示范能力包型和软编排型 Skills，帮你把隐性知识资产化，构建可复用的 AI 工作流与工程化系统。"
tags:
  - "clippings"
---
## Claude Skills： 从指令到资产的系统化构建指南 | AI 精英周刊 030

> Claude Agent Skills 的核心价值在于把隐性知识显性化、模块化、资产化。通过渐进式披露机制，Skills 实现了「入门极简、上限极高」的平衡——启动时只加载名称和描述（约 100 Token），按需加载完整指令和参考资料。本文用 MAPS 框架深度拆解能力包型和软编排型两种 Skills 设计模式，并提供从想法到落地的 5A+ 方法论完整闭环。

我本职是一个研究型的创作者，平时主要做的就是 AI 工作流以及系统化应用这一块。简单说，我主要做两件事：一是研究人和 AI 的协作，尤其是让 AI 在关键的问题上、关键的步骤上来输出可靠的结果；二是用 MAPS 来帮大家把零零散散用 AI 的经验变成一套可以真正能够落地的系统。

所以我所有的分享，目标都不是给你一堆 AI 工具的技巧、模型的使用技巧，而是希望你听完之后知道怎么把某一项能力——比如今天分享的 Agent Skills——变成你自己工作流的一部分。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/15d5563-7a7-46e6-bbab-521b18f0f2f3_image-20251203221909883.png)

## 为什么我要花这么多时间研究 CLAUDE SKILLS

2024 年初，NVIDIA CEO 黄仁勋（Jensen Huang）在迪拜世界政府峰会上表示，AI 时代不需要人人学编程。当时我就做了 [一期视频](https://youtu.be/GBi5IUvbxRE?si=L7aZL8x9MqJX_WQN) ，那时候的观点就是：只会敲代码的人确实会被 AI 替代，但是一个能构建系统的人永远稀缺。

一年半的时间过去了，Claude 推出了 Agent Skills（官方称 Agent Skills，于 2025 年 10 月推出）。它的出现可以说是完美验证了预判。Agent Skills 可以让不懂代码的人也能用自然语言来构建复杂的工具。它实际上标志着我们跟 AI 的协作，从我们用 AI 做事的聊天模式进化到了我们让 AI 来帮我们构建系统的模式。

那听起来程序员是不是真要失业了？

事情没那么简单。为什么？因为用自然语言构建系统，也不是随便聊聊天就可以的。你需要知道怎么样去拆解需求、怎么样去设计架构、怎么样让 AI 来准确执行你的意图。这背后实际上需要一套严密的方法论来支撑，那这套方法论就是我的 MAPS。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/37fea25-e40f-7588-1eef-3e463f4a53_MAPS_.jpg)

所以不管你是不是程序员，如果你永远只停留在「这个工具怎么用」这一层，那在 AI 时代其实就很难建立起护城河。

具体到 Skills 这套技术，我认为它实际上做对了两件事。

**第一，它把我们的专业判断变成了 AI 的执行逻辑。** 不仅是我们告诉 AI 你要做什么，而是教它如何去做判断。我们相当于把我们的隐性知识显性化了，那 AI 就获得了我们原本自己独有的能力。

**第二，它找到了简单和复杂的一个最佳平衡点。** 我们完全使用自然语言就可以实现调用工具、集成 MCP 这些复杂的系统能力。所以我说它入门极简，但是上限极高。

对于我们的 MAPS 学员，今天的内容就是对大家所学体系的一个最佳验证。你会发现哪怕是像 Skills 这样 2025 年的最新技术，它依然可以用我们 MAPS 框架和 5A+ 方法论进行完美拆解。所以这也再次证明了我们底层逻辑的完备性——不管技术怎么变，只要掌握心法，我们就能一眼看出来本质。

那今天我们就用这套逻辑，来拆解 Agent Skills 的整个体系，从核心岛，然后进入到实战岛，再到进阶岛。相信读完之后，你就应该能够独立创建自己的 Skills。

---

## 核心岛

### 第一：Skills 的本质

Skills 到底是什么，为什么值得我们关注？

在官方的定义里面，原话就是：Skills 是由指令、脚本和资源组成的文件夹，Claude 会动态地去加载它们以提升在专业任务上的表现。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/e838387-44e4-ccc3-b1cb-e42cb11a0137_AI_Capability_Engineering_2.jpg)

所以这里面的关键词就是：它是一个 **结构化的文件夹** ，然后它会有 **命令和动态加载** ，它的目标是 **完成一个专业的任务** 。

我们可以来看一个 Skills 的简单结构。这就是一个 Skills，它就是一个文件夹。它的主文件就是 SKILL.md，这里面就是它的指令，主要的指令文件就在 SKILL.md 这个文件里边。然后它会有 reference，会有参考的一些信息、模板之类的，还有脚本。那这就是一个 Skills 的结构，很简单。这都是纯文本，Markdown 文本。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/578-c6bd-351e-4ac-af736acdb12_image-20251204114233448.png)

所以我们实际上可以把它简单地从用户的角度定义为： **它是一个把判断逻辑和处理流程写成 Claude 能反复执行的模块。**

因为这里面的一个关键就是它是一次定义，可以永久复用的，它是一个可复用的资产。我们 Skills 定义好之后，那么你团队的所有人都可以用到这个 Skills。而且我们以后可以在不同的场合、不同的场景下去使用。另外它也是动态加载，这个我们在后面也会详细讲它的动态加载机制。

**从 MAPS 的角度，Skills 实际上是从一个 Prompt 一次性的指令到可复用资产的过程。**

从我们的心智层上来说，我们旧的模式就是我们知道该怎么做，但是我们写 Prompt 每次都要重新描述。在新的模式下，我们就会把我们的方法去封装成 Skills 的模块，Claude 会自动去调用。

所以，Skills 的本质核心就在于： **它是把我们的隐性知识进行了显性化、模块化，并且我们可以进一步把它们沉淀成一个资产——AI 能力资产化。**

所以从架构的角度，我们就相当于从一次性的 Prompt 指令进一步走到了 Skills 可复用的模块。我们还可以进一步再用 Skills 资源库去管理我们的这些资产。比如我就用 Notion 数据库来管理所有的 Skills，这就相当于是我的一个 AI 资源库。

### 第二：Skills 与其他概念的关系

在 Claude 的生态里面有很多概念，那么它们之间到底是什么关系？有人说 Skills 比 MCP 还要重要，那这样说有道理吗？

我们其实用一个厨房就可以很好地看出 Skills、Project、MCP，还有 Subagent 这些概念的关系。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/6c02c0-e888-5e3b-1bd-0ff668c75638_AI_Capability_Engineering_4.jpg)

#### Skills 和 Prompt 的区别

我们首先来简单说一下 Skills 和 Prompt 的区别。从前边 Skills 的文件夹结构当中看到了，Skills 最主要的就是一个 SKILL.md 文件，那个文件本质上就是一个 Prompt。

问题就在于：我们是不是可以写一个很长的 Prompt，把判断标准、流程步骤、注意事项都写进去，让 AI 每次照着做，那跟 Skills 不就没区别了吗？

其实从内容复杂度来说，Prompt 和 Skills 没有本质区别。你完全可以写一个上千字的 Prompt，把它当作工作说明书来使用。

**那差别实际上在于它们的形态：**

- **Prompt** 是一次性的对话内容，模型也不会自动知道你什么时候该用哪一个 Prompt。更关键的是，Prompt 会一次都塞到上下文里边，它会大量占用你的 AI 模型的上下文空间。
- **Skills** 是把同样的东西换一个更工程化的包装。它有文件夹，里面会有所有需要的指令和资源文件。Claude 在启动的时候，它只会加载名字和简介，这也就大概一百来个 Token，觉得相关了才会把完整的内容读进来。

这就是 Skills 一个重要的特性，叫做 **渐进式披露（Progressive Disclosure）** 、渐进式加载。我们后面还会详细讲。

另外，同一个 Skills 可以在不同的对话产品里面复用。所以我们也可以理解为： **Skills 不是写出了一个复杂的 Prompt，而是把复杂的 Prompt 变成了一个有结构、可以复用、可以自动调用的模块。** 这就是我为什么很看重 Skills 的原因。

#### Skills 和 MCP 的区别

简单来讲，MCP（Model Context Protocol，模型上下文协议）是给 AI 应用的通用适配协议，它可以让 AI 应用用一套标准的方式去连接各种外部的数据、各种外部的工具。

所以有人说 Skills 比 MCP 还重要，这个话对不对？其实也对也不对。

不对的地方就在于 Skills 和 MCP 并不是一个东西，不好直接去比较。对的地方在于，如果是从一个技术的想象空间或者说颠覆性的角度来说，我同意 Skills 比 MCP 有更大的潜力和创新性。

#### Project 和 Subagent 的概念

这里面还有两个概念。

一个就是 Claude 的 **Project** 。Project 有自己的记忆，它也有自己的指令和知识库。

还有一个概念是 Claude 的 **Subagent（子智能体）** 。它也有自己的指令，而且它有自己的工具。

那这几个概念的区别在哪里？

还是这个厨房的类比：

- **Project** 就相当于整个厨房的场景，它会来定义本次任务的上下文环境。这个上下文环境中，我们看到的知识库的内容，对于小项目来说，它是完全要加载到 Claude 的上下文空间的。那对于大的项目、大的内容，它会自动切换成 RAG（检索增强生成）模式。这是 Project 的概念，它是我们整个工作场景的定义。
- **Subagent** 相当于是一个子智能体，它相当于是一个专职的助手，它会拥有独立的大脑，它是有独立的上下文空间的。Claude 本身，可以认为它是整个大厨，它是一个核心的推理和执行中心。而 Subagent 就相当于是各个不同的专职助手，我们可以有很多专职助手。每一个 Subagent 我们就可以把它当作一个有独立脑袋的人。
- **Skills** 本身，它可以用来编排其他多个 Skills 来完成工作，它也可以用来编排多个 Subagent 来完成任务。

#### 什么时候用 Skills，什么时候用 Subagent？

其实这个判断很简单。正是因为 Subagent 有一个独立的脑袋，所以我们来判断使用 Skills 还是使用 Subagent 来完成任务，重点就是来看： **你要做的这项任务，它更像是一个人，还是一项技能？**

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/a3713b2-f64f-6055-0d31-4701fa16f0ad_AI_Capability_Engineering_6.jpg)

- 如果它有独立的角色、独立的口吻，而且还要有独立的上下文空间、独立使用的工具，那么我们用 **Subagent** 来完成任务。
- 如果它更像是一个技能，它完全依赖于主 Agent、主 Claude，就是我们用的外层的这个 Claude 的空间作为它的上下文空间，那么我们就用 **Skills** 。

**Skills 是一项技能，Subagent 是一个人** ，这就是它们之间的概念。

### 第三：渐进式披露机制

Skills 如何避免上下文空间的过载？为什么它能自动激活？

那这个概念就是 Skills 的 **渐进式披露机制** 。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/87e6151-2e1-7786-7d-0fdab0c7d3b0_AI_Capability_Engineering_7.jpg)

渐进式披露，它实际上是一个三层加载的机制：

**第一层：启动加载**

当 Claude 启动的时候，Claude 会加载所有 Skills 的名称和它的描述。所以在这个过程当中，它的 Token 消耗是很低的，每一个 Skills 可能也就在 100 来个 Token 左右。

**第二层：意图匹配**

当在我们的对话当中，根据我们需要某一个 Skills 的时候，Claude 会根据用户的意图来寻找、匹配到最相关的 Skills 的描述。然后它会把这个 Skills 的 SKILL.md 这个指令，全部加载到上下文空间，之后它会根据 SKILL.md 的指令去完成任务。

**第三层：按需读取**

在完成任务的过程当中，当它需要这个 Skills 的完整内容，包括里面定义的那些脚本、还有它的参考资料、reference 这些内容的时候，它才会被加载到上下文当中，而且并不是全文加载，而是需要哪一部分它就加载哪一部分。

这个机制是 Skills 的一个非常关键的机制，也是很重要的创新点。它确保了我们的 Claude 可以管理大量的 Skills，但是却不会在每次对话的过程中产生很大的性能开销。

**这就像图书馆的三级检索：先看目录（名称描述），再翻章节（SKILL.md），最后查附录（参考资料）。**

#### 描述优化的四个关键要素

既然 Claude 会根据 Skills 的描述来触发 Skills、来选择我们要用哪一个 Skills，那么我们精雕细琢我们的描述，让 Claude 能在正确的时间找到正确的 Skills，就变得很重要了。

对于这个描述的优化技巧，它本质上还是 Prompt Engineering（提示词工程）的思想。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/8435b8f-34a1-1a35-a446-1a6043df08df_AI_Capability_Engineering_8.jpg)

对于一些不好的描述，就是模糊的、而且特别通用性的，这会导致 Claude 不知道你在什么时候该触发。一个好的描述，它就必须是要具体和包含触发词的。比如「把这个字幕转换成文章」，这就是一个具体的描述、具体的触发词。

那这里面就有四个关键的要素：

1. **明确输入类型** ：你的输入类型是什么？字幕转文章，我的输入类型是 SRT 格式的字幕，或者是一个 Excel、一个电子表格。
2. **说明核心功能** ：这个最好就是跟你日常使用过程中给它下的指令是一样的，这样它就可以精确匹配到你这个 Skills。比如字幕转文章，我们想说「把这个字幕转换成文章」，那么我们就在这个描述里头把这句话作为它的核心功能说明。
3. **列举关键触发词** ：字幕转文章，或者还再把它变成英文 convert subtitle to article 这样的，我们不光用中文用英文来说都会正确触发它。
4. **强调特殊能力** ：这个 Skills 定义的特殊能力我们也要在描述当中把它强调清楚。

达到了这四点，就基本上就具备了一个很好的描述了。 Claude 就可以在你需要这个 Skills 的时候，正确的找到这个 Skills。

那即便是出现 Claude 找不到合适 Skills 的情况，你也可以直接去指定这个 Skills 的名称来让 Claude 去调用正确的 Skills。

### 核心岛小结

三个核心岛的基本概念：

1. Skills 的本质到底是什么
2. 它和其他的概念 MCP、Project 有什么区别
3. Skills 如何避免上下文空间过载、它为什么能够自动激活

我们可以用 MAPS 的视角来快速小结一下。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/728ea0-214c-0a75-d26c-750e8581da_MAPS_.jpg)

**MAPS 有四个维度：**

**从心智层（Mindset）** ，我们从每次现编 Prompt 到一次封装永久复用，这背后就是我们的资产化思维链——把我们的隐性知识要显性化，并且进一步模块化和资产化成为我们的数字资产。这是从心智上我们怎么去看待这个事情，我们怎么去看待这一项新技术。

**在架构层（Architecture）** ，Skills 我们已经看到了，它可以看成是一个结构化的能力模块，再配合上渐进式披露这样的特点，就可以让多个 Skills 在我们的 Claude 里面共存。

**在提示词层（Prompt）** ，我们也看到了 SKILL.md 这个文件，它本质上就是一份结构化的 Prompt，所以它的描述又决定了什么时候触发这个 Skills。我们以前学到的那些提示词的小技巧，在这里全部都用得上。

**还有系统层（Systems）** ，我们的核心岛还没有完全展开，我们会在接下来的实战岛的部分进行揭晓。

有朋友说 Skills 有点复杂。其实 Skills 用起来很简单，它并不复杂，它就是像我们刚才看到的一个文件夹结构。我们甚至可以说，在 SKILL.md 里面你可以写一个最简单的 Prompt，比如说你就「把英文翻译成中文」，那这样我们就可以建立成一个 Skills。

所以这就是我一直说的： **它其实用起来非常简单，入门很简单，但是你要把它用好，它天花板很高** ，我们可以把它做成一个很复杂的工具。

---

## 为什么我这么看重资产化

接下来的问题很关键，为什么我这么看重资产化。

因为我本身是一个偏研究型的创作者，我习惯把一个问题想透，把它彻底的前因后果搞清楚，然后再纳入到自己的系统。所以多年的这种工程化训练，让我在遇到一个复杂问题的时候，我的脑子里就会自动开始拆解、开始枚举方案。

这些东西，其实就是一种 **隐性知识** 。我感觉到我自己是在用的，但是很难一句话讲清楚。我以前其实也会纠结，这种东西，它好像就是只有跟我一起共事的人才能互相去体会，它很难像教程一样教给别人。

然后后来我就尝试把这一套一点点拆解，所以这个过程也就慢慢沉淀成了我们现在的这个 MAPS 框架。

**所以对你来说，重要的不是要记住它这个名称这个缩写，而是养成一种习惯。** 这个习惯就是：

- 首先我们在 **心智层** 我们要想清楚，你到底相信什么，你看到的这些 AI 的现象你相信什么，你希望 AI 在你的工作生活当中去扮演什么样的角色。
- 真正我们要用好它，我们要在 **架构层** ，去把这些能力拆解成模块，我们不要每次都从零开始，也不要一下子眉毛胡子一把抓。
- 我们再到 **提示词层** ，这个我认为始终是重要的，不管它的概念被怎么变，人机对话始终是重要的。它的核心也就是我一直强调的：清晰表达。
- 最后在 **系统层** ，能把我们拆解的这些模块组合成一条稳当的工作流。比如今天讲的字幕处理工作流，就是系统层的典型应用。

**MAPS 其实并不是一个锦上添花的高级玩法，这是我觉得我们在 AI 时代我们要跑得久一点、跑得稳一点的一个最小化的能力包，必备能力，四点缺了任何一点都不会稳当。**

所以对我自己来说，MAPS 就是把这些隐性的套路全部模块化，变成一份可以传给别人的数字化资产。对你来说，你也可以用同样的思路，把你自己的经验、你自己的判断来慢慢变成你自己的思维体系、自己的结构。

---

## 实战岛：两种 SKILLS 类型的深度拆解

核心岛就是我们主要的概念，这个概念我是希望大家，只要对一个技术感兴趣，我们一定要先把它的基本概念摸清楚，这样避免我们后面会走偏。有了概念的指导，我们就很方便来做我们的各种事情了。

接下来的实战岛我们会讲到，两个 Skills 的类型： **能力包型的 Skills** 怎么样去封装一些判断逻辑， **软编排型的 Skills** 如何来调度多个 Agent、让多个 Agent 来协作、它们之间又是怎么来传递这些数据。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/62885e-bf41-7734-81e-04d3deba835_Claude_Skills_AI_Assetization_7.jpg)

那这一部分，实战岛这一部分，才是咱们 MAPS 的系统层的完整体现，它不是一个单点的能力，而是一个闭环的系统。

### 快速上手：用 skill-creator 创建你的第一个 Skill

我们还是从简，由简入难。首先来看，我们怎么样去快速的从 0 到 1 来创建一个 Skills。

关于 Skills 的安装，我在 [之前的文章和 Newsletter 里面](https://www.axtonliu.ai/newsletters/ai-2/posts/claude-skills-capability-package-soft-orchestration-guide) 都讲过它的具体安装方法，也包括一些演示的详细过程。这边我就不重复它怎么安装了，今天我们就直接来看我们怎么用 **skill-creator** 这个 Anthropic 官方提供的 Skill 创建工具来快速创建出一个可用的 Skills。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/6836a-6063-548-bce0-bf3cbebcc48_AI_Capability_Engineering_10.jpg)

用 skill-creator 创建一个 Skill 的过程非常简单。比如我们就用一个英文到中文的翻译作为例子，给它的 Prompt 就是：「你使用 skill-creator 来帮我创建一个把英文文章翻译成中文的 Skill」，就这么一个简单的命令。

那么 Claude 就会来帮你创建这个 Skill 了，它会调用 skill-creator，整个过程你都不用去干预，最终它会把 Skill 给你创建完成，并且给你打包好，然后供你下载。

一句话，它就把所有这些 Skill 所需要的文件给你创建完了。这个就是它创建好的 Skill，已经压缩好了，Skill 就是一个 ZIP 的压缩包。我们直接就可以把它存到我们的 Claude 桌面端里面，存完就可以直接用了，所以很简单。使用指南也给你写好，包括 SKILL.md 的完整内容都直接做好。我们也可以看它这个 Skill 的文件夹结构。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/a5fb5f8-80-25be-b8d1-2d7c46208185_CleanShot2025-12-04at12.10.18.png)

**所以 skill-creator，它是我们最简单的创建 Skill 的方法。** 多数情况下，skill-creator 都能满足我们创建 Skill 的需求，包括一句话的要求，还有我们说的我们已经调教好的各种 Prompt。

当然如果你希望增强 skill-creator 的功能，你也可以让 skill-creator 来更新 skill-creator。比如说你说「给我增加一个版本号，以后在你创建的任何 Skill 里面都增加一项版本号，除了名称和 Description 之外」。那么我们可以更新、升级 skill-creator，因为 skill-creator 本身它也是一个 Skill，它也是 Markdown 文件，我们可以直接去改它的。

**所以这个 skill-creator 大家一定要去试用一下，它是你最好的使用自然语言编程的实践方式。**

比如说你要操作 Notion 数据库，就像我之前给大家看到的我的 Skill，它是负责把我的 Skill 全部放到我的 Notion 数据库里面的。假设你也要做这个工作，你要操作 Notion 数据库，你直接用你的自然语言说，「你给我生成一个 Skill，你要把我的什么信息要写到我的 Notion 的哪一个页面里面去」。你可以让它去调用 Notion 的 MCP，你也可以让它直接去用 Notion 的 API 来写代码。

**在这个过程中，你根本不需要会写代码。所以 Skill 是一个你很好的使用自然语言来体验编程的实践方式，而且做完马上就可以用到你的实际工作和学习当中去。**

当然如果你要对 Skill 进行更精确的控制或者更复杂的判断，完全可以手写。这里重点的 SKILL.md 这个文件，它实际上除了下面的指令，重要的就是这边名称和描述，这实际上就是一个 YAML 结构，这部分我们课程中都详细讲过。它主要的指令部分就是一个 Markdown，所以你可以去读一下官方的写法，很快很容易就能理解它的结构，很不复杂，我们完全可以去手写它。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/f2a43b-ad6-276b-84b7-c66ddee36c0_CleanShot2025-12-04at12.13.39.png)

### 深入对比：能力包型 vs 软编排型

接下来来看两种不同的 Skill 的类型。

在官方的文档里边，我们总结出来它大致就三种用途：

1. **知识包** ：比如品牌配色规范、专业术语表都可以打包进去
2. **能力包** ：比如处理 PDF 文档、创作 Word 文档等等，这些是一些更多的能力
3. **编排型** ：它在单个 Skills 里面可以编排一个多步骤的流程

那今天我要展示的，实际上是我的两种实际使用场景：

**第一种，能力包型** ，这实际上就是官方设计的用途。它的代表案例，就是我的整理笔记的 Skill。为什么叫它能力包型的 Skill？因为它是用来封装我们复杂的判断逻辑和处理规则的，它不调用其他的 Agent，只是让 Claude 按照它定义的规矩来做事情。

**第二种，软编排型** 。这相当于是我的一种扩展用法，我把它叫做软编排型。它的代表案例，就是我的处理字幕，因为当我做完视频之后我会有字幕文件。那这个字幕文件，我需要把它进行处理，我需要把它转换成一个大家读起来可读性比较好的文章。当中的识别错误，我还需要进行校对、还需要校正。必要的时候，如果这个字幕是个英文文章，我可能还需要把它进行翻译。

所以这种编排型的 Skill，就是它用来协调多个步骤。比如把字幕整理成可读性好的文章，是一个 Agent 来完成的事情。翻译是另外一个 Agent 来完成的事情。那么我这个 Skill 就是来把这些很多个不同的 Agent 给它调配好，让他们按照要求的顺序和条件来完成任务。

所以即便我会用到主 Claude，它是一个协调者，去协调多个子 Agent、Subagent。 **这跟官方的编排型的区别就是在于：官方的编排型，它实际上还是在一个 Skill 里面去编排多个步骤的，它不会离开主 Claude 的上下文空间，它并不去调配子智能体，所有操作都在主 Claude 的上下文中完成。**

这个理论现在看起来如果不太清楚没关系，我们来看看案例，它到底在干啥。我们的重点不是看它的运行过程，是看它的设计思路。

### 案例一：能力包型 Skills——整理笔记的智能助手

我们先来看一下第一个能力包型。

我们来快速看一下我的这个整理笔记的 Skill 它做的是什么。它的场景就是把我的这些笔记文件、我的这个文件夹里面的这些文件，给它整理成一个结构化的素材库。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/55ddf33-fbf1-7fdc-4aba-dfeddaf5c3fc_AI_Capability_Engineering_11.jpg)

那它就会根据我描述，它就知道它需要去调用哪一个 Skill，它会知道它要调用这个 discussion-organizer 来处理这个任务。它首先把 Skill 的指令列举出来了——这就是我们前面说的，当我们用到这个 Skills 的时候，它会把这个读进来上下文空间。

这是整个它的执行过程：找到文件、读取文件内容，文件太长的话它会自己去进行分步来读取。然后它会根据需求来创建出它的待办事项，最后一步一步完成。中间结果你都可以看到，然后最终会生成一个报告，就是提取了多轮对话的结果。比如这就是它提取出来的结果，整理了我的讨论记录，给出了整理了论点等等。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/5adb-521b-772c-08ef-3bf70262f06f_image-20251204122116239.png)

那这就是一个能力包型的。因为我要整理这些笔记，我其实是需要它去判断：哪些是已经验证的核心知识，哪些是对我有价值的一些实践的检验，哪些是需要进一步验证的说法，哪些是跟我的专业完全没关系的可以直接扔掉的。

**在创建这个 Skill 之前，我做同样的事情，其实用的就是一个完整的 markdown 格式的文件作为 prompt。** 这个 prompt 我可以在 ChatGPT 或者 Claude 的 project 用，也可以在 Gemini 里面当作一个 Gem 来用。所以这个 discussion 这个 skill，它实际上就是基于我原有的 prompt 创建的。这就是我们之前说，我们只要用 skill-creator 根据我之前已经写好的 prompt，它就可以创建出一个 skills 来。完全跟我们之前的 prompt 其实是完成一样的功能，但是它可以复用，将来用起来就会非常方便。

#### 从零创建能力包型 Skills 的四步设计模式

如果我们要是从头来创建一个 skill，我们没有现成的 prompt，我们其实只要遵循一个四步的设计模式：

1. **明确任务边界** ：你的这个 skill 它输入是什么，期望的输出是什么
2. **定义判断逻辑** ：那这就是你的隐性知识了，你的专业领域的知识就要体现在你给它的说明里边
3. **定义处理规则** ：怎么去处理、输出什么格式等等
4. **准备参考资源** ：比如说你的专业的说明文档、你的专业术语，包括你需要它输出的模板

跟着这四步走，基本上我们就可以创建出一个合适的 skill 了。

#### Token 优化技巧

这边还需要注意的一点就是我们对 Token 的优化。因为参考的文档，它可能会很长，比如说还是我这个 skill，这是一个参考文档，就是我完整的 SOP，那它里面可能有各种框架的说明，这是一个很长文档。你不能让它直接给加载到上下文里去，所以你不能把这些信息写到 SKILL.md 这个文件里，你就把它放成参考文档。

那放成参考文档的好处就是，当我需要 TBRC（Thesis-Boundary-Racetrack-Closure，我设计的内容框架）框架的时候，Claude 只会在我这个文档里面去找 TBRC 框架的部分，它不会去读跟这个 TBRC 框架无关的其他框架的内容。 **这就保证了我们可以节省 Token。**

### 案例二：软编排型 Skills——字幕到文章的自动化流水线

我们来看一下第二个案例，软编排型。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/6858bb6-42a3-6644-f1a-30bfff886a20_AI_Capability_Engineering_13.jpg)

这种就是字幕文件、一个视频字幕，我需要把它转换成一篇可以发布的文章。首先这是一行一行的字幕，我需要把它转换成段落。另外字幕是语音识别来的，它必然会有识别错误，所以我要先进行校对。在校对的过程中，AI 也会提供一些修改的建议。校对完成之后，我们要根据这些修改的建议来最终成文。最后一步如果这是一个英文的字幕，我还需要把它翻译成中文。这是我的 Skills 要做的事情。

这个 Skill，我们跟其他的 Skill 不同。来看一下它的执行过程，我就说「把这个字幕转换成文章」，然后把这个字幕告诉它。那么它就会使用我的这个 SRT Workflow 这个 Skill 来处理。我们其实可以看到这个 Skill 里面的描述了，它实际上定义了四个阶段的工作流。第一个阶段它会调用 Subagent 了，会调用一个 Subagent。它一共会调用四个 Subagent，从 0 到 3，这四个阶段。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/f057e-c76-2b52-1f4b-b24c1b6be444_CleanShot2025-12-04at12.27.22.png)

它的执行过程：首先就是读入 SRT，然后检测语言，发现不需要翻译，所以就使用三阶段工作流来处理。之后就是在每一步，比如 Stage 0 进行分段，然后 Stage 1 对分段内容进行审阅、识别错误的矫正。四个分段，这四个过程就调用了三个 Subagent、三个子智能体，最后生成最终的文章。这就是它的工作过程。

有朋友问智能体是在 Skills 里面说明吗？智能体不是在 Skills 里面说明，智能体是在 Claude Code 里面单独创建的，但是我们 Skill 是可以去调配它。

#### 软编排到底在做什么？

首先这个 Skill SRT Workflow，它不是自己干活，它只是定义了一套四个阶段的 SOP（标准操作流程，Standard Operating Procedure）。它会在每一个阶段去调用不同的 Subagent，每一个阶段都是一个 Subagent。

而每一个 Subagent，它是有自己的上下文窗口的，而且它会有自己允许使用的工具的白名单。也就是说，你比如说让字幕分割用 A 工具，让审查用 B 工具，你就可以给它们进行严格的指定。 **这样就保证了你的工具、包括权限、这个安全性。**

所以我们的主 Claude，它运行这个 Skill，它像一个项目经理。我们运行这个 Skill 是我们的 Claude，它像一个项目经理，它读取这个里面定义的 SOP，然后它会用 Task 工具、用工具按顺序来调用不同的 Subagent。它会去检查每一个阶段的输出，来决定下一步走哪一条分支。

**所以这种方式，实际上我们可以构造出很复杂的工作流。**

但是注意的就是，这个案例它只能在 Claude Code 里面用，因为它要用到 Task 工具去调用这些 Subagent、子智能体，所以它只能在 Claude Code 里面用。

#### 文件传递上下文的设计理念

这个案例里面有一个重点的设计理念，其实对你是很有参考价值的。就是我们在不同的 Subagent 里面，它实际上是要用来传递上下文的。那传递上下文一种方式，我们就可以通过主 Claude 来传，把输出告诉主 Claude，Claude 再把它的输出给到下一个 Subagent 作为下一个 Subagent 的输入。

**但是在我的设计里面，我用的是文件来传递上下文。** 也就是说，一个 Subagent 它完成工作之后，它会把它的结果输出到文件。下一个 Subagent 它需要前一个 Subagent 的输出的时候，它会去读这个文件，就是用文件来传递上下文。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/307bf8b-efae-4ed4-be15-377580244a4e_AI_Capability_Engineering_14.jpg)

**这就像工厂流水线，每道工序只看上一道的成品，不需要知道全部历史。**

它最主要的好处就是 **上下文的隔离** ——它不会导致我们的 Claude 的上下文空间被撑爆，同样也不会因为一些没有必要的上下文留在这个 Claude 的上下文空间里面去污染它的上下文空间。因为我们不是每一个这个智能体它都会需要前面所有智能体的输出。比如我的翻译的智能体，它可能只需要前一个阶段的智能体的输出就可以了，它并不需要前面再往前那几步的输出结果。

所以这里面一个主要的设计点就是在于，我们来使用文件来传递数据，在各个智能体之间。 **而且中间文件可以人工查看的，所以如果有问题我们都可以检查，也可以知道它的问题出在哪一个环节上。** 这是一个设计思路。

#### 工程级软编排的四条核心规则

为了做好一个工程级别的软编排，我们有四条核心规则需要遵守。这四条规则可以保证我们做出来的这种软编排，它不是一个玩具，它可以真正达到工程级别。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/f82415-4e-442-b28-884f3ee6b1a_AI_Capability_Engineering_15.jpg)

**第一，职责清晰。** 你的主的 Skill 它只定义规范，主 Claude 只负责理解和决策，用 Task 工具去负责调用执行，你不要把这个职责给混淆。主 Claude 不做事，它只负责调配。

**第二，最小权限。** 既然用到了 Subagent、子智能体，那么每一个子智能体实际上我们可以单独给它设置它的系统提示词和它的工具白名单，所以不要给多余的权限，只给它必须的那些工具就 OK 了。

**第三，文件传递。** 阶段性的产物，我们就通过固定文件命名的约定，我们在 agent 之间传递就可以了，不要在对话之中去粘贴内容。

**第四，失败记录。** 你的 agent 比较多的时候，你任何一个阶段的失败，你应该把它写到一个文件里面。这个文件实际上就相当于是一个总报告、运行报告。这可以保证你在中间环节出错的时候，一方面去调试，另外一方面你还可以去回滚。

### 实战岛小结

我们可以快速回顾一下。

首先就是 **快速上手** ，我们用 skill-creator 可以几分钟就创建你的第一个 Skill，所以建议大家赶紧试用一下，如果没用过的话。

那 Skill 的两种方式：

- **能力包型** ：就是把我们的判断逻辑封装起来方便复用、封装成一个可复用的模块
- **软编排型** ：我们可以在多个 agent 之间去协作，可以用文件来传递数据，可以失败了我们还有记录

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/bef6c-6d0f-8a68-7afa-d44d071a4272_AI_Capability_Engineering_12.jpg)

**这就是 MAPS 系统层的完整体现：不只是单点能力，而是可运行、可迭代、可扩展的系统。**

我们构建的不只是一次性 Prompt，而是可运行、可迭代、可扩展的系统。比如说我的字幕处理的四阶段工作流，那我再有其他需要的功能，我只需要扩展我的 agent 就行了，整个结构其实都已经定义好。

**在做这些 Skill 的整个过程当中，我是没写一行代码，但是我们产出的，确实具有工程级别能力的系统。** 所以这就是我开头说的，只会敲代码的人可能会被替代，但是构建系统的人会永远稀缺。其实这对任何一个技术类的职业，它都是适用的，比如说数据分析等等。

Skill 降低的就是我们构建系统的技术门槛，但是它并没有降低我们的方法论门槛。那我们刚才演示当中的拆解思路、架构设计、编排逻辑，实际上都来自于我们的 MAPS 的课程体系。

---

## 进阶岛：从想法到落地的系统化方法

接下来我们就要进入进阶岛了。进阶岛的内容比较多，我会精选其中部分重点内容来分享。

首先有朋友问：智能体是在 Skills 里面说明吗？

智能体不是在 Skills 里面说明的，智能体是在 Claude Code 里面定义的。

在 Claude Code 里面，agents 命令就可以创建智能体。比如创建一个新的智能体，然后你还可以管理你自己创建好的智能体。

智能体概念可能听起来有点大，但是它的结构其实并不复杂。我们来看字幕分段的智能体示例。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/47ad4b-0be-4043-47a1-00ed8ecb341b_image-20251204123541154.png)

首先它也是一个描述，这就跟 Skills 的描述很类似的，它是告诉 Claude 我们什么时候用这个智能体，而 Skills 的描述就是告诉 Claude 什么时候用那个 Skills。所以这个描述同样要遵循跟 Skills 同样的规则，我们要把它写清楚。那这边还有例子，给出了例子。

在你定义智能体的时候会有一个 Tool 工具的定义，注意： 在 Claude Code 的 Skills 里，也支持 `allowed-tools` ，它决定 **“这个 Skill 激活时实际能用什么”** 。但是，它并不能突破当前会话 / Agent 所决定的工具上限。然后你也可以选择不同的模型。

**所以我们说智能体它是一个人，它是有独立大脑的人，每一个智能体它都是一个单独的人、一个单独的 AI。而 Skills，它是技能，它共享主 Claude 的那个人的。**

下面，就是它的 System Prompt 系统提示。这个系统提示也是一样，跟普通的提示没有什么差别，定义角色、必须遵守、然后该怎么做等等，输出文件的结构。这边就定义了一个返回信息。完成以后我要向主 Claude 返回什么？返回我这一步完成的信息，然后我还要输出文件。这就是一个 Subagent、Agent 的定义。

**所以每次看到名词，如果不了解，可能觉得这个是不是一个什么很难的东西。但是你用起来就会发现，其实用工具、用功能都是很简单的，难在你怎么去系统化地把它用好，而不是说哪个按钮怎么点、使用步骤这些并不是很困难的。** 这也是 MAPS 课程要解决的核心问题。

### 5A+ 方法论：Skills 设计的完整闭环

我们来看进阶岛的第一个重点：Skill 的设计和 5A+ 落地方法论。

它解决的核心问题是什么？就是我们如何从想法到落地来系统化地设计一个高质量的 Skill。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/dcf6b2-1a41-df26-04c6-da8357be656_AI_Capability_Engineering_17.jpg)

这个方法论有五个过程，最重要的首先就是说我们要明确我们的设计目标，就是 **AIM（明确目标）阶段** 。

#### AIM：明确目标

这一步所完成的核心问题是什么？它解决的核心问题就是： **你的这个任务值得做成 Skill 吗？**

我们评估的框架就在于，对于一些重复性高、然后有标准的流程、也比较耗时间、还需要专业判断的这些事情，包括涉及到一些领域知识，那么说明这个任务就值得做成一个 Skill。

**所以专业判断、领域知识，这就是我们经常说的隐性知识，涉及到这些它就值得做成一个 Skill，把它显性化，然后我们可以去分享、把它资产化。**

那不适合做成 Skill 呢？比如说一次性的任务、高度创意性的工作，或者太简单的任务，而且每次执行的时候场景差异太大，没有什么标准化的流程，那这种就不适合做成 Skill。

#### ACQUIRE：获取资源

获取必要的背景资料和参考案例，比如现有 prompt、官方文档、团队已有 SOP 等。

#### ATTEMPT：快速验证

我们怎么样去小步快跑，来最小化地去验证我们的 Skill。

不要一下子上来就把我们所有想的可能十个步骤一下子做成一个 Skill 来做，这样你会很难去调试和测试它。所以我们就从一个两个开始，从一个最小功能的 Skill 来做，就跟我们最小产品的方式是一样的 MVP 最小化产品，那么 Skill 我们就叫 **MVS（Minimum Viable Skill，最小可行 Skill）** ，来一步一步去扩展。

#### ADJUST：评估迭代

你的 Skill 到底做得好不好，这个实际上是我们需要一些数据来进行迭代优化的。比如说：

- **触发准确率** ：是不是每次我想让这个 Skill 来出现帮我做任务的时候，我说的一句话，Claude 都能正确去调用这个 Skill
- **执行成功率** ：Skill 是否按预期完成任务
- **资源消耗** ：Token 使用量是否合理

这些我们来去不断优化它。

#### APPLY：规模化

最后我们就想办法让我们的 Skill 成为一个可持续的资产，我们就把它进行规模化或者资产化。

比如说我们一个简单的 Skill，我可以通过场景的扩展让它完成越来越多的功能。然后我可以把它跟我们的团队进行共享。然后我还可以通过集成 MCP、集成 API 来让我的 Skill 的能力越来越强、更加强大。规模就越来越大，它所能完成的事情就越来越多，这就是一个规模化的过程。

**所以任何一个，不光是 Skill，我们来做任何一个项目，这个 5A+ 的方法论，都是可以帮助你来把这个事情做成一个完整闭环的。**

### 构建你的 AI 资源库：管理与迭代

我们再看下一个点。这个是我建议大家来做一个自己的 AI 资源库。我用 Notion 创建可自动同步的 AI 资源库。大家可以用任何一个工具 Obsidian 等等，用你的笔记工具来做你的资源库。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/fff4707-0a57-3d25-b77-f70ee0a07c8_AI_Capability_Engineering_20.jpg)

因为当你有越来越多的 Skill 的时候，你需要记住他们的用途、触发词。关键是，如果你的 Skills 是一个编排型的 Skill，它会调用其他的 Skill，它也还会去调用其他的 Subagent，你要记住它这些靠脑袋记就很费劲了。它还有版本整个的迭代过程， **所以我建议大家用一个 AI 资源库来管理你所有的 AI 资源。**

这就是我的 Notion 的资源库，它的结构。它是配合我那个自动更新的 Skill 来实现自动同步的。当我有新的 Skill 之后，我就可以自动把这个 Skill 同步到我 Notion 的资源库里面来。正是这个 Skill，它是一个工作流，它实际上调用了 Notion 的 MCP 并且集成了一些 API 的工具、写了一些小代码。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/b610f-3e1d-f5e2-481e-1e16bb061b40_CleanShot2025-11-26at17.41.57.png)

我们在这里其实就可以看出我在用的 Skill 这些用法：

- 编排 Skill，Skill 可以调用 Skill
- 编排 Agent 来调用 Agent
- 调用 MCP、调用工具
- 状态管理

那这个 Notion 版本的 AI 资源库，我们 MAPS 课程里面是有专门的 Notion 的新手教程的，从 0 开始设计来构建这样的 AI 资源库。不光 Skill，我们还可以把我们的 Agent、把我们的 Prompt 都统一地管理起来。

### 实战经验：三大原则与常见陷阱

然后再分享一些我们实战经验过程当中的规范和常见的陷阱。这个也是我在做 Skill 过程当中去碰到过的各种事情，总结出来的。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/736ce0b-6230-0507-06e4-44a66ce1d7_Claude_Skills_AI_Assetization_13-4870664.jpg)

#### 三大核心原则

首先就是三大核心原则，本质上来说这还是一个 Prompt Engineering、提示词工程的过程。

**第一，简洁至上。** 我们不要浪费它的上下文空间，上下文窗口是我们最宝贵的资源。所以 SKILL.md 这个文件里，我们要控制它的大小，复杂的逻辑和文档都放到它的参考里面。

**第二，合适的自由度。** 关键在于给模型合适的自由度，我们需要根据我们的任务来决定它的精确度。对于一些需要很准确的步骤，比如说我的窗口大小我一定要有 300 个像素，那这种我们就不能让模型去任意发挥，我们需要通过很精确的指令来确定，就是说给模型最低的自由度。但是你要需要模型有一定的创造性，你就需要给它高一些的自由度，你不能把模型限制。这就是自由度，我们要有合适的自由度，需要精确我们就不要让模型去猜测。 **自由度的选择，取决于你对结果的控制需求。**

**第三，迭代驱动。** 就是我们前面说的，我们真实的使用中发现问题，然后不断去完善我们的 skill。

#### 常见陷阱

这里面几个常见的陷阱：

**过度工程化。** 我们要尽量保证我们 skill 的职责是单一的，我们不要把太多的功能塞到一个 skill 里面。如果你要完成的功能太复杂，那么我的建议就是拆分，拆分成更多的 skill、更多的 agent。

**文档和实现的脱节、触发混淆。** 对我们这个是我们需要精心设计我们的 description，就是描述，避免它误触发或者不知道该触发哪一个，然后还要节省我们的 Token。

**边界情况。** 什么是边界情况？标准的输入下，它的 skill 可能工作很正常，但是有一些非常极端的情况会导致 skill 来出错。比如我需要 skill 处理我的文本、markdown 的文本，但是我给它那个 pdf 文件，它肯定就处理不了。但是如果你不说明我只能处理文本，它可能就会去试图处理这个 pdf 文件，那这一步其实是多余的操作，我们应该去避免这样的多余的操作。

---

## MAPS 视角总结

我们就用 MAPS 来再做一个简单的回顾。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/d13a1c-badd-d44-37c-74a5a6612c7e_Claude_Skills_From_Command_to_Asset_17.jpg)

### 心智层

还是首先心智层，我们一定要建立起来的就是 **资产化思维** 。这也是 Skills 带给我们的最方便的一点，Skills 不是一个用完就扔的 Prompt，它是可以反复来进行增值的数字资产，把我们的隐性知识资产化。

**从今天开始，把你常用的 Prompt 改造成第一个 Skill，开启资产化之路。**

然后 **迭代驱动开发** ，我们不要追求一步到位，快速验证、小步快跑。

### 架构层

我们之前看到了能力包、软编排，这是使用 Skills 的多种方法。然后在软编排的过程当中，我们通过文件的传递来让上下文保持干净，它可以支持更大规模的工作流。

### 提示词层

**清晰表达** ，这就是我们一直强调的清晰表达。然后 Skills 本身特有的按需加载，它避免了上下文空间爆炸。这里面重点就是我们需要精细地去设计 Skills 的描述，保证 Claude 不会用错，它很清楚知道你的 Skills 在干什么。

### 系统层

我们可以通过 **5A+ 的循环** 把我们的想法落地，5A+ 的循环可以帮助我们做到工程化的实践。那工程化的实践，除此之外还有更多的比如版本管理、还有测试策略等等，这些都是进阶岛的内容。以后有机会再跟大家详细分享，这些更进一步的内容。

然后就是 **资产库** ，我们建立我们自己的 AI 资源库，这样我们的这些 Skills，我们可以检索、可以追踪。还有些测试的过程，保证我们 Skills 稳定可靠。

---

## 核心结论

讲到这，今天的三个岛基本上就要做完了。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/f1e335-c8c0-4bdb-ccf6-a08384f285f_Claude_Skills_AI_Assetization_3.jpg)

如果你能看到现在，我相信你应该已经发现一件事情： **你对 Claude Skills 的兴趣，其实不应该停留在「这个功能特别酷」这一层。**

我希望大家下意识地想：这个东西它在我的 workflow、在我的工作流里面，它应该能放到哪一层？它能不能变成一个稳定的 SOP？我今后就不用再一遍一遍复述，能不能去复用、方便维护，并且交给别人来用？

**所以我们对 AI 的期待，看到 Skills，我们不是多了一个新玩具，而是多了一个优化现有系统的组件。**

---

## 附：N8N / MAKE 和 SKILLS 的关系（FAQ）

有朋友问到 N8N 和 Skills 的关系。

像 N8N 或者像 Make 这样的自动化工作流平台，我前面之所以把我 Skills 叫做 **软编排** ，那么这些自动化工作流平台，它实际上我们可以认为它是 **硬编排** 。

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148203597/images/afd5f4-a72b-468-c28b-84c74088d63e_AI_Capability_Engineering_12-4871115.jpg)

你需要有非常严格的流程控制，甚至你需要有更广泛的工具的生态。那么 Make、N8N、Zapier 等工作流自动化平台，还是你的不二之选。

**任何一项技术，它都不可能满足所有的应用场景。** 比如像 Make，它几千种 App、几千个服务的集成，有非常严格的流程控制，这些方面，Skills 是做不到的。如果你需要有更加严格的工作流编排、更广泛的 API 或者工具调用的话，那么这些老牌的自动化平台还是必要的，它并不是被替代了。

[![旗舰课程 MAPS™ 训练营](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/themes/2156870510/settings_images/23a3eb-0a7-d375-e087-471c55cca_a2e26503-cd1e-4000-adc7-d8655929c339.jpg)](https://www.axtonliu.ai/resource_redirect/landing_pages/2151451780)

## 这篇文章解决了你的一个“点”

但真正的竞争力，来自于将无数个“点”连接成“系统”的能力。旗舰课程 **MAPS™ 训练营** 专为此而设，带你从解决零散问题，到构建一个能为你持续创造价值的AI强大引擎。