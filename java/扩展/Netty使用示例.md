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