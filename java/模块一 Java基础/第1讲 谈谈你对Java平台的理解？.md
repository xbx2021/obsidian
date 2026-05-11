![](assets/第1讲%20谈谈你对Java平台的理解？/file-20260511104121404.png)

从你接触 Java 开发到现在，你对 Java 最直观的印象是什么呢？是它宣传的 “Write once, run anywhere”，还是目前看已经有些过于形式主义的语法呢？你对于 Java 平台到底了解到什么程度？请你先停下来总结思考一下。

今天我要问你的问题是，**谈谈你对 Java 平台的理解？“Java 是解释执行”，这句话正确吗？**

# 典型回答

Java 本身是一种面向对象的语言，最显著的特性有两个方面，一是所谓的 **“书写一次，到处运行”** （Write once, run anywhere），能够非常容易地获得跨平台能力；另外就是**垃圾收集**（GC, Garbage Collection），Java 通过垃圾收集器（Garbage Collector）回收分配内存，大部分情况下，程序员不需要自己操心内存的分配和回收。

我们日常会接触到 JRE（Java Runtime Environment）或者 JDK（Java Development Kit）。 **JRE，也就是 Java 运行环境，包含了 JVM 和 Java 类库，以及一些模块等**。而 **JDK 可以看作是 JRE 的一个超集，提供了更多工具，比如编译器、各种诊断工具等。**

