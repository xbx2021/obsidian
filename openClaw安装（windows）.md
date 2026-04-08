- 下载并安装Node.js  22.x 或更高版本

- 国内网络慢，安装前务必设置镜像源
```
# npm 
npm config set registry https://registry.npmmirror.com/
```

- 全局安装 OpenClaw
````
npm install -g openclaw@latest
````

- 运行初始化向导
```
openclaw onboard
```

- OpenClaw 自带诊断工具，自动检测问题：
```
openclaw doctor
```





碰到如下缺包的问题时，
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