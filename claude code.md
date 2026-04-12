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
- 配置其他模型，需要获取base_url和api_key

# 用法

`/init` 通读项目，保存到CLAUDE.md文件，cc执行任务前先读取文件来了解项目

`/compact` 压缩上下文，减少token消耗

`/clear` 清楚上下文，新任务不受上下文影响

`shift+tab` 切换模式，默认普通模式修改代码需要人工审核，auto-accept模式不需要审核，
plan mode只提出想法，不修改代码

`/ide`  
# 其他
接入Gemini，Gemini负载均衡