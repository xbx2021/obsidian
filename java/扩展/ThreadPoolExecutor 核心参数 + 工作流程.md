# ThreadPoolExecutor 核心参数 + 工作流程

`ThreadPoolExecutor` 是 Java 线程池的**核心实现类**，吃透它的参数和工作流程，就能完全掌握线程池原理。

---

## 一、7 个核心参数（必背）
这是构造方法的完整参数，每个都有明确作用：
```java
public ThreadPoolExecutor(
    int corePoolSize,          // 1. 核心线程数
    int maximumPoolSize,       // 2. 最大线程数
    long keepAliveTime,        // 3. 空闲线程存活时间
    TimeUnit unit,            // 4. 时间单位
    BlockingQueue<Runnable> workQueue, // 5. 任务队列
    ThreadFactory threadFactory,      // 6. 线程工厂
    RejectedExecutionHandler handler  // 7. 拒绝策略
)
```

### 逐参数详解
1. **corePoolSize（核心线程数）**
   - 线程池中长期存活的**核心线程**，即使空闲也不会被回收（默认）。
   - 类比：公司正式员工，一直在岗。

2. **maximumPoolSize（最大线程数）**
   - 线程池能容纳的**最大总线程数** = 核心线程 + 非核心线程。
   - 类比：正式员工 + 临时员工的总人数上限。

3. **keepAliveTime（空闲线程存活时间）**
   - 非核心线程空闲超过这个时间，会被**自动销毁**。
   - 核心线程默认不回收，可通过 `allowCoreThreadTimeOut(true)` 开启回收。

4. **unit（时间单位）**
   - 配合存活时间使用：`TimeUnit.SECONDS`/`MINUTES` 等。

5. **workQueue（任务阻塞队列）**
   - 当核心线程都在忙时，新任务会放入这个队列**等待执行**。
   - 常用队列：
     - `ArrayBlockingQueue`：有界队列（固定容量，推荐生产使用）
     - `LinkedBlockingQueue`：无界队列（容量无限，容易OOM）
     - `SynchronousQueue`：不存储元素，直接提交任务

6. **threadFactory（线程工厂）**
   - 用于创建新线程，可自定义线程名、优先级、守护线程等。
   - 默认：`Executors.defaultThreadFactory()`。

7. **handler（拒绝策略）**
   - 当**线程数达到最大 + 队列满了**，继续提交任务时的处理方式。
   - JDK 内置 4 种策略：
     1. `AbortPolicy`（默认）：直接抛异常，阻止程序运行
     2. `CallerRunsPolicy`：让提交任务的线程自己执行
     3. `DiscardPolicy`：直接丢弃新任务，不抛异常
     4. `DiscardOldestPolicy`：丢弃队列最老的任务，执行新任务

---

## 二、线程池工作流程（核心逻辑）
这是线程池处理任务的**固定步骤**，面试必考：

### 执行流程（一句话总结）
**先开核心线程 → 再进队列 → 最后开非核心线程 → 满了就拒绝**

### 分步图解
1. **提交任务**
   调用 `execute()` / `submit()` 提交任务。

2. **判断核心线程数**
   - 如果**运行线程数 < corePoolSize**：直接创建**核心线程**执行任务。

3. **判断任务队列**
   - 核心线程满了 → 将任务加入 **workQueue 队列** 等待。

4. **判断最大线程数**
   - 队列也满了 → 创建**非核心线程**执行任务。
   - 要求：总线程数 < maximumPoolSize。

5. **执行拒绝策略**
   - 总线程数达到 maximumPoolSize + 队列满了 → 执行 **拒绝策略**。

6. **空闲回收**
   - 任务执行完，非核心线程空闲超过 `keepAliveTime` → 自动销毁。
   - 最终线程池会收缩回 corePoolSize 大小。

---

## 三、极简流程图（秒懂）
```
提交新任务
    ↓
运行线程数 < 核心线程数？ → 是：创建核心线程执行
    ↓否
任务队列未满？ → 是：加入队列等待
    ↓否
运行线程数 < 最大线程数？ → 是：创建非核心线程执行
    ↓否
执行拒绝策略
```

---

## 四、示例代码（带注释）
```java
import java.util.concurrent.*;

public class ThreadPoolDemo {
    public static void main(String[] args) {
        // 自定义线程池
        ThreadPoolExecutor pool = new ThreadPoolExecutor(
                2,                // 核心线程：2
                5,                // 最大线程：5
                3,                // 空闲存活时间：3秒
                TimeUnit.SECONDS,
                new ArrayBlockingQueue<>(3), // 任务队列：容量3
                Executors.defaultThreadFactory(),
                new ThreadPoolExecutor.AbortPolicy() // 默认拒绝策略
        );

        // 提交10个任务测试流程
        for (int i = 1; i <= 10; i++) {
            int task = i;
            pool.execute(() -> {
                System.out.println(Thread.currentThread().getName() + " 执行任务" + task);
                try { Thread.sleep(1000); } catch (InterruptedException e) {}
            });
        }
        pool.shutdown();
    }
}
```

---

### 总结
1. **核心参数**：核心线程、最大线程、存活时间、队列、线程工厂、拒绝策略。
2. **工作流程**：核心线程 → 任务队列 → 非核心线程 → 拒绝策略。
3. **核心原则**：**队列优先，非核心线程兜底**，避免频繁创建线程。