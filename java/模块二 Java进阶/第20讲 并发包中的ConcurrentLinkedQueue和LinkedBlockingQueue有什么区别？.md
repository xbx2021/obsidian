![](assets/第20讲%20并发包中的ConcurrentLinkedQueue和LinkedBlockingQueue有什么区别？/file-20260515102812594.png)
在上一讲中，我分析了 Java 并发包中的部分内容，今天我来介绍一下线程安全队列。Java 标准库提供了非常多的线程安全队列，很容易混淆。

今天我要问你的问题是，**并发包中的 ConcurrentLinkedQueue 和 LinkedBlockingQueue 有什么区别？**

# 典型回答

有时候我们把并发包下面的所有容器都习惯叫作并发容器，但是严格来讲，类似 ConcurrentLinkedQueue 这种“Concurrent*”容器，才是真正代表并发。

关于问题中它们的区别：

- Concurrent 类型基于 lock-free，在常见的多线程访问场景，一般可以提供较高吞吐量。

- 而 LinkedBlockingQueue 内部则是基于锁，并提供了 BlockingQueue 的等待性方法。
