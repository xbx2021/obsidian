## 什么是WSL2？

- 以前 Windows 想用 Linux 命令（`git`、`curl`、`apt`、`bash`）很麻烦
- WSL2 就是微软官方做的一个**轻量级 Linux 环境**
- 本质是**轻量化虚拟机**，但比 VMware、VirtualBox 小得多、快得多

## 能干什么？

- 运行 **Linux 命令**：`bash`、`ls`、`grep`、`sudo`、`apt`
- 装 Linux 软件：Python、Node、Docker、Nginx、MySQL
- 做开发：前端、后端、爬虫、深度学习环境

## 安装
win+R命令行
```bash
wsl --install
```

## 使用
https://learn.microsoft.com/zh-cn/windows/wsl/

常用命令
```bash
# 查看发行版列表 确认 VERSION 为 2
wsl -l -v

# 启动默认发行版 直接进入 Linux 终端
wsl

# 关闭 WSL 停止所有 WSL 实例
wsl --shutdown

# 列出可用发行版 查看可安装的发行版
wsl --list --online
```
