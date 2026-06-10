# 后端工程师的高阶面经 - 课程目录

## 00 开篇词

- [开篇词｜面试如戏，台上一分钟，台下十年功](https://time.geekbang.org/column/article/668548)

## 01 微服务架构

- [01｜服务注册与发现：AP和CP，你选哪个？](https://time.geekbang.org/column/article/668434)
- [02｜负载均衡：调用结果、缓存机制是怎么影响负载均衡的？](https://time.geekbang.org/column/article/668453)
- [03｜熔断：熔断-恢复-熔断-恢复，抖来抖去怎么办？](https://time.geekbang.org/column/article/669233)
- [04｜降级：为什么每次大促的时候总是要把退款之类的服务停掉？](https://time.geekbang.org/column/article/669254)
- [05｜限流：别说算法了，就问你"阈值"怎么算？](https://time.geekbang.org/column/article/670039)
- [06｜隔离：怎么保证尊贵的VIP用户体验不受损？](https://time.geekbang.org/column/article/670854)
- [07｜超时控制：怎么保证用户一定能在1s内拿到响应？](https://time.geekbang.org/column/article/670877)
- [08｜调用第三方：下游的接口不稳定性能又差怎么办？](https://time.geekbang.org/column/article/672238)
- [09｜综合服务治理方案：怎么保证微服务应用的高可用？](https://time.geekbang.org/column/article/672251)
- [模拟面试（一）｜微服务架构面试思路一图懂](https://time.geekbang.org/column/article/672561)

## 02 数据库与MySQL

- [10｜数据库索引：为什么MySQL用B+树而不用B树？](https://time.geekbang.org/column/article/672553)
- [11｜SQL优化：如何发现SQL中的问题？](https://time.geekbang.org/column/article/674168)
- [12｜数据库锁：明明有行锁，怎么突然就加了表锁？](https://time.geekbang.org/column/article/674789)
- [13｜MVCC协议：MySQL 在修改数据的时候，还能不能读到这条数据？](https://time.geekbang.org/column/article/675235)
- [14｜数据库事务：事务提交了，你的数据就一定不会丢吗？](https://time.geekbang.org/column/article/675812)
- [15｜数据迁移：如何在不停机的情况下保证迁移数据的一致性？](https://time.geekbang.org/column/article/676586)
- [16｜分库分表主键生成：如何设计一个主键生成算法？](https://time.geekbang.org/column/article/676793)
- [17｜分库分表分页查询：为什么你的分页查询又慢又耗费内存？](https://time.geekbang.org/column/article/677491)
- [18｜分布式事务：如何同时保证分库分表、ACID和高性能？](https://time.geekbang.org/column/article/678287)
- [19｜分库分表无分库分表键查询：你按照买家分库分表，那我卖家怎么查？](https://time.geekbang.org/column/article/678315)
- [20｜分库分表容量预估：分库分表的时候怎么计算需要多少个库多少个表？](https://time.geekbang.org/column/article/682824)
- [21｜数据库综合应用：怎么保证数据库的高可用、高性能？](https://time.geekbang.org/column/article/683232)
- [模拟面试｜数据库面试思路一图懂](https://time.geekbang.org/column/article/683948)

## 03 消息队列

- [22｜消息队列：消息队列可以用来解决什么问题？](https://time.geekbang.org/column/article/684182)
- [23｜延迟消息：怎么在 Kafka 上支持延迟消息？](https://time.geekbang.org/column/article/685187)
- [24｜消息顺序：保证消息有序，一个 topic 只能有一个 partition 吗？](https://time.geekbang.org/column/article/685914)
- [25｜消息积压：业务突然增长，导致消息消费不过来怎么办？](https://time.geekbang.org/column/article/685943)
- [26｜消息不丢失：生产者收到写入成功响应后消息一定不会丢失吗？](https://time.geekbang.org/column/article/687062)
- [27｜重复消费：高并发场景下怎么保证消息不会重复消费？](https://time.geekbang.org/column/article/687082)
- [28｜架构设计：如果让你设计一个消息队列，你会怎么设计它的架构？](https://time.geekbang.org/column/article/688562)
- [29｜高性能：Kafka 为什么性能那么好？](https://time.geekbang.org/column/article/689362)
- [30｜Kafka 综合运用：怎么在实践中保证 Kafka 高性能？](https://time.geekbang.org/column/article/689379)
- [模拟面试｜消息队列面试思路一图懂](https://time.geekbang.org/column/article/689793)

## 04 缓存

- [31｜缓存过期：为什么 Redis 不立刻删除已经过期的数据？](https://time.geekbang.org/column/article/689782)
- [32｜缓存淘汰策略：怎么淘汰缓存命中率才不会下降？](https://time.geekbang.org/column/article/692691)
- [33｜缓存模式：缓存模式能不能解决缓存一致性问题？](https://time.geekbang.org/column/article/692719)
- [34｜缓存一致性问题：高并发服务如何保证缓存一致性？](https://time.geekbang.org/column/article/696599)
- [35｜缓存问题：怎么解决缓存穿透、击穿和雪崩问题？](https://time.geekbang.org/column/article/698514)
- [36｜Redis 单线程：为什么 Redis 用单线程而 Memcached 用多线程？](https://time.geekbang.org/column/article/699268)
- [37｜分布式锁：如何保证Redis分布式锁的高可用和高性能？](https://time.geekbang.org/column/article/700522)
- [38｜缓存综合应用：怎么用缓存来提高整个应用的性能？](https://time.geekbang.org/column/article/701317)
- [模拟面试｜缓存面试思路一图懂](https://time.geekbang.org/column/article/700599)

## 05 NoSQL

- [39｜Elasticsearch高可用：怎么保证Elasticsearch的高可用？](https://time.geekbang.org/column/article/701813)
- [40｜Elasticsearch查询：怎么优化 Elasticsearch 的查询性能？](https://time.geekbang.org/column/article/703179)
- [41｜MongoDB：MongoDB 是怎么做到高可用的？](https://time.geekbang.org/column/article/703160)
- [42｜MongoDB高性能：怎么优化MongoDB的查询性能？](https://time.geekbang.org/column/article/703200)
- [模拟面试｜NoSQL面试思路一图懂](https://time.geekbang.org/column/article/708001)

## 06 课程迭代

- [再出发｜大厂技术终面"必答题"](https://time.geekbang.org/column/article/854675)
- [MySQL问题排查：线上突发故障，怎么办？](https://time.geekbang.org/column/article/854687)
- [Redis响应时间太慢了，怎么办？](https://time.geekbang.org/column/article/860223)
- [如何解决Redis的热点问题？](https://time.geekbang.org/column/article/865962)
- [如何用系统化思维排查Kafka问题？](https://time.geekbang.org/column/article/865985)
- [ElasticSearch查询太慢怎么办？](https://time.geekbang.org/column/article/865988)

## 07 直播加餐

- [直播加餐｜后端工程师如何在面试中脱颖而出？](https://time.geekbang.org/column/article/766155)
- [直播加餐｜3个例子教你设计面试连招](https://time.geekbang.org/column/article/790222)
- [直播加餐｜如何设计面试连招？](https://time.geekbang.org/column/article/797622)

## 08 结束语

- [结束语｜未来掌握在自己手中](https://time.geekbang.org/column/article/708286)
- [结课测试｜来赴一场满分之约！](https://time.geekbang.org/column/article/708341)
