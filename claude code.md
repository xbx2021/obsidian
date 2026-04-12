# 安装

官网 https://claude.com/product/claude-code

安装claude code
```
npm install -g @anthropic-ai/claude-code
```
github https://github.com/musistudio/claude-code-router 将开源模型接入claude code

- 安装claude-code-router
```
npm install -g @musistudio/claude-code-router
```
- 创建配置文件
`~/.claude-code-router/config.json`

- 配置文件设置provider为Qwen模型
- 魔塔社区 https://modelscope.cn/my/access/token 获取访问令牌，复制到配置文件api_key
- 启动claude code
```
ccr code
```
