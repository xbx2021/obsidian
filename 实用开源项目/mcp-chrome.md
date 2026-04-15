https://github.com/hangwin/mcp-chrome

|维度|chrome-devtools-mcp|mcp-chrome|
|:--|:--|:--|
|**维护方**|Chrome 官方（ChromeDevTools）|第三方社区（ZodOpen）|
|**浏览器环境**|全新、隔离、干净实例（无插件 / 登录）|复用当前正在使用的 Chrome（保留所有状态）|
|**底层通信**|Puppeteer → CDP（调试端口）|Chrome 扩展 API（无需 CDP）|
|**核心定位**|DevTools 调试、性能、诊断|日常浏览器操作、自动化、内容提取|
|**核心能力**|Console、Network、Performance、DOM、Lighthouse|标签管理、导航、内容、书签、历史、下载|
|**安装方式**|npx 直接运行|安装 Chrome 扩展 + 启动本地服务|
|**典型场景**|前端调试、性能优化、AI 测试|AI 接管浏览、批量操作、内容抓取|

