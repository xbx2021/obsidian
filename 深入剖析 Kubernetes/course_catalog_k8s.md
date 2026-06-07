# 深入剖析 Kubernetes - 课程目录


## 课前必读

- [开篇词 | 打通"容器技术"的任督二脉](https://time.geekbang.org/column/article/14252)
- [01 | 预习篇 · 小鲸鱼大事记（一）：初出茅庐](https://time.geekbang.org/column/article/14254)
- [02 | 预习篇 · 小鲸鱼大事记（二）：崭露头角](https://time.geekbang.org/column/article/14256)
- [03 | 预习篇 · 小鲸鱼大事记（三）：群雄并起](https://time.geekbang.org/column/article/14405)
- [04 | 预习篇 · 小鲸鱼大事记（四）：尘埃落定](https://time.geekbang.org/column/article/14406)

## 容器技术概念入门篇

- [05 | 白话容器基础（一）：从进程说开去](https://time.geekbang.org/column/article/14642)
- [06 | 白话容器基础（二）：隔离与限制](https://time.geekbang.org/column/article/14653)
- [07 | 白话容器基础（三）：深入理解容器镜像](https://time.geekbang.org/column/article/17921)
- [08 | 白话容器基础（四）：重新认识Docker容器](https://time.geekbang.org/column/article/18119)
- [09 | 从容器到容器云：谈谈Kubernetes的本质](https://time.geekbang.org/column/article/23132)

## Kubernetes集群搭建与实践

- [10 | Kubernetes一键部署利器：kubeadm](https://time.geekbang.org/column/article/39712)
- [11 | 从0到1：搭建一个完整的Kubernetes集群](https://time.geekbang.org/column/article/39724)
- [12 | 牛刀小试：我的第一个容器化应用](https://time.geekbang.org/column/article/40008)

## 容器编排与Kubernetes作业管理

- [13 | 为什么我们需要Pod？](https://time.geekbang.org/column/article/40092)
- [14 | 深入解析Pod对象（一）：基本概念](https://time.geekbang.org/column/article/40366)
- [15 | 深入解析Pod对象（二）：使用进阶](https://time.geekbang.org/column/article/40466)
- [16 | 编排其实很简单：谈谈"控制器"模型](https://time.geekbang.org/column/article/40583)
- [17 | 经典PaaS的记忆：作业副本与水平扩展](https://time.geekbang.org/column/article/40906)
- [18 | 深入理解StatefulSet（一）：拓扑状态](https://time.geekbang.org/column/article/41017)
- [19 | 深入理解StatefulSet（二）：存储状态](https://time.geekbang.org/column/article/41154)
- [20 | 深入理解StatefulSet（三）：有状态应用实践](https://time.geekbang.org/column/article/41217)
- [21 | 容器化守护进程的意义：DaemonSet](https://time.geekbang.org/column/article/41366)
- [22 | 撬动离线业务：Job与CronJob](https://time.geekbang.org/column/article/41607)
- [23 | 声明式API与Kubernetes编程范式](https://time.geekbang.org/column/article/41769)
- [24 | 深入解析声明式API（一）：API对象的奥秘](https://time.geekbang.org/column/article/41876)
- [25 | 深入解析声明式API（二）：编写自定义控制器](https://time.geekbang.org/column/article/42076)
- [26 | 基于角色的权限控制：RBAC](https://time.geekbang.org/column/article/42154)
- [27 | 聪明的微创新：Operator工作原理解读](https://time.geekbang.org/column/article/42493)

## Kubernetes容器持久化存储

- [28 | PV、PVC、StorageClass，这些到底在说啥？](https://time.geekbang.org/column/article/42698)
- [29 | PV、PVC体系是不是多此一举？从本地持久化卷谈起](https://time.geekbang.org/column/article/42819)
- [30 | 编写自己的存储插件：FlexVolume与CSI](https://time.geekbang.org/column/article/44245)
- [31 | 容器存储实践：CSI插件编写指南](https://time.geekbang.org/column/article/64392)

## Kubernetes容器网络

- [32 | 浅谈容器网络](https://time.geekbang.org/column/article/64948)
- [33 | 深入解析容器跨主机网络](https://time.geekbang.org/column/article/65287)
- [34 | Kubernetes网络模型与CNI网络插件](https://time.geekbang.org/column/article/67351)
- [35 | 解读Kubernetes三层网络方案](https://time.geekbang.org/column/article/67775)
- [36 | 为什么说Kubernetes只有soft multi-tenancy？](https://time.geekbang.org/column/article/68316)
- [37 | 找到容器不容易：Service、DNS与服务发现](https://time.geekbang.org/column/article/68636)
- [38 | 从外界连通Service与Service调试"三板斧"](https://time.geekbang.org/column/article/68964)
- [39 | 谈谈Service与Ingress](https://time.geekbang.org/column/article/69214)

## Kubernetes作业调度与资源管理

- [40 | Kubernetes的资源模型与资源管理](https://time.geekbang.org/column/article/69678)
- [41 | 十字路口上的Kubernetes默认调度器](https://time.geekbang.org/column/article/69890)
- [42 | Kubernetes默认调度器调度策略解析](https://time.geekbang.org/column/article/70211)
- [43 | Kubernetes默认调度器的优先级与抢占机制](https://time.geekbang.org/column/article/70519)
- [44 | Kubernetes GPU管理与Device Plugin机制](https://time.geekbang.org/column/article/70876)

## Kubernetes容器运行时

- [45 | 幕后英雄：SIG-Node与CRI](https://time.geekbang.org/column/article/71056)
- [46 | 解读 CRI 与 容器运行时](https://time.geekbang.org/column/article/71499)
- [47 | 绝不仅仅是安全：Kata Containers 与 gVisor](https://time.geekbang.org/column/article/71606)

## Kubernetes容器监控与日志

- [48 | Prometheus、Metrics Server与Kubernetes监控体系](https://time.geekbang.org/column/article/72281)
- [49 | Custom Metrics: 让Auto Scaling不再"食之无味"](https://time.geekbang.org/column/article/72693)
- [50 | 让日志无处可逃：容器日志收集与管理](https://time.geekbang.org/column/article/73156)

## 再谈开源与社区

- [51 | 谈谈Kubernetes开源社区和未来走向](https://time.geekbang.org/column/article/73477)

## 答疑文章

- [52 | 答疑：在问题中解决问题，在思考中产生思考](https://time.geekbang.org/column/article/73790)

## 特别放送

- [特别放送 | 2019 年，容器技术生态会发生些什么？](https://time.geekbang.org/column/article/83596)
- [特别放送 | 基于 Kubernetes 的云原生应用管理，到底应该怎么做？](https://time.geekbang.org/column/article/114197)

## 结束语

- [结束语 | Kubernetes：赢开发者赢天下](https://time.geekbang.org/column/article/74278)

## 结课测试

- [结课测试｜这些Kubernetes的相关知识，你都掌握了吗？](https://time.geekbang.org/column/article/224358)
