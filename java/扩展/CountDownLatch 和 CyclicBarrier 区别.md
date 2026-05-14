## 一、核心定义
### CountDownLatch
- **减法计数器**：初始化固定次数 `count`
- 线程调用 `countDown()` 计数-1
- 主线程 `await()` 等待**计数减到0**再往下走
- **只能用一次，不能重置**

### CyclicBarrier
- **同步栅栏**：初始化参与线程数 `N`
- 每个线程到屏障点调用 `await()`
- **凑齐 N 个线程**，统一放行
- **自动循环复用**，一轮结束直接下一轮

---

## 二、关键区别对比表
| 维度 | CountDownLatch | CyclicBarrier |
|------|----------------|---------------|
| 复用性 | **一次性**，用完作废，不能重置 | **可循环复用**，自动重置栅栏 |
| 等待关系 | **主线程等子线程**<br>等任务做完 | **线程之间互相等**<br>大家都到齐再一起走 |
| 计数方式 | 递减 `countDown()` | 到达栅栏阻塞，凑齐放行 |
| 触发动作 | 无内置回调 | 支持**栅栏凑齐后执行回调任务** |
| 适用场景 | 任务拆分、主等从、启动/等待完成 | 多线程分阶段同步、一轮一轮执行 |
| 异常破坏 | 不会破坏整体 | 某个线程中断/异常，栅栏损坏 |

---

## 三、场景举例（秒懂）
### 1. CountDownLatch 场景
**马拉松发令枪**
- 运动员全部准备好（子线程任务完成）
- 裁判（主线程）等所有人就位，**发令开跑**
- 只发一次令，跑完就结束，不能再来一轮

### 2. CyclicBarrier 场景
**旅游大巴集合**
- 一车5个人，必须**5人全部到齐**才发车
- 到景点解散，再集合又等5人到齐再走
- **可以反复集合、反复发车**（循环复用）

---

## 四、代码行为差异（结合你刚才的代码）
你代码里：
- 5个线程，每轮都要等所有人打印完再下一轮
- 循环3轮，自动卡点同步 → **必须用 CyclicBarrier**

如果换成 CountDownLatch：
- 只能等一轮，计数到0就废了
- 没法实现**三轮重复同步**

---

## 五、CountDownLatch 示例（一次性、主等子、不可复用）
特点：**主线程等所有子线程干完活**，计数器归零就报废，不能第二轮再用。

```java
import java.util.concurrent.CountDownLatch;

public class CountDownLatchDemo {
    public static void main(String[] args) throws InterruptedException {
        // 计数器 = 5
        CountDownLatch latch = new CountDownLatch(5);

        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                System.out.println(Thread.currentThread().getName() + " 执行任务");
                // 计数减1
                latch.countDown();
            }).start();
        }

        // 主线程阻塞，等5个线程全部 countDown 完
        latch.await();
        System.out.println("所有子线程执行完毕，主线程继续往下走");

        // 重点：不能复用！再 await 直接放行，没有第二轮等待
    }
}
```

### 核心特点
1. 子线程干完活主动 `countDown()`
2. 主线程 `await()` 等待全部完成
3. **只能用一次**，不能循环多轮同步

---

## 六、CyclicBarrier 示例（可循环、互相等、凑齐放行）
特点：**线程之间互相等待**，凑齐数量统一放行，自动重置，可以多轮循环。

```java
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierDemo {
    public static void main(String[] args) {
        // 5个线程到达屏障才放行，放行后执行回调
        CyclicBarrier barrier = new CyclicBarrier(5, () ->
                System.out.println("===== 所有人到齐，统一放行 =====")
        );

        // 开启5个线程
        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                // 模拟3轮循环，每轮都要等所有人到齐
                for (int round = 1; round <= 3; round++) {
                    System.out.println(Thread.currentThread().getName() + " 第" + round + "轮就绪");
                    try {
                        // 阻塞，等凑齐5个线程
                        barrier.await();
                    } catch (InterruptedException | BrokenBarrierException e) {
                        e.printStackTrace();
                    }
                }
            }).start();
        }
    }
}
```

### 核心特点
1. 每个线程到卡点都调用 `await()` **互相等待**
2. 凑齐设定数量，统一放行 + 执行回调
3. **自动循环复用**，可以无限多轮同步

---

## 七、一句话终极区别（背下来就能面试）
1. **CountDownLatch**：
**一个线程等一群线程，一次性，不可逆，不能复用。**
适合：**等待所有任务初始化完成 / 所有任务执行结束**。

2. **CyclicBarrier**：
**一群线程互相等，凑齐再一起走，可循环复用。**
适合：**多线程分阶段执行、每一轮都要全员同步**。

---
