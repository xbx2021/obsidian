![](assets/第26讲%20如何监控和诊断JVM堆内和堆外内存使用？/file-20260516100114163.png)

上一讲我介绍了 JVM 内存区域的划分，总结了相关的一些概念，今天我将结合 JVM 参数、工具等方面，进一步分析 JVM 内存结构，包括外部资料相对较少的堆外部分。

今天我要问你的问题是，**如何监控和诊断 JVM 堆内和堆外内存使用？**

# 典型回答

了解 JVM 内存的方法有很多，具体能力范围也有区别，简单总结如下：

- 可以使用综合性的图形化工具，如 JConsole、VisualVM（注意，从 Oracle JDK 9 开始，VisualVM 已经不再包含在 JDK 安装包中）等。这些工具具体使用起来相对比较直观，直接连接到 Java 进程，然后就可以在图形化界面里掌握内存使用情况。

以 JConsole 为例，其内存页面可以显示常见的**堆内存**和**各种堆外部分**使用状态。

- 也可以使用命令行工具进行运行时查询，如 **jstat 和 jmap 等工具都提供了一些选项，可以查看堆、方法区等使用数据**。

- 或者，也可以**使用 jmap 等提供的命令，生成堆转储（Heap Dump）文件，然后利用 jhat 或 Eclipse MAT 等堆转储分析工具进行详细分析**。

- 如果你使用的是 Tomcat、Weblogic 等 Java EE 服务器，这些服务器同样提供了内存管理相关的功能。

- 另外，从某种程度上来说，GC 日志等输出，同样包含着丰富的信息。

- 这里有一个相对特殊的部分，就是是堆外内存中的直接内存，前面的工具基本不适用，可以使用 JDK 自带的 Native Memory Tracking（NMT）特性，它会从 JVM 本地内存分配的角度进行解读。

# 考点分析

今天选取的问题是 Java 内存管理相关的基础实践，对于普通的内存问题，掌握上面我给出的典型工具和方法就足够了。这个问题也可以理解为考察两个基本方面能力，第一，你是否真的理解了 JVM 的内部结构；第二，具体到特定内存区域，应该使用什么工具或者特性去定位，可以用什么参数调整。

对于 JConsole 等工具的使用细节，我在专栏里不再赘述，如果你还没有接触过，你可以参考[JConsole 官方教程](https://docs.oracle.com/javase/7/docs/technotes/guides/management/jconsole.html)。我这里特别推荐[Java Mission Control](http://www.oracle.com/technetwork/java/javaseproducts/mission-control/java-mission-control-1998576.html)（JMC），这是一个非常强大的工具，不仅仅能够使用[JMX](https://en.wikipedia.org/wiki/Java_Management_Extensions)进行普通的管理、监控任务，还可以配合[Java Flight Recorder](https://docs.oracle.com/javacomponents/jmc-5-4/jfr-runtime-guide/about.htm#JFRUH171)（JFR）技术，以非常低的开销，收集和分析 JVM 底层的 Profiling 和事件等信息。目前， Oracle 已经将其开源，如果你有兴趣请可以查看 OpenJDK 的[Mission Control](http://openjdk.java.net/projects/jmc/)项目。

关于内存监控与诊断，我会在知识扩展部分结合 JVM 参数和特性，尽量从庞杂的概念和 JVM 参数选项中，梳理出相对清晰的框架：

- 细化对各部分内存区域的理解，堆内结构是怎样的？如何通过参数调整？
- 堆外内存到底包括哪些部分？具体大小受哪些因素影响？

# 知识扩展

今天的分析，我会结合相关 JVM 参数和工具，进行对比以加深你对内存区域更细粒度的理解。

## 堆内存结构

首先，堆内部是什么结构？

对于堆内存，我在上一讲介绍了最常见的新生代和老年代的划分，其内部结构随着 JVM 的发展和新 GC 方式的引入，可以有不同角度的理解，下图就是年代视角的堆结构示意图。
![](assets/第26讲%20如何监控和诊断JVM堆内和堆外内存使用？/file-20260516101513465.png)

你可以看到，按照通常的 GC 年代方式划分，Java 堆内分为：

1. 新生代

新生代是大部分对象创建和销毁的区域，在通常的 Java 应用中，绝大部分对象生命周期都是很短暂的。其内部又分为 Eden 区域，作为对象初始分配的区域；两个 Survivor，有时候也叫 from、to 区域，被用来放置从 Minor GC 中保留下来的对象。

- JVM 会随意选取一个 Survivor 区域作为“to”，然后会在 GC 过程中进行区域间拷贝，也就是将 Eden 中存活下来的对象和 from 区域的对象，拷贝到这个“to”区域。这种设计主要是为了防止内存的碎片化，并进一步清理无用对象。

- 从内存模型而不是垃圾收集的角度，对 Eden 区域继续进行划分，Hotspot JVM 还有一个概念叫做 **Thread Local Allocation Buffer（TLAB）**，据我所知所有 OpenJDK 衍生出来的 JVM 都提供了 TLAB 的设计。这是 JVM 为每个线程分配的一个私有缓存区域，否则，多线程同时分配内存时，为避免操作同一地址，可能需要使用加锁等机制，进而影响分配速度，你可以参考下面的示意图。从图中可以看出，TLAB 仍然在堆上，它是分配在 Eden 区域内的。其内部结构比较直观易懂，start、end 就是起始地址，top（指针）则表示已经分配到哪里了。所以我们分配新对象，JVM 就会移动 top，当 top 和 end 相遇时，即表示该缓存已满，JVM 会试图再从 Eden 里分配一块儿。
![](assets/第26讲%20如何监控和诊断JVM堆内和堆外内存使用？/file-20260516102203822.png)

2. 老年代

放置长生命周期的对象，通常都是从 Survivor 区域拷贝过来的对象。当然，也有特殊情况，我们知道普通的对象会被分配在 TLAB 上；如果对象较大，JVM 会试图直接分配在 Eden 其他位置上；如果对象太大，完全无法在新生代找到足够长的连续空闲空间，JVM 就会直接分配到老年代。

3. 永久代

这部分就是早期 Hotspot JVM 的方法区实现方式了，储存 Java 类元数据、常量池、Intern 字符串缓存，在 JDK 8 之后就不存在永久代这块儿了。

那么，我们如何利用 JVM 参数，直接影响堆和内部区域的大小呢？我来简单总结一下：

## 堆内存JVM 参数

- 最大堆体积
```bash
-Xmx value
```

- 初始的最小堆体积
```bash
-Xms value
```

- 老年代和新生代的比例
```bash
-XX:NewRatio=value
```

默认情况下，这个数值是 2，意味着老年代是新生代的 2 倍大；换句话说，新生代是堆大小的 1/3。

- 当然，也可以不用比例的方式调整新生代的大小，直接指定下面的参数，设定具体的内存大小数值。
```bash
-XX:NewSize=value
```

- Eden 和 Survivor 的大小是按照比例设置的，如果 SurvivorRatio 是 8，那么 Survivor 区域就是 Eden 的 1/8 大小，也就是新生代的 1/10，因为 YoungGen=Eden + 2* Survivor，JVM 参数格式是