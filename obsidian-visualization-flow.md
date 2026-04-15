# Obsidian 可视化技能流程图

## 图表说明
以下流程图展示了 Obsidian 中原生的可视化功能、丰富的插件生态系统以及 AI 工具的整合，构成了完整的数据可视化和知识管理能力。

```mermaid
graph TB
    subgraph native["原生功能"]
        MDT[Markdown 语法<br/>粗体 *斜块* 代码]
        LV[链接和嵌入<br/>[[链接]] ![]()]
        BKM[双向链接和图谱<br/>🔗 反向链接]
        CV[Canvas 白板<br/>📝 自由布局]
        DT[Dataview 表格<br/>📊 动态查询]
        TP[模板片段<br/>📋 快速插入]
        BT[块级引用<br/>^(块引用)]
    end

    subgraph plugins["插件生态"]
        CT[Chart.js<br/>📈 图表生成]
        GP[Graphviz<br/>🔗 拓扑图]
        MP[MindMap<br/>🧠 思维导图]
        BPC[BP 矩阵<br/>⚡ 四象限]
        GP2[Grid 渲染<br/>⚡ 表格视图]
        Ex[Excalidraw<br/>🎨 手绘图表]
        MP2[Marp Slides<br/>📼 幻灯片]
        R[Rollbar<br/>📜 轮播代码]
    end

    subgraph ai["AI 工具"]
        GPT[ChatGPT 集成<br/>💬 对话式]
        MH[Mermaid Helper<br/>📝 自动生成]
        CA[Canvas AI<br/>🤖 智能布局]
        KH[Khoj 搜索<br/>🔍 智能检索]
        G[Gemini Pro<br/>🌟 多模态]
        M[Claude 填充<br/>✨ 内容扩展]
    end

    subgraph core["核心可视化能力"]
        OT[文本输出<br/>📄 文档]
        IR[图像渲染<br/>🖼️ 图片]
        IC[交互组件<br/>🎮 表单]
        SG[结构化数据<br/>📊 表格]
        N[网络图<br/>🕸️ 关系]
        T[时间轴<br/>⏰ 序列]
        R3D[3D 可视化<br/>🎲 立体]
    end

    subgraph input["输入源"]
        MD[Markdown 文档]
        MD2[CSV/TXT 数据]
        MD3[代码文件]
        MD4[网页内容]
        MD5[图片资源]
    end

    subgraph output["输出方式"]
        VP[可视化预览]
        EP[导出图片]
        SP[分享链接]
        EP2[PDF/HTML]
        VP2[演示模式]
    end

    %% 连接关系
    input --> native
    input --> plugins
    input --> ai
    
    native --> core
    plugins --> core
    ai --> core
    
    core --> output

    %% 样式定义
    classDef native fill:#e5f3ff,stroke:#3182ce,stroke-width:2px
    classDef plugins fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    classDef ai fill:#fef3c7,stroke:#d97706,stroke-width:2px
    classDef core fill:#f3e8ff,stroke:#7c3aed,stroke-width:2px
    classDef input fill:#fee2e2,stroke:#dc2626,stroke-width:2px
    classDef output fill:#dcfce7,stroke:#16a34a,stroke-width:2px

    %% 应用样式
    class MDT,LV,BKM,CV,DT,TP,BT native
    class CT,GP,MP,BPC,GP2,Ex,MP2,R plugins
    class GPT,MH,CA,KH,G,M ai
    class OT,IR,IC,SG,N,T,R3D core
    class MD,MD2,MD3,MD4,MD5 input
    class VP,EP,SP,EP2,VP2 output
```

## 主要特性说明

### 原生功能
- **Markdown 语法**：基础的文本格式化和代码块支持
- **链接系统**：双向链接和嵌入功能，知识图谱可视化
- **Canvas**：自由画布，支持拖拽和自定义布局
- **Dataview**：基于查询的动态表格和数据展示
- **模板**：可复用的内容和结构模板
- **块引用**：精确到段落级别的引用和引用

### 插件生态
- **Chart.js**：丰富的图表类型，支持交互式数据可视化
- **Graphviz**：自动生成关系图和流程图
- **MindMap**：交互式思维导图，支持多层级结构
- **BP 矩阵**：四象限分析图，用于优先级管理
- **Grid 渲染**：表格化和结构化数据展示
- **Excalidraw**：手绘风格图表，支持手绘形状和文字
- **Marp**：基于 Markdown 的幻灯片生成
- **Rollbar**：代码片段轮播展示

### AI 工具集成
- **ChatGPT**：对话式内容生成和问答
- **Mermaid Helper**：自然语言转流程图
- **Canvas AI**：智能布局和内容建议
- **Khoj**：语义搜索和关联发现
- **Gemini Pro**：多模态内容处理
- **Claude**：内容扩展和重写

### 可视化输出类型
- **文本**：格式化的文档和报告
- **图像**：PNG/SVG 格式的图表
- **交互**：支持用户交互的组件
- **结构化**：表格和结构化数据展示
- **网络**：关系图和拓扑结构
- **时间**：时间轴和序列展示
- **3D**：立体图形和空间可视化