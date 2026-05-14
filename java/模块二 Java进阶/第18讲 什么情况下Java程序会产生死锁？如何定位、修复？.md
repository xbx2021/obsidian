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