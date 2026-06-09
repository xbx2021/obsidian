https://github.com/haris-musa/excel-mcp-server

这是一个**基于 MCP（Model Context Protocol）的 Excel 操作服务器**，**无需安装 Microsoft Excel**，就能让 AI 代理 / 客户端创建、读写、修改 Excel 文件。
## 一、核心定位

- 遵循 **MCP 协议**，为 AI 提供标准化 Excel 操作接口
- 纯 Python 实现，依赖 openpyxl，跨平台运行
- 支持本地 / 远程调用，适配 Claude Desktop 等 MCP 客户端

---

## 二、完整功能清单

### 1. 工作簿与工作表

- 创建、读取、保存、修改 Excel 工作簿（支持 .xlsx/.xlsm 等）
- 工作表：新增、复制、重命名、删除、调整顺序
- 获取工作表元信息、结构解析

### 2. 数据与公式

- 单元格 / 区域读写、批量写入、分页读取
- 完整支持 Excel 公式（写入与计算）
- 数据校验：范围、公式、数据完整性校验

### 3. 样式与格式

- 字体、颜色、边框、对齐、填充
- 条件格式、单元格合并
- Excel 表格（Table）样式自定义

### 4. 图表与数据透视表

- 生成折线、柱状、饼图、散点图等主流图表
- 创建、更新动态数据透视表
- 支持图表样式与布局配置

### 5. 传输与部署

- 三种传输方式：
    
    1. **stdio**（本地首选）
    2. SSE（已弃用）
    3. **Streamable HTTP**（远程推荐）
    
- 环境变量配置文件根目录、服务端口
- 支持本地服务与远程部署

### 6. 安全与路径控制

- HTTP/SSE 模式强制相对路径，禁止绝对路径与目录穿越
- 可指定 EXCEL_FILES_PATH 限定读写目录
- 结构化错误返回，便于 AI 处理与调试

---

## 三、典型使用场景

- AI 助手自然语言操作 Excel（生成报表、提取数据、画图表）
- 自动化流程：批量处理表格、生成周报 / 月报
- 无 Excel 环境的服务器端报表生成
- 低代码 / AI Agent 接入表格能力

## 安装
需要先安装uv命令
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
**astral.sh 是专注打造极速 Python 开发工具链的技术公司官网，核心是用 Rust 开发高性能 Python 工具，提升 Python 生态效率**。 https://astral.sh/

 **主力产品 
- **Ruff**
    极速 Python 代码检查器（linter），速度比 Flake8、Pylint 等快**近 1000 倍**，支持自动修复。
    
- **ty**
    极速 Python 类型检查器 + 语言服务器，对标 mypy、Pyright、Pylance。
    
- **uv**
    极速 Python 包管理器与环境管理器，替代 pip、pip-tools、venv 等。


claude code 安装MCP
```
claude mcp add excel -- uvx excel-mcp-server stdio
```