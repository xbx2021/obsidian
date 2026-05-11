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

## **第一，理解 Throwable、Exception、Error 的设计和分类**。

比如，掌握那些应用最为广泛的子类，以及如何自定义异常等。

很多面试官会进一步追问一些细节，比如，你了解哪些 Error、Exception 或者 RuntimeException？我画了一个简单的类图，并列出来典型例子，可以给你作为参考，至少做到基本心里有数。
![](assets/第2讲%20Exception和Error有什么区别？/file-20260511143043715.png)
其中有些子类型，最好重点理解一下，比如 NoClassDefFoundError 和 ClassNotFoundException 有什么区别，这也是个经典的入门题目。

### **NoClassDefFoundError 和 ClassNotFoundException 区别**
 
 **ClassNotFoundException**

1. **类型**：受检异常 `Exception`
2. **触发时机**：**运行时**，**主动尝试加载类**时找不到
3. **核心原因**：类**根本不在运行时 classpath 中**
4. **常见代码**：
 ```java
Class.forName("com.mysql.jdbc.Driver"); // 找不到驱动类 → 抛 ClassNotFoundException
 ```
5. **场景**：缺少 jar 包、依赖冲突、类名写错、classpath 配置错误

**NoClassDefFoundError**

1. **类型**：严重错误 `Error`
2. **触发时机**：**运行时**，类**已经编译存在**，但 JVM 找不到**类的定义**
3. **核心原因**：
- 类的**静态代码块 / 构造方法执行失败**（类初始化失败）
- 类被加载后，**对应的 class 文件被删除 / 替换**
- 类依赖的其他类加载失败

4. **表现**：编译完全正常，运行直接崩
5. **示例**：
```java
public class Test {
    static {
        // 静态代码块抛异常 → 类初始化失败
        int i = 1 / 0; 
    }
}
```

总结
1. **ClassNotFoundException**：运行时**找不到类文件**，主动加载失败（缺包 / 路径错）
2. **NoClassDefFoundError**：类文件存在，但**加载 / 初始化失败**（静态块报错 / 文件损坏）
3. 一个是**找不到**，一个是**找到了但用不了**


## **第二，理解 Java 语言中操作 Throwable 的元素和实践**。

掌握最基本的语法是必须的，如 try-catch-finally 块，throw、throws 关键字等。与此同时，也要懂得如何处理典型场景。

异常处理代码比较繁琐，比如我们需要写很多千篇一律的捕获代码，或者在 finally 里面做一些资源回收工作。随着 Java 语言的发展，引入了一些更加便利的特性，比如 try-with-resources 和 multiple catch，具体可以参考下面的代码段。在编译时期，会自动生成相应的处理逻辑，比如，自动按照约定俗成 close 那些扩展了 AutoCloseable 或者 Closeable 的对象。
```java
try (BufferedReader br = new BufferedReader(…);
     BufferedWriter writer = new BufferedWriter(…)) {// Try-with-resources
// do something
catch ( IOException | XEception e) {// Multiple catch
   // Handle it
} 
```


# 知识扩展

前面谈的大多是概念性的东西，下面我来谈些实践中的选择，我会结合一些代码用例进行分析。

## 代码一

先开看第一个吧，下面的代码反映了异常处理中哪些不当之处？
```java
try {
  // 业务代码
  // …
  Thread.sleep(1000L);
} catch (Exception e) {
  // Ignore it
}
```

这段代码虽然很短，但是已经违反了异常处理的两个基本原则。

**第一，尽量不要捕获类似 Exception 这样的通用异常，而是应该捕获特定异常**，在这里是 Thread.sleep() 抛出的 InterruptedException。

这是因为在日常的开发和合作中，我们读代码的机会往往超过写代码，软件工程是门协作的艺术，所以我们有义务让自己的代码能够直观地体现出尽量多的信息，而泛泛的 Exception 之类，恰恰隐藏了我们的目的。另外，我们也要保证程序不会捕获到我们不希望捕获的异常。比如，你可能更希望 RuntimeException 被扩散出来，而不是被捕获。

进一步讲，除非深思熟虑了，否则不要捕获 Throwable 或者 Error，这样很难保证我们能够正确程序处理 OutOfMemoryError。

**第二，不要生吞（swallow）异常**。这是异常处理中要特别注意的事情，因为很可能会导致非常难以诊断的诡异情况。

生吞异常，往往是基于假设这段代码可能不会发生，或者感觉忽略异常是无所谓的，但是千万不要在产品代码做这种假设！

如果我们不把异常抛出来，或者也没有输出到日志（Logger）之类，程序可能在后续代码以不可控的方式结束。没人能够轻易判断究竟是哪里抛出了异常，以及是什么原因产生了异常。

## 代码二
再来看看第二段代码
```java
try {
   // 业务代码
   // …
} catch (IOException e) {
    e.printStackTrace();
}
```

这段代码作为一段实验代码，它是没有任何问题的，但是在产品代码中，通常都不允许这样处理。你先思考一下这是为什么呢？

我们先来看看[printStackTrace()](https://docs.oracle.com/javase/9/docs/api/java/lang/Throwable.html#printStackTrace--)的文档，开头就是“Prints this throwable and its backtrace to the standard error stream”。问题就在这里，在稍微复杂一点的生产系统中，标准出错（STERR）不是个合适的输出选项，因为你很难判断出到底输出到哪里去了。

尤其是对于分布式系统，如果发生异常，但是无法找到堆栈轨迹（stacktrace），这纯属是为诊断设置障碍。所以，最好使用产品日志，详细地输出到日志系统里。

## 代码三

我们接下来看下面的代码段，体会一下 **Throw early, catch late 原则**。
```java
public void readPreferences(String fileName){
   //...perform operations... 
  InputStream in = new FileInputStream(fileName);
   //...read the preferences file...
}
```

如果 fileName 是 null，那么程序就会抛出 NullPointerException，但是由于没有第一时间暴露出问题，堆栈信息可能非常令人费解，往往需要相对复杂的定位。这个 NPE 只是作为例子，实际产品代码中，可能是各种情况，比如获取配置失败之类的。在发现问题的时候，第一时间抛出，能够更加清晰地反映问题。

我们可以修改一下，让问题“throw early”，对应的异常信息就非常直观了。
```java

```
