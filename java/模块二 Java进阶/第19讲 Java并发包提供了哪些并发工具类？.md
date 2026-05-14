![](assets/第19讲%20Java并发包提供了哪些并发工具类？/file-20260514155140303.png)

通过前面的学习，我们一起回顾了线程、锁等各种并发编程的基本元素，也逐步涉及了 Java 并发包中的部分内容，相信经过前面的热身，我们能够更快地理解 Java 并发包。

今天我要问你的问题是，**Java 并发包提供了哪些并发工具类？**

# 典型回答

我们通常所说的并发包也就是 java.util.concurrent 及其子包，集中了 Java 并发的各种基础工具类，具体主要包括几个方面：

- 提供了比 synchronized 更加高级的各种同步结构，包括 **CountDownLatch**、**CyclicBarrier**、**Semaphore** 等，可以实现更加丰富的多线程操作，比如利用 Semaphore 作为资源控制器，限制同时进行工作的线程数量。

- 各种线程安全的容器，比如最常见的 **ConcurrentHashMap**、有序的 **ConcurrentSkipListMap**，或者通过类似快照机制，实现线程安全的动态数组 **CopyOnWriteArrayList** 等。

- 各种并发队列实现，如各种 **BlockingQueue** 实现，比较典型的 **ArrayBlockingQueue**、 **SynchronousQueue** 或针对特定场景的 **PriorityBlockingQueue** 等。

- 强大的 **Executor** 框架，可以创建各种不同类型的线程池，调度任务运行等，绝大部分情况下，不再需要自己从头实现线程池和任务调度器。

# 考点分析

