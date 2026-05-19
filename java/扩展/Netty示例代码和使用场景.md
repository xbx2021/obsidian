# Netty 极简使用示例（服务端 + 客户端）
我给你写一个**最精简、可直接运行**的 Netty 示例，包含 **TCP 服务端** 和 **客户端**，实现客户端发消息 → 服务端接收并回显。

## 1. 先加依赖（Maven）
```xml
<dependencies>
    <!-- Netty 核心依赖 -->
    <dependency>
        <groupId>io.netty</groupId>
        <artifactId>netty-all</artifactId>
        <version>4.1.100.Final</version>
    </dependency>
</dependencies>
```

---

## 2. Netty 服务端（监听端口，接收消息）
```java
import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.codec.string.StringEncoder;

/**
 * Netty 服务端：监听 8888 端口，接收客户端消息并回显
 */
public class NettyServer {
    public static void main(String[] args) throws InterruptedException {
        // 1. 创建两组线程池（boss 接收连接，worker 处理读写）
        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();

        try {
            // 2. 服务端启动助手
            ServerBootstrap bootstrap = new ServerBootstrap();
            bootstrap.group(bossGroup, workerGroup)
                     .channel(NioServerSocketChannel.class)  // 使用 NIO 通道
                     .option(ChannelOption.SO_BACKLOG, 100)   // 等待连接队列
                     .childHandler(new ChannelInitializer<SocketChannel>() {
                         @Override
                         protected void initChannel(SocketChannel ch) {
                             ChannelPipeline pipeline = ch.pipeline();
                             // 字符串编解码器（直接收发字符串）
                             pipeline.addLast(new StringDecoder());
                             pipeline.addLast(new StringEncoder());
                             // 自定义业务处理器
                             pipeline.addLast(new ServerHandler());
                         }
                     });

            // 3. 绑定端口，同步启动
            ChannelFuture future = bootstrap.bind(8888).sync();
            System.out.println("Netty 服务端已启动，监听端口：8888");

            // 等待服务端关闭
            future.channel().closeFuture().sync();
        } finally {
            // 优雅关闭线程池
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }

    // 服务端消息处理逻辑
    static class ServerHandler extends SimpleChannelInboundHandler<String> {
        @Override
        protected void channelRead0(ChannelHandlerContext ctx, String msg) {
            System.out.println("收到客户端消息：" + msg);
            // 回显给客户端
            ctx.writeAndFlush("服务端已收到：" + msg);
        }

        // 异常处理
        @Override
        public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
            cause.printStackTrace();
            ctx.close();
        }
    }
}
```

---

## 3. Netty 客户端（连接服务端，发消息）
```java
import io.netty.bootstrap.Bootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.codec.string.StringEncoder;

/**
 * Netty 客户端：连接 127.0.0.1:8888，发送消息并接收回显
 */
public class NettyClient {
    public static void main(String[] args) throws InterruptedException {
        // 1. 客户端只需要一个线程组
        EventLoopGroup group = new NioEventLoopGroup();

        try {
            // 2. 客户端启动助手
            Bootstrap bootstrap = new Bootstrap();
            bootstrap.group(group)
                     .channel(NioSocketChannel.class)
                     .handler(new ChannelInitializer<SocketChannel>() {
                         @Override
                         protected void initChannel(SocketChannel ch) {
                             ChannelPipeline pipeline = ch.pipeline();
                             // 字符串编解码器
                             pipeline.addLast(new StringDecoder());
                             pipeline.addLast(new StringEncoder());
                             // 客户端处理器
                             pipeline.addLast(new ClientHandler());
                         }
                     });

            // 3. 连接服务端
            ChannelFuture future = bootstrap.connect("127.0.0.1", 8888).sync();
            System.out.println("已连接 Netty 服务端");

            // 发送消息
            future.channel().writeAndFlush("Hello Netty!");

            // 等待客户端关闭
            future.channel().closeFuture().sync();
        } finally {
            group.shutdownGracefully();
        }
    }

    // 客户端消息处理
    static class ClientHandler extends SimpleChannelInboundHandler<String> {
        @Override
        protected void channelRead0(ChannelHandlerContext ctx, String msg) {
            System.out.println("收到服务端回显：" + msg);
        }
    }
}
```

