## 安装
```shell
pip install graphifyy && graphify install
```

生成的graphify-out文件：
- graph.html - 交互式图形
- graph.json - 原始图形数据
- GRAPH_REPORT.md - 审计报告
- cost.json - 令牌使用情况                          
- manifest.json - 清单文件 
## 使用

`/graphify` 在项目目录下，cc或openCode输入命令生成知识图谱

`/graphify query` 查询内容

`/graphify explain`  解释实现

`/graphify --update` 更新图谱

`/graphify add` +链接地址，获取内容，更新图谱

`/graphify path` 追踪节点和代码实现之间的图谱路径

`/graphify --obsidian` 生成笔记

更多使用命令：
https://github.com/safishamsi/graphify/tree/v4