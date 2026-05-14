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

这个题目主要考察你对并发包了解程度，以及是否有实际使用经验。我们进行多线程编程，无非是达到几个目的：

- 利用多线程提高程序的扩展能力，以达到业务对吞吐量的要求。
- 协调线程间调度、交互，以完成业务逻辑。
- 线程间传递数据和状态，这同样是实现业务逻辑的需要。

所以，这道题目只能算作简单的开始，往往面试官还会进一步考察如何利用并发包实现某个特定的用例，分析实现的优缺点等。

如果你在这方面的基础比较薄弱，我的建议是：

- 从总体上，把握住几个主要组成部分（前面回答中已经简要介绍）。
- 理解具体设计、实现和能力。
- 再深入掌握一些比较典型工具类的适用场景、用法甚至是原理，并熟练写出典型的代码用例。

掌握这些通常就够用了，毕竟并发包提供了方方面面的工具，其实很少有机会能在应用中全面使用过，扎实地掌握核心功能就非常不错了。真正特别深入的经验，还是得靠在实际场景中踩坑来获得。

# 知识扩展

首先，我们来看看并发包提供的丰富同步结构。前面几讲已经分析过各种不同的显式锁，今天我将专注于

- [CountDownLatch](https://docs.oracle.com/javase/9/docs/api/java/util/concurrent/CountDownLatch.html)，允许一个或多个线程等待某些操作完成。
- [CyclicBarrier](https://docs.oracle.com/javase/9/docs/api/java/util/concurrent/CyclicBarrier.html)，一种辅助性的同步结构，允许多个线程等待到达某个屏障。
- [Semaphore](https://docs.oracle.com/javase/9/docs/api/java/util/concurrent/Semaphore.html)，Java 版本的信号量实现。

Java 提供了经典信号量（[Semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming))）的实现，它通过控制一定数量的允许（permit）的方式，来达到限制通用资源访问的目的。你可以想象一下这个场景，在车站、机场等出租车时，当很多空出租车就位时，为防止过度拥挤，调度员指挥排队等待坐车的队伍一次进来 5 个人上车，等这 5 个人坐车出发，再放进去下一批，这和 Semaphore 的工作原理有些类似。

你可以试试使用 Semaphore 来模拟实现这个调度过程：
```java
import java.util.concurrent.Semaphore;
public class UsualSemaphoreSample {
  public static void main(String[] args) throws InterruptedException {
      System.out.println("Action...GO!");
      Semaphore semaphore = new Semaphore(5);
      for (int i = 0; i < 10; i++) {
          Thread t = new Thread(new SemaphoreWorker(semaphore));
          t.start();
      }
  }
}
class SemaphoreWorker implements Runnable {
  private String name;
  private Semaphore semaphore;
  public SemaphoreWorker(Semaphore semaphore) {
      this.semaphore = semaphore;
  }
  @Override
  public void run() {
      try {
          log("is waiting for a permit!");
         semaphore.acquire();
          log("acquired a permit!");
          log("executed!");
      } catch (InterruptedException e) {
          e.printStackTrace();
      } finally {
          log("released a permit!");
          semaphore.release();
      }
  }
  private void log(String msg){
      if (name == null) {
          name = Thread.currentThread().getName();
      }
      System.out.println(name + " " + msg);
  }
}
```