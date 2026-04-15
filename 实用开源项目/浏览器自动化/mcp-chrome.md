https://github.com/hangwin/mcp-chrome

| 维度          | chrome-devtools-mcp                                                          | mcp-chrome                     | Playwright (含 @playwright/mcp)                       |
| :---------- | :--------------------------------------------------------------------------- | :----------------------------- | :--------------------------------------------------- |
| **维护方**     | Google Chrome 官方                                                             | 第三方社区（ZodOpen）                 | 微软（官方）                                               |
| **MCP 定位**  | AI 前端调试 / 性能分析                                                               | AI 接管日常浏览器                     | AI 自动化 / E2E 测试                                      |
| **浏览器环境**   | 全新、隔离、干净实例（无插件 / 登录）                                                         | 复用当前正在用的 Chrome（全状态保留）         | 全新隔离实例（可配置用户数据目录）                                    |
| **通信方式**    | Puppeteer → CDP（调试端口直连）                                                      | Chrome 扩展 API（无需 CDP）          | Playwright 引擎 → 跨浏览器协议                               |
| **核心能力**    | DevTools 全量：Network 抓包、Performance Trace、Console 日志、DOM/CSS、Lighthouse、JS 执行 | 标签管理、导航、内容提取、书签 / 历史、下载、表单、多标签 | 跨浏览器交互、智能等待、断言、截图 / 录屏、网络拦截、CI / 并发、多浏览器             |
| **安装 / 启动** | `npx chrome-devtools-mcp@latest` 直接运行                                        | 装 Chrome 扩展 + 启动本地 MCP 服务      | `npm init playwright@latest` 或 `npx @playwright/mcp` |
| **适用场景**    | 前端 Bug 定位、性能优化、网络分析、Lighthouse 审计                                            | AI 辅助浏览、批量操作、内容抓取、保留登录的自动化     | E2E 测试、稳定自动化、跨浏览器验证、CI 流水线                           |
| **跨浏览器**    | ❌ 仅 Chrome/Chromium                                                          | ❌ 仅 Chrome                     | ✅ Chrome/Firefox/Safari/Edge                         |