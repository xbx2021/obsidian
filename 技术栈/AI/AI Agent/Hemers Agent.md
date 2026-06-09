要先安装WSL2（Windows Subsystem for Linux 2，Windows 下的 Linux 子系统（第二代））
# 什么是WSL2？

- 以前 Windows 想用 Linux 命令（`git`、`curl`、`apt`、`bash`）很麻烦
- WSL2 就是微软官方做的一个**轻量级 Linux 环境**
- 本质是**轻量化虚拟机**，但比 VMware、VirtualBox 小得多、快得多

# 能干什么？

- 运行 **Linux 命令**：`bash`、`ls`、`grep`、`sudo`、`apt`
- 装 Linux 软件：Python、Node、Docker、Nginx、MySQL
- 做开发：前端、后端、爬虫、深度学习环境

# 安装Hemers Agent
安装WSL
```bash
wsl --install
```

进入Ubuntu
```bash
wls
```

安装Hemers Agent，使用国内镜像源安装
```bash
curl -fsSL https://res1.hermesagent.org.cn/install.sh | bash
```

刷新环境变量
```bash
source ~/.bashrc
```

Hemers命令
```bash
hermes --version    查看版本
hermes              启动
hermes setup        配置 API Key 和设置
hermes config       查看 / 编辑配置
hermes gateway install 安装网关服务
```

Hermes Path
```bash
Config:       /home/xiebx/.hermes/config.yaml
Secrets:      /home/xiebx/.hermes/.env
Install:      /home/xiebx/.hermes/hermes-agent
```

# 连接微信
通过 `hermes setup` 设置连接微信，扫码配对后，微信会接收到如下配对信息，将信息在终端发送给Hermes即完成配置
```bash
hermes pairing approve weixin ABC123
```
需要启动网关才能继续通信
```bash
hermes gateway start
```
