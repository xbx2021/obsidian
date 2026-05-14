![](assets/第16讲%20synchronized底层如何实现？什么是锁的升级、降级？/file-20260514102451632.png)

我在上一讲对比和分析了 synchronized 和 ReentrantLock，算是专栏进入并发编程阶段的热身，相信你已经对线程安全，以及如何使用基本的同步机制有了基础，今天我们将深入了解 synchronize 底层机制，分析其他锁实现和应用场景。

今天我要问你的问题是 ，**synchronized 底层如何实现？什么是锁的升级、降级？**

# 典型回答

在回答这个问题前，先简单复习一下上一讲的知识点。synchronized 代码块是由一对儿 **monitorenter/monitorexit** 指令实现的，Monitor 对象是同步的基本实现[单元](https://docs.oracle.com/javase/specs/jls/se10/html/jls-8.html#d5e13622)。

在 Java 6 之前，Monitor 的实现完全是依靠操作系统内部的互斥锁，因为需要进行用户态到内核态的切换，所以同步操作是一个无差别的重量级操作。

现代的（Oracle）JDK 中，JVM 对此进行了大刀阔斧地改进，提供了三种不同的 Monitor 实现，也就是常说的三种不同的锁：**偏斜锁**（Biased Locking）、**轻量级锁**和**重量级锁**，大大改进了其性能。

所谓锁的升级、降级，就是 JVM 优化 synchronized 运行的机制，当 JVM 检测到不同的竞争状况时，会自动切换到适合的锁实现，这种切换就是锁的升级、降级。