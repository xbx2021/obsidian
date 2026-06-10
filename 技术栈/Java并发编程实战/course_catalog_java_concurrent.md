# Java 并发编程实战 - 课程目录


## 00 开篇词

- [开篇词 | 你为什么需要学习并发编程？](https://time.geekbang.org/column/article/83087)


## 01 学习攻略

- [学习攻略 | 如何才能学好并发编程？](https://time.geekbang.org/column/article/83267)


## 02 第一部分：并发理论基础

- [01 | 可见性、原子性和有序性问题：并发编程Bug的源头](https://time.geekbang.org/column/article/83682)
- [02 | Java内存模型：看Java如何解决可见性和有序性问题](https://time.geekbang.org/column/article/84017)
- [03 | 互斥锁（上）：解决原子性问题](https://time.geekbang.org/column/article/84344)
- [04 | 互斥锁（下）：如何用一把锁保护多个资源？](https://time.geekbang.org/column/article/84601)
- [05 | 一不小心就死锁了，怎么办？](https://time.geekbang.org/column/article/85001)
- [06 | 用"等待-通知"机制优化循环等待](https://time.geekbang.org/column/article/85241)
- [07 | 安全性、活跃性以及性能问题](https://time.geekbang.org/column/article/85702)
- [08 | 管程：并发编程的万能钥匙](https://time.geekbang.org/column/article/86089)
- [09 | Java线程（上）：Java线程的生命周期](https://time.geekbang.org/column/article/86366)
- [10 | Java线程（中）：创建多少线程才是合适的？](https://time.geekbang.org/column/article/86666)
- [11 | Java线程（下）：为什么局部变量是线程安全的？](https://time.geekbang.org/column/article/86695)
- [12 | 如何用面向对象思想写好并发程序？](https://time.geekbang.org/column/article/87365)
- [13 | 理论基础模块热点问题答疑](https://time.geekbang.org/column/article/87749)


## 03 第二部分：并发工具类

- [14 | Lock和Condition（上）：隐藏在并发包中的管程](https://time.geekbang.org/column/article/87779)
- [15 | Lock和Condition（下）：Dubbo如何用管程实现异步转同步？](https://time.geekbang.org/column/article/88487)
- [16 | Semaphore：如何快速实现一个限流器？](https://time.geekbang.org/column/article/88499)
- [17 | ReadWriteLock：如何快速实现一个完备的缓存？](https://time.geekbang.org/column/article/88909)
- [18 | StampedLock：有没有比读写锁更快的锁？](https://time.geekbang.org/column/article/89456)
- [19 | CountDownLatch和CyclicBarrier：如何让多线程步调一致？](https://time.geekbang.org/column/article/89461)
- [20 | 并发容器：都有哪些"坑"需要我们填？](https://time.geekbang.org/column/article/90201)
- [21 | 原子类：无锁工具类的典范](https://time.geekbang.org/column/article/90515)
- [22 | Executor与线程池：如何创建正确的线程池？](https://time.geekbang.org/column/article/90771)
- [23 | Future：如何用多线程实现最优的"烧水泡茶"程序？](https://time.geekbang.org/column/article/91292)
- [24 | CompletableFuture：异步编程没那么难](https://time.geekbang.org/column/article/91569)
- [25 | CompletionService：如何批量执行异步任务？](https://time.geekbang.org/column/article/92245)
- [26 | Fork/Join：单机版的MapReduce](https://time.geekbang.org/column/article/92524)
- [27 | 并发工具类模块热点问题答疑](https://time.geekbang.org/column/article/92849)


## 04 第三部分：并发设计模式

- [28 | Immutability模式：如何利用不变性解决并发问题？](https://time.geekbang.org/column/article/92856)
- [29 | Copy-on-Write模式：不是延时策略的COW](https://time.geekbang.org/column/article/93154)
- [30 | 线程本地存储模式：没有共享，就没有伤害](https://time.geekbang.org/column/article/93745)
- [31 | Guarded Suspension模式：等待唤醒机制的规范实现](https://time.geekbang.org/column/article/94097)
- [32 | Balking模式：再谈线程安全的单例模式](https://time.geekbang.org/column/article/94604)
- [33 | Thread-Per-Message模式：最简单实用的分工方法](https://time.geekbang.org/column/article/95098)
- [34 | Worker Thread模式：如何避免重复创建线程？](https://time.geekbang.org/column/article/95525)
- [35 | 两阶段终止模式：如何优雅地终止线程？](https://time.geekbang.org/column/article/95847)
- [36 | 生产者-消费者模式：用流水线思想提高效率](https://time.geekbang.org/column/article/96168)
- [37 | 设计模式模块热点问题答疑](https://time.geekbang.org/column/article/96736)


## 05 第四部分：案例分析

- [38 | 案例分析（一）：高性能限流器Guava RateLimiter](https://time.geekbang.org/column/article/97231)
- [39 | 案例分析（二）：高性能网络应用框架Netty](https://time.geekbang.org/column/article/97622)
- [40 | 案例分析（三）：高性能队列Disruptor](https://time.geekbang.org/column/article/98134)
- [41 | 案例分析（四）：高性能数据库连接池HiKariCP](https://time.geekbang.org/column/article/98491)


## 06 第五部分：其他并发模型

- [42 | Actor模型：面向对象原生的并发模型](https://time.geekbang.org/column/article/98903)
- [43 | 软件事务内存：借鉴数据库的并发经验](https://time.geekbang.org/column/article/99251)
- [44 | 协程：更轻量级的线程](https://time.geekbang.org/column/article/99787)
- [45 | CSP模型：Golang的主力队员](https://time.geekbang.org/column/article/100098)


## 07 结束语

- [结束语 | 十年之后，初心依旧](https://time.geekbang.org/column/article/100627)
- [结课测试 | 这些Java并发编程实战的知识你都掌握了吗？](https://time.geekbang.org/column/article/243424)


## 08 用户故事

- [用户来信 | 真好，面试考到这些并发编程，我都答对了！](https://time.geekbang.org/column/article/102300)
- [3 个用户来信 | 打开一个新的并发世界](https://time.geekbang.org/column/article/105074)
