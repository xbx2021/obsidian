https://github.com/VoltAgent/awesome-design-md

目前已参考 66 个顶级网站的视觉风格，提炼成了现成的 DESIGN.md 文件，可直接拿来就用。

比如 Notion、Linear、Figma 等，覆盖 AI 工具、开发者工具、设计工具、电商、金融、汽车等多个领域，基本想得到的标杆产品都有。

每个网站除了 DESIGN.md 文件本体，还附带了一个 preview.html 预览页，能直观看到色板、字阶、按钮、卡片的具体样式，不用全靠想象。

使用也非常简单，以 Notion 为例。

在 GitHub 仓库里找到 Notion 风格的 DESIGN.md，下载并放到本地项目根目录。

或者直接访问网站 https://getdesign.md 找到 Notion 设计规范：

然后执行对应安装命令即可：

```
npx getdesign@latest add notion
```
接着打开 Claude Code，告诉它：
```
请参考项目根目录下的 DESIGN.md 风格，帮我构建一个关于 Hermes Agent 介绍网站。
```
对某个细节不满意，继续对话微调就行。整个过程不需要自己查颜色值，也不需要手动调字体。