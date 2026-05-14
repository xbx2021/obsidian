![](assets/第16讲%20synchronized底层如何实现？什么是锁的升级、降级？/file-20260514102451632.png)

我在上一讲对比和分析了 synchronized 和 ReentrantLock，算是专栏进入并发编程阶段的热身，相信你已经对线程安全，以及如何使用基本的同步机制有了基础，今天我们将深入了解 synchronize 底层机制，分析其他锁实现和应用场景。

今天我要问你的问题是 ，**synchronized 底层如何实现？什么是锁的升级、降级？**

# 典型回答

在回答这个问题前，先简单复习一下上一讲的知识点。synchronized 代码块是由一对儿 **monitorenter/monitorexit** 指令实现的，Monitor 对象是同步的基本实现[单元](https://docs.oracle.com/javase/specs/jls/se10/html/jls-8.html#d5e13622)。

在 Java 6 之前，Monitor 的实现完全是依靠操作系统内部的互斥锁，因为需要进行用户态到内核态的切换，所以同步操作是一个无差别的重量级操作。

现代的（Oracle）JDK 中，JVM 对此进行了大刀阔斧地改进，提供了三种不同的 Monitor 实现，也就是常说的三种不同的锁：**偏斜锁**（Biased Locking）、**轻量级锁**和**重量级锁**，大大改进了其性能。

所谓锁的升级、降级，就是 JVM 优化 synchronized 运行的机制，**当 JVM 检测到不同的竞争状况时，会自动切换到适合的锁实现，这种切换就是锁的升级、降级**。

当没有竞争出现时，默认会使用偏斜锁。JVM 会利用 CAS 操作（[compare and swap](https://en.wikipedia.org/wiki/Compare-and-swap)），在对象头上的 Mark Word 部分设置线程 ID，以表示这个对象偏向于当前线程，所以并不涉及真正的互斥锁。这样做的假设是基于在很多应用场景中，大部分对象生命周期中最多会被一个线程锁定，使用偏斜锁可以降低无竞争开销。

如果有另外的线程试图锁定某个已经被偏斜锁过的对象，JVM 就需要撤销（revoke）偏斜锁，并切换到轻量级锁实现。轻量级锁依赖 CAS 操作 Mark Word 来试图获取锁，如果重试成功，就使用普通的轻量级锁；否则，进一步升级为重量级锁。

我注意到有的观点认为 Java 不会进行锁降级。实际上据我所知，锁降级确实是会发生的，当 JVM 进入安全点（SafePoint）的时候，会检查是否有闲置的 Monitor，然后试图进行降级。

# 考点分析

今天的问题主要是考察你对 Java 内置锁实现的掌握，也是并发的经典题目。我在前面给出的典型回答，涵盖了一些基本概念。如果基础不牢，有些概念理解起来就比较晦涩，我建议还是尽量理解和掌握，即使有不懂的也不用担心，在后续学习中还会逐步加深认识。

我个人认为，能够基础性地理解这些概念和机制，其实对于大多数并发编程已经足够了，毕竟大部分工程师未必会进行更底层、更基础的研发，很多时候解决的是知道与否，真正的提高还要靠实践踩坑。

后面我会进一步分析：

- 从源码层面，稍微展开一些 synchronized 的底层实现，并补充一些上面答案中欠缺的细节，有同学反馈这部分容易被问到。如果你对 Java 底层源码有兴趣，但还没有找到入手点，这里可以成为一个切入点。

- 理解并发包中 java.util.concurrent.lock 提供的其他锁实现，毕竟 Java 可不是只有 ReentrantLock 一种显式的锁类型，我会结合代码分析其使用。

# 知识扩展

我在上一讲提到过 synchronized 是 JVM 内部的 Intrinsic Lock，所以偏斜锁、轻量级锁、重量级锁的代码实现，并不在核心类库部分，而是在 JVM 的代码中。

Java 代码运行可能是解释模式也可能是编译模式（如果不记得，请复习专栏第 1 讲），所以对应的同步逻辑实现，也会分散在不同模块下，比如，解释器版本就是：

[src/hotspot/share/interpreter/interpreterRuntime.cpp](http://hg.openjdk.java.net/jdk/jdk/file/6659a8f57d78/src/hotspot/share/interpreter/interpreterRuntime.cpp)

为了简化便于理解，我这里会专注于通用的基类实现：

[src/hotspot/share/runtime/](http://hg.openjdk.java.net/jdk/jdk/file/6659a8f57d78/src/hotspot/share/runtime/)

另外请注意，链接指向的是最新 JDK 代码库，所以可能某些实现与历史版本有所不同。

首先，synchronized 的行为是 JVM runtime 的一部分，所以我们需要先找到 Runtime 相关的功能实现。通过在代码中查询类似“monitor_enter”或“Monitor Enter”，很直观的就可以定位到：

[sharedRuntime.cpp/hpp](http://hg.openjdk.java.net/jdk/jdk/file/6659a8f57d78/src/hotspot/share/runtime/sharedRuntime.cpp) ，它是解释器和编译器运行时的基类。

[synchronizer.cpp/hpp](https://hg.openjdk.java.net/jdk/jdk/file/896e80158d35/src/hotspot/share/runtime/synchronizer.cpp)， JVM 同步相关的各种基础逻辑。

在 sharedRuntime.cpp 中，下面代码体现了 synchronized 的主要逻辑。
```cpp
Handle h_obj(THREAD, obj);
  if (UseBiasedLocking) {
    // Retry fast entry if bias is revoked to avoid unnecessary inflation
    ObjectSynchronizer::fast_enter(h_obj, lock, true, CHECK);
  } else {
    ObjectSynchronizer::slow_enter(h_obj, lock, CHECK);
  }
```

其实现可以简单进行分解：

- **UseBiasedLocking** 是一个检查，因为，在 JVM 启动时，我们可以指定是否开启偏斜锁。

偏斜锁并不适合所有应用场景，撤销操作（revoke）是比较重的行为，只有当存在较多不会真正竞争的 synchronized 块儿时，才能体现出明显改善。实践中对于偏斜锁的一直是有争议的，有人甚至认为，当你需要大量使用并发类库时，往往意味着你不需要偏斜锁。从具体选择来看，我还是建议需要在实践中进行测试，根据结果再决定是否使用。

