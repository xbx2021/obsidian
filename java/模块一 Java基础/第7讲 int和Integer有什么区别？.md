![](assets/第7讲%20int和Integer有什么区别？/file-20260512104641339.png)

Java 虽然号称是面向对象的语言，但是原始数据类型仍然是重要的组成元素，所以在面试中，经常考察原始数据类型和包装类等 Java 语言特性。

今天我要问你的问题是，**int 和 Integer 有什么区别？谈谈 Integer 的值缓存范围**。

# 典型回答

int 是我们常说的整形数字，是 Java 的 8 个原始数据类型（Primitive Types，boolean、byte 、short、char、int、float、double、long）之一。**Java 语言虽然号称一切都是对象，但原始数据类型是例外。**

**Integer 是 int 对应的包装类**，它有一个 int 类型的字段存储数据，并且提供了基本操作，比如数学运算、int 和字符串之间转换等。在 Java 5 中，引入了自动装箱和自动拆箱功能（boxing/unboxing），Java 可以根据上下文，自动进行转换，极大地简化了相关编程。

