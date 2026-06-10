# Redis 核心技术与实战 - 课程目录

## 00 开篇词

- [开篇词 | 这样学Redis，才能技高一筹](https://time.geekbang.org/column/article/268247)

## 01 基础篇

- [01 | 基本架构：一个键值数据库包含什么？](https://time.geekbang.org/column/article/268262)
- [02 | 数据结构：快速的Redis有哪些慢操作？](https://time.geekbang.org/column/article/268253)
- [03 | 高性能IO模型：为什么单线程Redis能那么快？](https://time.geekbang.org/column/article/270474)
- [04 | AOF日志：宕机了，Redis如何避免数据丢失？](https://time.geekbang.org/column/article/271754)
- [05 | 内存快照：宕机后，Redis如何实现快速恢复？](https://time.geekbang.org/column/article/271839)
- [06 | 数据同步：主从库如何实现数据一致？](https://time.geekbang.org/column/article/272852)
- [07 | 哨兵机制：主库挂了，如何不间断服务？](https://time.geekbang.org/column/article/274483)
- [08 | 哨兵集群：哨兵挂了，主从库还能切换吗？](https://time.geekbang.org/column/article/275337)
- [09 | 切片集群：数据增多了，是该加内存还是加实例？](https://time.geekbang.org/column/article/276545)
- [10 | 第1～9讲课后思考题答案及常见问题答疑](https://time.geekbang.org/column/article/277373)

## 02 实践篇

- [11 | "万金油"的String，为什么不好用了？](https://time.geekbang.org/column/article/279649)
- [12 | 有一亿个keys要统计，应该用哪种集合？](https://time.geekbang.org/column/article/280680)
- [13 | GEO是什么？还可以定义新的数据类型吗？](https://time.geekbang.org/column/article/281745)
- [14 | 如何在Redis中保存时间序列数据？](https://time.geekbang.org/column/article/282478)
- [15 | 消息队列的考验：Redis有哪些解决方案？](https://time.geekbang.org/column/article/284291)
- [16 | 异步机制：如何避免单线程模型的阻塞？](https://time.geekbang.org/column/article/285000)
- [17 | 为什么CPU结构也会影响Redis的性能？](https://time.geekbang.org/column/article/286082)
- [18 | 波动的响应延迟：如何应对变慢的Redis？（上）](https://time.geekbang.org/column/article/286549)
- [19 | 波动的响应延迟：如何应对变慢的Redis？（下）](https://time.geekbang.org/column/article/287819)
- [20 | 删除数据后，为什么内存占用率还是很高？](https://time.geekbang.org/column/article/289140)
- [21 | 缓冲区：一个可能引发"惨案"的地方](https://time.geekbang.org/column/article/291277)
- [22 | 第11～21讲课后思考题答案及常见问题答疑](https://time.geekbang.org/column/article/292285)
- [23 | 旁路缓存：Redis是如何工作的？](https://time.geekbang.org/column/article/293929)
- [24 | 替换策略：缓存满了怎么办？](https://time.geekbang.org/column/article/294640)
- [25 | 缓存异常（上）：如何解决缓存和数据库的数据不一致问题？](https://time.geekbang.org/column/article/295812)
- [26 | 缓存异常（下）：如何解决缓存雪崩、击穿、穿透难题？](https://time.geekbang.org/column/article/296586)
- [27 | 缓存被污染了，该怎么办？](https://time.geekbang.org/column/article/297270)
- [28 | Pika：如何基于SSD实现大容量Redis？](https://time.geekbang.org/column/article/298205)
- [29 | 无锁的原子操作：Redis如何应对并发访问？](https://time.geekbang.org/column/article/299806)
- [30 | 如何使用Redis实现分布式锁？](https://time.geekbang.org/column/article/301092)
- [31 | 事务机制：Redis能实现ACID属性吗？](https://time.geekbang.org/column/article/301491)
- [32 | Redis主从同步与故障切换，有哪些坑？](https://time.geekbang.org/column/article/303247)
- [33 | 脑裂：一次奇怪的数据丢失](https://time.geekbang.org/column/article/303568)
- [34 | 第23~33讲课后思考题答案及常见问题答疑](https://time.geekbang.org/column/article/304145)
- [35 | Codis VS Redis Cluster：我该选择哪一个集群方案？](https://time.geekbang.org/column/article/306548)
- [36 | Redis支撑秒杀场景的关键技术和实践都有哪些？](https://time.geekbang.org/column/article/307421)
- [37 | 数据分布优化：如何应对数据倾斜？](https://time.geekbang.org/column/article/308393)
- [38 | 通信开销：限制Redis Cluster规模的关键因素](https://time.geekbang.org/column/article/310347)

## 03 期中测试

- [期中测试题 | 一套习题，测出你的掌握程度](https://time.geekbang.org/column/article/292800)
- [期中测试题答案 | 这些问题，你都答对了吗？](https://time.geekbang.org/column/article/292803)

## 04 未来篇

- [39 | Redis 6.0的新特性：多线程、客户端缓存与安全](https://time.geekbang.org/column/article/310838)
- [40 | Redis的下一步：基于NVM内存的实践](https://time.geekbang.org/column/article/312568)
- [41 | 第35～40讲课后思考题答案及常见问题答疑](https://time.geekbang.org/column/article/313129)

## 05 加餐篇

- [加餐（一）| 经典的Redis学习资料有哪些？](https://time.geekbang.org/column/article/278677)
- [加餐（二）| 用户Kaito：我是如何学习Redis的？](https://time.geekbang.org/column/article/282987)
- [加餐（三）| 用户Kaito：我希望成为在压力中成长的人](https://time.geekbang.org/column/article/289950)
- [加餐（四）| Redis客户端如何与服务器端交换命令和数据？](https://time.geekbang.org/column/article/298504)
- [加餐（五）| Redis有哪些好用的运维工具？](https://time.geekbang.org/column/article/305195)
- [加餐（六）| Redis的使用规范小建议](https://time.geekbang.org/column/article/309089)
- [加餐（七）| 从微博的Redis实践中，我们可以学到哪些经验？](https://time.geekbang.org/column/article/313895)

## 06 结束语

- [期末测试 | 这些Redis核心知识，你都掌握了吗？](https://time.geekbang.org/column/article/314209)
- [结束语 | 从学习Redis到向Redis学习](https://time.geekbang.org/column/article/316679)
