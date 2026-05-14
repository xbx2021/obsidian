![](assets/第15讲%20synchronized和ReentrantLock有什么区别呢？/file-20260514092933499.png)
从今天开始，我们将进入 Java 并发学习阶段。软件并发已经成为现代软件开发的基础能力，而 Java 精心设计的高效并发机制，正是构建大规模应用的基础之一，所以考察并发基本功也成为各个公司面试 Java 工程师的必选项。

今天我要问你的问题是， **synchronized 和 ReentrantLock 有什么区别？有人说 synchronized 最慢，这话靠谱吗？**

# 典型回答

**synchronized** 是 Java 内建的同步机制，所以也有人称其为 Intrinsic Locking，它提供了互斥的语义和可见性，当一个线程已经获取当前锁时，其他试图获取的线程只能等待或者阻塞在那里。

在 Java 5 以前，synchronized 是仅有的同步手段，在代码中， synchronized 可以用来修饰方法，也可以使用在特定的代码块儿上，本质上 synchronized 方法等同于把方法全部语句用 synchronized 块包起来。

**ReentrantLock**，通常翻译为再入锁，是 Java 5 提供的锁实现，它的语义和 synchronized 基本相同。再入锁通过代码直接调用 lock() 方法获取，代码书写也更加灵活。与此同时，ReentrantLock 提供了很多实用的方法，能够实现很多 synchronized 无法做到的细节控制，比如可以控制 fairness，也就是公平性，或者利用定义条件等。但是，编码中也需要注意，必须要明确调用 unlock() 方法释放，不然就会一直持有该锁。

synchronized 和 ReentrantLock 的性能不能一概而论，早期版本 synchronized 在很多场景下性能相差较大，在后续版本进行了较多改进，在低竞争场景中表现可能优于 ReentrantLock。

# 考点分析

今天的题目是考察并发编程的常见基础题，我给出的典型回答算是一个相对全面的总结。

对于并发编程，不同公司或者面试官面试风格也不一样，有个别大厂喜欢一直追问你相关机制的扩展或者底层，有的喜欢从实用角度出发，所以你在准备并发编程方面需要一定的耐心。

我认为，锁作为并发的基础工具之一，你至少需要掌握：

- **理解什么是线程安全。**
- **synchronized、ReentrantLock 等机制的基本使用与案例。**

更进一步，你还需要：

- **掌握 synchronized、ReentrantLock 底层实现；理解锁膨胀、降级；理解偏斜锁、自旋锁、轻量级锁、重量级锁等概念。**
- **掌握并发包中 java.util.concurrent.lock 各种不同实现和案例分析。**

# 知识扩展

专栏前面几期穿插了一些并发的概念，有同学反馈理解起来有点困难，尤其对一些并发相关概念比较陌生，所以在这一讲，我也对会一些基础的概念进行补充。

## 线程安全

首先，我们需要理解什么是线程安全。

我建议阅读 Brain Goetz 等专家撰写的《Java 并发编程实战》（Java Concurrency in Practice），虽然可能稍显学究，但不可否认这是一本非常系统和全面的 Java 并发编程书籍。按照其中的定义，**线程安全是一个多线程环境下正确性的概念，也就是保证多线程环境下共享的、可修改的状态的正确性，这里的状态反映在程序中其实可以看作是数据**。

换个角度来看，如果状态不是共享的，或者不是可修改的，也就不存在线程安全问题，进而可以推理出保证线程安全的两个办法：

- **封装**：通过封装，我们可以将对象内部状态隐藏、保护起来。
- **不可变**：还记得我们在专栏第 3 讲强调的 final 和 immutable 吗，就是这个道理，Java 语言目前还没有真正意义上的原生不可变，但是未来也许会引入。

线程安全需要保证几个基本特性：

- **原子性**，简单说就是相关操作不会中途被其他线程干扰，一般通过同步机制实现。
- **可见性**，是一个线程修改了某个共享变量，其状态能够立即被其他线程知晓，通常被解释为将线程本地状态反映到主内存上，**volatile** 就是负责保证可见性的。
- **有序性**，是保证线程内串行语义，避免指令重排等。

可能有点晦涩，那么我们看看下面的代码段，分析一下原子性需求体现在哪里。这个例子通过取两次数值然后进行对比，来模拟两次对共享状态的操作。

你可以编译并执行，可以看到，仅仅是两个线程的低度并发，就非常容易碰到 former 和 latter 不相等的情况。这是因为，在两次取值的过程中，其他线程可能已经修改了 sharedState。
```java
public class ThreadSafeSample {
  public int sharedState;
  public void nonSafeAction() {
      while (sharedState < 100000) {
          int former = sharedState++;
          int latter = sharedState;
          if (former != latter - 1) {
              System.out.printf("Observed data race, former is " +
                      former + ", " + "latter is " + latter);
          }
      }
  }

  public static void main(String[] args) throws InterruptedException {
      ThreadSafeSample sample = new ThreadSafeSample();
      Thread threadA = new Thread(){
          public void run(){
              sample.nonSafeAction();
          }
      };
      Thread threadB = new Thread(){
          public void run(){
              sample.nonSafeAction();
          }
      };
      threadA.start();
      threadB.start();
      threadA.join();
      threadB.join();
  }
}
```

