![](assets/第36讲%20谈谈MySQL支持的事务隔离级别，以及悲观锁和乐观锁的原理和应用场景？/file-20260518170652004.png)

在日常开发中，尤其是业务开发，少不了利用 Java 对数据库进行基本的增删改查等数据操作，这也是 Java 工程师的必备技能之一。做好数据操作，不仅仅需要对 Java 语言相关框架的掌握，更需要对各种数据库自身体系结构的理解。今天这一讲，作为补充 Java 面试考察知识点的完整性，关于数据库的应用和细节还需要在实践中深入学习。

今天我要问你的问题是，**谈谈 MySQL 支持的事务隔离级别，以及悲观锁和乐观锁的原理和应用场景？**

# 典型回答

所谓隔离级别（[Isolation Level](https://en.wikipedia.org/wiki/Isolation_(database_systems)#Isolation_levels)），就是在数据库事务中，为保证并发数据读写的正确性而提出的定义，它并不是 MySQL 专有的概念，而是源于[ANSI](https://en.wikipedia.org/wiki/American_National_Standards_Institute)/[ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)制定的[SQL-92](https://en.wikipedia.org/wiki/SQL-92)标准。

每种关系型数据库都提供了各自特色的隔离级别实现，虽然在通常的[定义](https://en.wikipedia.org/wiki/Isolation_(database_systems)#Isolation_levels)中是以锁为实现单元，但实际的实现千差万别。以最常见的 MySQL InnoDB 引擎为例，它是基于 [MVCC](https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html)（Multi-Versioning Concurrency Control）和锁的复合实现，按照隔离程度从低到高，MySQL 事务隔离级别分为四个不同层次：

- **读未提交**（Read uncommitted），就是一个事务能够看到其他事务尚未提交的修改，这是最低的隔离水平，**允许[脏读](https://en.wikipedia.org/wiki/Isolation_(database_systems)#Dirty_reads)出现**。

- **读已提交**（Read committed），事务能够看到的数据都是其他事务已经提交的修改，也就是保证不会看到任何中间性状态，当然脏读也不会出现。读已提交仍然是比较低级别的隔离，并不保证再次读取时能够获取同样的数据，也就是允许其他事务并发修改数据，**允许不可重复读和幻象读（Phantom Read）出现**。

- **可重复读**（Repeatable reads），保证同一个事务中多次读取的数据是一致的，这是 **MySQL InnoDB 引擎的默认隔离级别**，但是和一些其他数据库实现不同的是，可以简单认为 MySQL 在可重复读级别不会出现幻象读。

- **串行化**（Serializable），并发事务之间是串行化的，通常意味着读取需要获取共享读锁，更新需要获取排他写锁，如果 SQL 使用 WHERE 语句，还会获取区间锁（MySQL 以 GAP 锁形式实现，可重复读级别中默认也会使用），这是最高的隔离级别。

至于**悲观锁和乐观锁**，也并不是 MySQL 或者数据库中独有的概念，而是并发编程的基本概念。主要区别在于，操作共享数据时，“悲观锁”即认为数据出现冲突的可能性更大，而“乐观锁”则是认为大部分情况不会出现冲突，进而决定是否采取排他性措施。

