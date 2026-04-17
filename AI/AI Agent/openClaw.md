# 安装（windows）

- 下载并安装Node.js  22.x 或更高版本 https://nodejs.org/

- 全局安装 OpenClaw
````
npm i -g openclaw
````

- 运行初始化向导
```
openclaw onboard
```

- OpenClaw 自带诊断工具，自动检测问题：
```
openclaw doctor
```

- 启动网关
```
openclaw gateway run
```

- 打开控制面板
```
openclaw dashboard
```


碰到如下丢包问题时
```
Error: Cannot find module '@buape/carbon'
Require stack:
C:\Users\54310\AppData\Roaming\npm\node_modules\openclaw\dist\ui-7MjYF8PY.js
```

先卸载再重装
```
# 卸载所有相关全局包 
npm uninstall -g openclaw @buape/carbon @larksuiteoapi/node-sdk

# 删除用户配置缓存 
Remove-Item -Recurse -Force $env:USERPROFILE\.openclaw 

# 删除npm全局安装残留 
Remove-Item -Recurse -Force $env:APPDATA\npm\node_modules\openclaw 
Remove-Item -Recurse -Force $env:APPDATA\npm\node_modules\@larksuiteoapi 
Remove-Item -Recurse -Force $env:APPDATA\npm\node_modules\@buape

# 清理 npm 缓存（防止缓存损坏）
npm cache clean --force
```

或安装缺失的包
```
# 进入 OpenClaw 全局安装目录
cd C:\Users\54310\AppData\Roaming\npm\node_modules\openclaw
npm install @larksuiteoapi/node-sdk
```

# workspace文件结构
AGENTS.md：工作规范
IDENTITY.md SOUL.md：自我认知
USER.md：对用户的认知
TOOL.md：工具调用知识
MEMORY.md 长期记忆
memory/ 短期记忆
HEARTBEAT.md 心跳机制

# 设置
## 工具-Tool Profile 选full

## ## 配置搜索功能
- git bash执行如下命令，安装skillhub
```
curl -fsSL [https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh](https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh) | bash
```

- 通过对话方式：安装openclaw-tavily-search技能
- tavily登录github账号获取apiKey
- 通过对话方式：配置API Key
- workspace TOOL.md添加提示词

# clawHub安装skill
直接复制链接，通过对话方式安装skill

github项目：awesome-openclaw-skills

摘要总结：https://clawhub.ai/mkpareek0315/summarize-pro

# openClaw配置新模型

```
# 配置信息
openclaw config
```

```
# 模型列表
openclaw model list
```

# openClaw接入微信

