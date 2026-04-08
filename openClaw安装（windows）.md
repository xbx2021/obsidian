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





碰到的问题：
```
Error: Cannot find module '@buape/carbon'
Require stack:
C:\Users\54310\AppData\Roaming\npm\node_modules\openclaw\dist\ui-7MjYF8PY.js
```
