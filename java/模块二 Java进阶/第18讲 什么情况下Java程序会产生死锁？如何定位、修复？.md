![](assets/第18讲%20什么情况下Java程序会产生死锁？如何定位、修复？/file-20260514143243360.png)
今天，我会介绍一些日常开发中类似线程死锁等问题的排查经验，并选择一两个我自己修复过或者诊断过的核心类库死锁问题作为例子，希望不仅能在面试时，包括在日常工作中也能对你有所帮助。

今天我要问你的问题是，**什么情况下 Java 程序会产生死锁？如何定位、修复？**

# 典型回答

死锁是一种特定的程序状态，在实体之间，由于循环依赖导致彼此一直处于等待之中，没有任何个体可以继续前进。死锁不仅仅是在线程之间会发生，存在资源独占的进程之间同样也可能出现死锁。通常来说，我们大多是聚焦在多线程场景中的死锁，指两个或多个线程之间，由于互相持有对方需要的锁，而永久处于阻塞的状态。

你可以利用下面的示例图理解基本的死锁问题：
![](assets/第18讲%20什么情况下Java程序会产生死锁？如何定位、修复？/file-20260514144355553.png)

定位死锁最常见的方式就是利用 jstack 等工具获取线程栈，然后定位互相之间的依赖关系，进而找到死锁。如果是比较明显的死锁，往往 jstack 等就能直接定位，类似 JConsole 甚至可以在图形界面进行有限的死锁检测。

如果程序运行时发生了死锁，绝大多数情况下都是无法在线解决的，只能重启、修正程序本身问题。所以，代码开发阶段互相审查，或者利用工具进行预防性排查，往往也是很重要的。

# 考点分析

今天的问题偏向于实用场景，大部分死锁本身并不难定位，掌握基本思路和工具使用，理解线程相关的基本概念，比如各种线程状态和同步、锁、Latch 等并发工具，就已经足够解决大多数问题了。

针对死锁，面试官可以深入考察：

- 抛开字面上的概念，让面试者写一个可能死锁的程序，顺便也考察下基本的线程编程。
- 诊断死锁有哪些工具，如果是分布式环境，可能更关心能否用 API 实现吗？
- 后期诊断死锁还是挺痛苦的，经常加班，如何在编程中尽量避免一些典型场景的死锁，有其他工具辅助吗？

# 知识扩展

在分析开始之前，先以一个基本的死锁程序为例，我在这里只用了两个嵌套的 synchronized 去获取锁，具体如下：
```java
public class DeadLockSample extends Thread {
  private String first;
  private String second;
  public DeadLockSample(String name, String first, String second) {
      super(name);
      this.first = first;
      this.second = second;
  }

  public  void run() {
      synchronized (first) {
          System.out.println(this.getName() + " obtained: " + first);
          try {
              Thread.sleep(1000L);
              synchronized (second) {
                  System.out.println(this.getName() + " obtained: " + second);
              }
          } catch (InterruptedException e) {
              // Do nothing
          }
      }
  }
  public static void main(String[] args) throws InterruptedException {
      String lockA = "lockA";
      String lockB = "lockB";
      DeadLockSample t1 = new DeadLockSample("Thread1", lockA, lockB);
      DeadLockSample t2 = new DeadLockSample("Thread2", lockB, lockA);
      t1.start();
      t2.start();
      t1.join();
      t2.join();
  }
}
```

这个程序编译执行后，几乎每次都可以重现死锁，请看下面截取的输出。另外，这里有个比较有意思的地方，为什么我先调用 Thread1 的 start，但是 Thread2 却先打印出来了呢？这就是因为线程调度依赖于（操作系统）调度器，虽然你可以通过优先级之类进行影响，但是具体情况是不确定的。
![](assets/第18讲%20什么情况下Java程序会产生死锁？如何定位、修复？/file-20260514145042496.png)

下面来模拟问题定位，我就选取最常见的 jstack，其他一些类似 JConsole 等图形化的工具，请自行查找。

首先，可以使用 jps 或者系统的 ps 命令、任务管理器等工具，确定进程 ID。

其次，调用 jstack 获取线程栈：
```
${JAVA_HOME}\bin\jstack your_pid
```

然后，分析得到的输出，具体片段如下：
![](assets/第18讲%20什么情况下Java程序会产生死锁？如何定位、修复？/file-20260514145146516.png)

最后，结合代码分析线程栈信息。上面这个输出非常明显，找到处于 BLOCKED 状态的线程，按照试图获取（waiting）的锁 ID（请看我标记为相同颜色的数字）查找，很快就定位问题。 jstack 本身也会把类似的简单死锁抽取出来，直接打印出来。

在实际应用中，类死锁情况未必有如此清晰的输出，但是总体上可以理解为：

**区分线程状态 -> 查看等待目标 -> 对比 Monitor 等持有状态**

所以，理解线程基本状态和并发相关元素是定位问题的关键，然后配合程序调用栈结构，基本就可以定位到具体的问题代码。

如果我们是开发自己的管理工具，需要用更加程序化的方式扫描服务进程、定位死锁，可以考虑使用 Java 提供的标准管理 API，[ThreadMXBean](https://docs.oracle.com/javase/9/docs/api/java/lang/management/ThreadMXBean.html#findDeadlockedThreads--)，其直接就提供了 findDeadlockedThreads​() 方法用于定位。为方便说明，我修改了 DeadLockSample，请看下面的代码片段。
```java
public static void main(String[] args) throws InterruptedException {

  ThreadMXBean mbean = ManagementFactory.getThreadMXBean();
  Runnable dlCheck = new Runnable() {

      @Override
      public void run() {
          long[] threadIds = mbean.findDeadlockedThreads();
          if (threadIds != null) {
                     ThreadInfo[] threadInfos = mbean.getThreadInfo(threadIds);
                     System.out.println("Detected deadlock threads:");
              for (ThreadInfo threadInfo : threadInfos) {
                  System.out.println(threadInfo.getThreadName());
              }
          }
       }
    };

       ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
       // 稍等5秒，然后每10秒进行一次死锁扫描
        scheduler.scheduleAtFixedRate(dlCheck, 5L, 10L, TimeUnit.SECONDS);
// 死锁样例代码…
}
```

重新编译执行，你就能看到死锁被定位到的输出。在实际应用中，就可以据此收集进一步的信息，然后进行预警等后续处理。但是要注意的是，对线程进行快照本身是一个相对重量级的操作，还是要慎重选择频度和时机。

## 如何在编程中尽量预防死锁呢？

