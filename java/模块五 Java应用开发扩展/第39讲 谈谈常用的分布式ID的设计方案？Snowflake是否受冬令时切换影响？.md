![](assets/第39讲%20谈谈常用的分布式ID的设计方案？Snowflake是否受冬令时切换影响？/file-20260519113954305.png)


专栏的绝大部分主题都侧重于 Java 语言和虚拟机，基本都是单机模式下的问题，今天我会补充一个分布式相关的问题。严格来说，分布式并不算是 Java 领域，而是一个单独的大主题，但确实也会在 Java 技术岗位面试中被涉及。在准备面试时，如果有丰富的分布式系统经验当然好；如果没有，你可以选择典型问题和基础技术进行适当准备。关于分布式，我自身的实战经验也非常有限，专栏里就谈谈从理论出发的一些思考。

今天我要问你的问题是，**谈谈常用的分布式 ID 的设计方案？Snowflake 是否受冬令时切换影响？**

# 典型回答

首先，我们需要明确通常的分布式 ID 定义，基本的要求包括：

- 全局唯一，区别于单点系统的唯一，全局是要求分布式系统内唯一。

- 有序性，通常都需要保证生成的 ID 是有序递增的。例如，在数据库存储等场景中，有序 ID 便于确定数据位置，往往更加高效。

目前业界的方案很多，典型方案包括：

- 基于数据库自增序列的实现。这种方式优缺点都非常明显，好处是简单易用，但是在扩展性和可靠性等方面存在局限性。

- 基于 Twitter 早期开源的[Snowflake](https://github.com/twitter/snowflake)的实现，以及相关改动方案。这是目前应用相对比较广泛的一种方式，其结构定义你可以参考下面的示意图。
![](assets/第39讲%20谈谈常用的分布式ID的设计方案？Snowflake是否受冬令时切换影响？/file-20260519114448548.png)

整体长度通常是 64 （1 + 41 + 10+ 12 = 64）位，适合使用 Java 语言中的 long 类型来存储。

头部是 1 位的正负标识位。

紧跟着的高位部分包含 41 位时间戳，通常使用 System.currentTimeMillis()。

后面是 10 位的 WorkerID，标准定义是 5 位数据中心 + 5 位机器 ID，组成了机器编号，以区分不同的集群节点。

最后的 12 位就是单位毫秒内可生成的序列号数目的理论极限。

Snowflake 的官方版本是基于 Scala 语言，Java 等其他语言的[参考实现](https://github.com/relops/snowflake)有很多，是一种非常简单实用的方式，具体位数的定义是可以根据分布式系统的真实场景进行修改的，并不一定要严格按照示意图中的设计。

- Redis、ZooKeeper、MongoDB 等中间件，也都有各种唯一 ID 解决方案。其中一些设计也可以算作是 Snowflake 方案的变种。例如，MongoDB 的[ObjectId](https://mongodb.github.io/node-mongodb-native/2.0/tutorials/objectid/)提供了一个 12 byte（96 位）的 ID 定义，其中 32 位用于记录以秒为单位的时间，机器 ID 则为 24 位，16 位用作进程 ID，24 位随机起始的计数序列。

- 国内的一些大厂开源了其自身的部分分布式 ID 实现，InfoQ 就曾经介绍过微信的[seqsvr](http://www.infoq.com/cn/articles/wechat-serial-number-generator-architecture)，它采取了相对复杂的两层架构，并根据社交应用的数据特点进行了针对性设计，具体请参考相关[代码实现](https://github.com/nebula-im/seqsvr)。另外，[百度](https://github.com/baidu/uid-generator/blob/master/README.zh_cn.md)、美团等也都有开源或者分享了不同的分布式 ID 实现，都可以进行参考。