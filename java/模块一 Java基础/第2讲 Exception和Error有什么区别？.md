![](assets/第2讲%20Exception和Error有什么区别？/file-20260511141119896.png)
世界上存在永远不会出错的程序吗？也许这只会出现在程序员的梦中。随着编程语言和软件的诞生，异常情况就如影随形地纠缠着我们，只有正确处理好意外情况，才能保证程序的可靠性。

Java 语言在设计之初就提供了相对完善的异常处理机制，这也是 Java 得以大行其道的原因之一，因为这种机制大大降低了编写和维护可靠程序的门槛。如今，异常处理机制已经成为现代编程语言的标配。

今天我要问你的问题是，**请对比 Exception 和 Error，另外，运行时异常与一般异常有什么区别？**

# 典型回答

Exception 和 Error 都是继承了 Throwable 类，在 Java 中**只有 Throwable 类型的实例才可以被抛出（throw）或者捕获（catch）**，它是异常处理机制的基本组成类型。

Exception 和 Error 体现了 Java 平台设计者对不同异常情况的分类。**Exception 是程序正常运行中，可以预料的意外情况，可能并且应该被捕获，进行相应处理**。

Error 是指在正常情况下，不大可能出现的情况，**绝大部分的 Error 都会导致程序（比如 JVM 自身）处于非正常的、不可恢复状态**。既然是非正常情况，所以不便于也不需要捕获，常见的比如 OutOfMemoryError 之类，都是 Error 的子类。

Exception 又分为**可检查**（checked）异常和**不检查**（unchecked）异常，**可检查异常在源代码里必须显式地进行捕获处理**，这是编译期检查的一部分。前面我介绍的不可查的 Error，是 Throwable 不是 Exception。

**不检查异常就是所谓的运行时异常**，类似 NullPointerException、ArrayIndexOutOfBoundsException 之类，通常是可以编码避免的逻辑错误，具体根据需要来判断是否需要捕获，并不会在编译期强制要求。


# 考点分析

分析 Exception 和 Error 的区别，是从概念角度考察了 Java 处理机制。总的来说，还处于理解的层面，面试者只要阐述清楚就好了。

我们在日常编程中，如何处理好异常是比较考验功底的，我觉得需要掌握两个方面。

**第一，理解 Throwable、Exception、Error 的设计和分类**。比如，掌握那些应用最为广泛的子类，以及如何自定义异常等。

很多面试官会进一步追问一些细节，比如，你了解哪些 Error、Exception 或者 RuntimeException？我画了一个简单的类图，并列出来典型例子，可以给你作为参考，至少做到基本心里有数。
![](assets/第2讲%20Exception和Error有什么区别？/file-20260511143043715.png)
其中有些子类型，最好重点理解一下，比如 NoClassDefFoundError 和 ClassNotFoundException 有什么区别，这也是个经典的入门题目。

