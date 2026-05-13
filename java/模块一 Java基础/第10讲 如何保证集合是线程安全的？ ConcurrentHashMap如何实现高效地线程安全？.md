![](assets/第10讲%20如何保证集合是线程安全的？%20ConcurrentHashMap如何实现高效地线程安全？/file-20260513094943779.png)
我在之前两讲介绍了 Java 集合框架的典型容器类，它们绝大部分都不是线程安全的，仅有的线程安全实现，比如 Vector、Stack，在性能方面也远不尽如人意。幸好 Java 语言提供了并发包（java.util.concurrent），为高度并发需求提供了更加全面的工具支持。

今天我要问你的问题是，**如何保证容器是线程安全的？ConcurrentHashMap 如何实现高效地线程安全？**

# 典型回答

Java 提供了不同层面的线程安全支持。在传统集合框架内部，除了 Hashtable 等同步容器，还提供了所谓的同步包装器（Synchronized Wrapper），我们可以调用 Collections 工具类提供的包装方法，来获取一个同步的包装容器（如 Collections.synchronizedMap），但是它们都是利用非常粗粒度的同步方式，在高并发情况下，性能比较低下。

