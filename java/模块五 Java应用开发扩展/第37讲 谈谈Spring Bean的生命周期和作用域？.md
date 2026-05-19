![](assets/第37讲%20谈谈Spring%20Bean的生命周期和作用域？/file-20260519091625600.png)

在企业应用软件开发中，Java 是毫无争议的主流语言，开放的 Java EE 规范和强大的开源框架功不可没，其中 Spring 毫无疑问已经成为企业软件开发的事实标准之一。今天这一讲，我将补充 Spring 相关的典型面试问题，并谈谈其部分设计细节。

今天我要问你的问题是，**谈谈 Spring Bean 的生命周期和作用域？**

# 典型回答

Spring Bean 生命周期比较复杂，可以分为创建和销毁两个过程。

首先，创建 Bean 会经过一系列的步骤，主要包括：

- 实例化 Bean 对象。
- 设置 Bean 属性。
- 如果我们通过各种 Aware 接口声明了依赖关系，则会注入 Bean 对容器基础设施层面的依赖。具体包括 BeanNameAware、BeanFactoryAware 和 ApplicationContextAware，分别会注入 Bean ID、Bean Factory 或者 ApplicationContext。
- 调用 BeanPostProcessor 的前置初始化方法 postProcessBeforeInitialization。
- 如果实现了 InitializingBean 接口，则会调用 afterPropertiesSet 方法。
- 调用 Bean 自身定义的 init 方法。
- 调用 BeanPostProcessor 的后置初始化方法 postProcessAfterInitialization。
- 创建过程完毕。

你可以参考下面示意图理解这个具体过程和先后顺序。
![](assets/第37讲%20谈谈Spring%20Bean的生命周期和作用域？/file-20260519091926368.png)

第二，Spring Bean 的销毁过程会依次调用 DisposableBean 的 destroy 方法和 Bean 自身定制的 destroy 方法。

Spring Bean 有五个作用域，其中最基础的有下面两种：

- **Singleton**，这是 Spring 的默认作用域，也就是为每个 IOC 容器创建唯一的一个 Bean 实例。
- **Prototype**，针对每个 getBean 请求，容器都会单独创建一个 Bean 实例。

从 Bean 的特点来看，Prototype 适合有状态的 Bean，而 Singleton 则更适合无状态的情况。另外，使用 Prototype 作用域需要经过仔细思考，毕竟频繁创建和销毁 Bean 是有明显开销的。

如果是 Web 容器，则支持另外三种作用域：

- **Request**，为每个 HTTP 请求创建单独的 Bean 实例。
- **Session**，很显然 Bean 实例的作用域是 Session 范围。
- **GlobalSession**，用于 Portlet 容器，因为每个 Portlet 有单独的 Session，GlobalSession 提供一个全局性的 HTTP Session。

# 考点分析

今天我选取的是一个入门性质的高频 Spring 面试题目，我认为相比于记忆题目典型回答里的细节步骤，理解和思考 Bean 生命周期所体现出来的 Spring 设计和机制更有意义。

你能看到，Bean 的生命周期是完全被容器所管理的，从属性设置到各种依赖关系，都是容器负责注入，并进行各个阶段其他事宜的处理，Spring 容器为应用开发者定义了清晰的生命周期沟通界面。

如果从具体 API 设计和使用技巧来看，还记得我在专栏第 13 讲提到过的 Marker Interface 吗，Aware 接口就是个典型应用例子，Bean 可以实现各种不同 Aware 的子接口，为容器以 Callback 形式注入依赖对象提供了统一入口。

言归正传，还是回到 Spring 的学习和面试。关于 Spring，也许一整本书都无法完整涵盖其内容，专栏里我会有限地补充：

- Spring 的基础机制。
- Spring 框架的涵盖范围。
- Spring AOP 自身设计的一些细节，前面第 24 讲偏重于底层实现原理，这样还不够全面，毕竟不管是动态代理还是字节码操纵，都还只是基础，更需要 Spring 层面对切面编程的支持。

# 知识扩展

## Spring 基础机制

首先，我们先来看看 Spring 的基础机制，至少你需要理解下面两个基本方面。

- **控制反转**（Inversion of Control），或者也叫**依赖注入**（Dependency Injection），广泛应用于 Spring 框架之中，可以有效地改善了模块之间的紧耦合问题。

从 Bean 创建过程可以看到，它的依赖关系都是由容器负责注入，具体实现方式包括带参数的构造函数、setter 方法或者[AutoWired](https://docs.spring.io/spring-framework/docs/5.0.3.RELEASE/javadoc-api/org/springframework/beans/factory/annotation/Autowired.html)方式实现。

- **AOP**，我们已经在前面接触过这种切面编程机制，Spring 框架中的事务、安全、日志等功能都依赖于 AOP 技术，下面我会进一步介绍。

## Spring 是什么

第二，Spring 到底是指什么？

我前面谈到的 Spring，其实是狭义的[Spring Framework](https://github.com/spring-projects/spring-framework/blob/67ea4b3a050af3db5545f58ff85a0d132ee91c2a/spring-aop/src/main/java/org/aopalliance/aop/Advice.java)，其内部包含了依赖注入、事件机制等核心模块，也包括事务、O/R Mapping 等功能组成的数据访问模块，以及 Spring MVC 等 Web 框架和其他基础组件。

广义上的 Spring 已经成为了一个庞大的生态系统，例如：

- **Spring Boot**，通过整合通用实践，更加自动、智能的依赖管理等，Spring Boot 提供了各种典型应用领域的快速开发基础，所以它是以应用为中心的一个框架集合。

- **Spring Cloud**，可以看作是在 Spring Boot 基础上发展出的更加高层次的框架，它提供了构建分布式系统的通用模式，包含服务发现和服务注册、分布式配置管理、负载均衡、分布式诊断等各种子系统，可以简化微服务系统的构建。

- 当然，还有针对特定领域的 Spring Security、Spring Data 等。

上面的介绍比较笼统，针对这么多内容，如果将目标定得太过宽泛，可能就迷失在 Spring 生态之中，我建议还是深入你当前使用的模块，如 Spring MVC。并且，从整体上把握主要前沿框架（如 Spring Cloud）的应用范围和内部设计，至少要了解主要组件和具体用途，毕竟如何构建微服务等，已经逐渐成为 Java 应用开发面试的热点之一。

## Spring AOP

第三，我们来探讨一下更多有关 Spring AOP 自身设计和实现的细节。

先问一下自己，我们为什么需要切面编程呢？