---

## 4. 运行方式
1. **先启动 NettyServer**
2. **再启动 NettyClient**

### 运行结果
- **服务端控制台**
  ```
  Netty 服务端已启动，监听端口：8888
  收到客户端消息：Hello Netty!
  ```
- **客户端控制台**
  ```
  已连接 Netty 服务端
  收到服务端回显：服务端已收到：Hello Netty!
  ```

---

## 核心概念（一看就懂）
1. **EventLoopGroup**：Netty 的线程池，负责处理连接、读写事件
2. **ChannelPipeline**：通道流水线，添加**编码器、解码器、业务处理器**
3. **Handler**：真正处理消息的业务逻辑
4. **StringDecoder/StringEncoder**：直接收发字符串，不用自己处理字节

---

### 总结
1. 这是 Netty **最经典、最简**的 TCP 通信示例
2. 服务端监听 8888，客户端连接后发送消息，服务端回显
3. 代码可直接复制运行，适合入门学习 Netty 基本用法
4. 你可以轻松改成自定义协议、心跳、长连接等功能


# Netty 主流使用场景（精简实用版）
## 一、核心定位
**高性能 NIO 网络通信框架**，解决 Java BIO 阻塞、IO 效率低、高并发难问题，主打**高并发、高吞吐、低延迟**。

## 二、实际业务场景
### 1. 互联网后端服务
- 微服务**RPC 通信**：Dubbo、gRPC 底层通信依赖 Netty
- 网关服务：API 网关、服务网关内网转发
- 长连接服务：后台服务间持久通信

### 2. 即时通讯 IM
- 聊天软件：私聊、群聊、消息推送
- 直播弹幕、实时互动消息
- 企业内部即时通讯系统

### 3. 物联网 IoT
- 设备上报数据：传感器、智能硬件上报
- 设备远程控制、指令下发
- MQTT/Modbus 协议服务端

### 4. 游戏服务器
- 手游/端游**游戏逻辑服、网关服**
- 实时对战、帧同步、房间通信
- 游戏心跳保活、玩家状态同步

### 5. 大数据中间件
- 消息队列：RocketMQ、Kafka 网络层
- 数据采集、日志实时推送
- 流式计算节点数据互通

### 6. 金融支付系统
- 支付网关、银行接口对接
- 交易报文实时传输、对账通信
- 高并发交易请求转发

### 7. 推送服务
- APP 离线推送、消息推送
- 站内信、运营活动实时推送
- 移动端长连接保活

### 8. 自研私有协议
- 自定义二进制通信协议
- 加密私有报文传输
- 内网专属通信框架

### 9. 运维/监控
- 远程命令执行、运维通道
- 服务器状态实时监控上报
- 批量机器管理通信

### 10. 串口/网络硬件对接
- 工控设备、门禁、摄像头对接
- 安防设备数据接收

## 三、适合用 Netty 的场景特点
1. **高并发连接**：上万长连接同时在线
2. **实时性要求高**：毫秒级消息响应
3. **长连接居多**：不断开、心跳保活
4. **自定义协议**：不用 HTTP，自己定义报文
5. **IO 密集型**：大量网络读写

## 四、不适合用 Netty
1. 简单短接口（直接用 SpringMVC/HTTP 足够）
2. 低并发、小流量内部系统
3. 只做简单 HTTP 接口业务

## 五、主流知名开源项目都在用
- Dubbo、RocketMQ、Elasticsearch
- Redis Java 客户端、Spark、Flink
- Spring Cloud 部分通信组件
- 大部分游戏服务器、IM 系统

需要我给你整理**Netty 学习路线 + 常用组件清单**吗？