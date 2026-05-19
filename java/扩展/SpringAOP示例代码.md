# Spring AOP 极简示例（最常用、最易懂版本）

我给你写一个**纯注解、可直接运行**的 Spring AOP 入门案例，包含：日志打印、方法执行时间统计、统一异常处理。

## 1. 先加依赖（Maven）
```xml
<!-- Spring Boot 启动器（自动配置AOP） -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>

<!-- Spring Web（用来写测试接口） -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

## 2. 核心：AOP 切面类（重点）
```java
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;

@Aspect // 声明这是一个切面
@Component // 交给Spring管理
public class LogAspect {

    // ===================== 1. 定义切点（哪些方法需要被增强） =====================
    // 匹配 com.example.demo 包下所有类的所有方法
    @Pointcut("execution(* com.example.demo..*.*(..))")
    public void pointCut() {}

    // ===================== 2. 前置通知（方法执行前） =====================
    @Before("pointCut()")
    public void before(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("【前置通知】开始执行方法：" + methodName);
    }

    // ===================== 3. 后置通知（方法正常执行后） =====================
    @AfterReturning(pointcut = "pointCut()", returning = "result")
    public void afterReturning(JoinPoint joinPoint, Object result) {
        System.out.println("【后置通知】方法执行完毕，返回值：" + result);
    }

    // ===================== 4. 异常通知（方法抛异常时执行） =====================
    @AfterThrowing(pointcut = "pointCut()", throwing = "ex")
    public void afterThrowing(JoinPoint joinPoint, Exception ex) {
        System.out.println("【异常通知】方法报错：" + ex.getMessage());
    }

    // ===================== 5. 最终通知（无论是否异常都会执行） =====================
    @After("pointCut()")
    public void after(JoinPoint joinPoint) {
        System.out.println("【最终通知】方法执行结束\n");
    }

    // ===================== 6. 环绕通知（最强大，控制整个方法执行） =====================
    @Around("pointCut()")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();

        // 执行目标方法
        Object result = pjp.proceed();

        long end = System.currentTimeMillis();
        System.out.println("【环绕通知】方法耗时：" + (end - start) + "ms");
        return result;
    }
}
```

## 3. 写一个测试业务类
```java
package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    // 正常接口
    @GetMapping("/test")
    public String test() {
        System.out.println("=== 目标方法正在执行 ===");
        return "AOP 测试成功";
    }

    // 抛异常接口（测试异常通知）
    @GetMapping("/error")
    public String error() {
        int i = 1 / 0;
        return "不会执行到这里";
    }
}
```

## 4. 启动类
```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

---

## 运行结果（访问 /test）
```
【前置通知】开始执行方法：test
=== 目标方法正在执行 ===
【后置通知】方法执行完毕，返回值：AOP 测试成功
【最终通知】方法执行结束
【环绕通知】方法耗时：1ms
```

访问 `/error` 会触发**异常通知**。

---

## AOP 核心概念（一句话看懂）
| 注解 | 作用 |
|---|----------------|
| @Aspect | 标记这是一个**切面** |
| @Pointcut | 定义**切点**：哪些方法需要增强 |
| @Before | 方法**执行前**执行 |
| @AfterReturning | 方法**正常返回后**执行 |
| @AfterThrowing | 方法**抛异常**时执行 |
| @After | 方法**最终一定执行**（无论成败） |
| @Around | **环绕整个方法**（最强大） |

---

### 总结
1. 这个例子是**Spring Boot 最标准的 AOP 用法**，企业开发通用；
2. 无需任何 XML，纯注解；
3. 包含了 AOP 所有核心通知类型；
4. 复制即可直接运行。


# Spring AOP 自定义注解实现（权限校验实战）
## 1. 引入依赖
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

## 2. 自定义权限注解
```java
import java.lang.annotation.*;

@Target(ElementType.METHOD) // 作用在方法上
@Retention(RetentionPolicy.RUNTIME) // 运行时生效
@Documented
public @interface CheckPermission {
    // 定义需要的权限标识
    String value();
}
```

## 3. 编写AOP切面拦截注解
```java
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;

@Aspect
@Component
public class PermissionAspect {

    // 切点：拦截所有加了 @CheckPermission 注解的方法
    @Pointcut("@annotation(com.example.demo.CheckPermission)")
    public void permissionPoint(){}

    // 环绕通知做权限校验
    @Around("permissionPoint()")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        // 1. 获取目标方法
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        Method method = signature.getMethod();

        // 2. 获取注解上的权限值
        CheckPermission permission = method.getAnnotation(CheckPermission.class);
        String needPerm = permission.value();
        System.out.println("接口需要权限：" + needPerm);

        // 模拟当前用户拥有的权限
        String userPerm = "admin";

        // 3. 权限判断
        if (!needPerm.equals(userPerm)) {
            return "权限不足，拒绝访问";
        }

        // 4. 权限通过，执行目标方法
        return joinPoint.proceed();
    }
}
```

## 4. 业务接口使用注解
```java
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PermController {

    // 需要 admin 权限
    @GetMapping("/admin")
    @CheckPermission("admin")
    public String adminApi(){
        return "欢迎进入管理员后台";
    }

    // 需要 user 权限
    @GetMapping("/user")
    @CheckPermission("user")
    public String userApi(){
        return "普通用户页面";
    }
}
```

## 5. 启动类
```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AopApplication {
    public static void main(String[] args) {
        SpringApplication.run(AopApplication.class,args);
    }
}
```

## 6. 运行测试
- 访问 `/admin` → 权限匹配，正常返回数据
- 访问 `/user` → 权限不匹配，返回**权限不足，拒绝访问**

## 常用拓展场景
1. **接口日志记录**：注解标记接口，自动记录入参、出参、操作人
2. **接口限流**：注解设置访问次数，AOP拦截限流
3. **事务控制**：简易本地事务切面
4. **数据脱敏**：返回结果自动脱敏手机号、身份证
