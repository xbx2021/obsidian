
这是**Java 集合框架（HashMap/HashSet等）的强制约定**，也是面试高频考点。核心一句话：
**equals 相等的两个对象，hashCode 必须相等；但 hashCode 相等的两个对象，equals 不一定相等。**

如果只重写一个，会导致**HashSet存重复对象、HashMap查不到值**等致命BUG。

---

## 一、先搞懂两个方法的作用
### 1. `equals()`
- 作用：**判断两个对象是否“逻辑相等”**
- 默认实现（Object类）：比较**内存地址**，`==`
- 重写后：按业务规则判断（比如两个学生`id`相同就算相等）

### 2. `hashCode()`
- 作用：返回一个**int哈希值**，给哈希表（HashMap/HashSet）用
- 默认实现：根据对象内存地址计算
- 哈希表靠它**快速定位对象位置**

---

## 二、Java 的官方强制约定（必须背）
1. **如果两个对象调用 `equals()` 返回 true**
   → 它们的 `hashCode()` **必须返回相同的值**
2. **如果两个对象 `equals()` 返回 false**
   → 它们的 `hashCode()` **可以相同，也可以不同**（最好不同，提高效率）

---

## 三、只重写 equals，不重写 hashCode：会出什么BUG？
举个最直观的例子：
我们定义一个`User`类，只重写`equals()`（id相同即相等），**不重写`hashCode()`**。

```java
class User {
    private int id;

    public User(int id) {
        this.id = id;
    }

    // 只重写 equals
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return id == user.id;
    }

    // 故意不重写 hashCode！
}
```

### 测试代码（BUG出现）
```java
public class Test {
    public static void main(String[] args) {
        User u1 = new User(1);
        User u2 = new User(1);

        // 1. equals 相等（符合预期）
        System.out.println(u1.equals(u2)); // true

        // 2. 存入 HashSet（Set本应该去重）
        HashSet<User> set = new HashSet<>();
        set.add(u1);
        set.add(u2);

        // 3. 结果：Set里存了两个"相等"的对象！BUG！
        System.out.println(set.size()); // 输出 2（本应该是1）
    }
}
```

### 为什么会这样？
1. HashSet 添加元素时，**先算 hashCode 定位桶位置**
2. u1 和 u2 用的是**默认 hashCode**（按内存地址算）→ **hashCode 不同**
3. 哈希表认为它们是**两个不同位置的对象**，直接都存进去
4. 完全无视了`equals()`返回true → **违反去重规则**

---

## 四、只重写 hashCode，不重写 equals：也会BUG
如果只重写`hashCode()`，不重写`equals()`：
- 两个对象hashCode相同 → 哈希表放到同一个桶里
- 但`equals()`比较的是内存地址 → 返回false
- 最终还是会**存重复对象**，同样失效

---

## 五、正确写法：两个方法一起重写
遵循规则：**参与 equals 判断的属性，必须全部参与 hashCode 计算**

```java
class User {
    private int id;
    private String name;

    public User(int id, String name) {
        this.id = id;
        this.name = name;
    }

    // 1. 重写 equals：用 id + name 判断相等
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return id == user.id && Objects.equals(name, user.name);
    }

    // 2. 重写 hashCode：必须用和 equals 相同的属性
    @Override
    public int hashCode() {
        return Objects.hash(id, name);
    }
}
```

✅ 现在：
- `u1.equals(u2) == true` → `u1.hashCode() == u2.hashCode()`
- HashSet/HashMap 能**正常去重、正常查询**

---

## 六、底层原理：哈希表怎么工作？
以 HashMap 为例，存/查对象分两步：
1. **算 hashCode** → 快速找到数组下标（桶）
2. **桶内用 equals 逐个比较** → 确认是否是同一个对象

### 流程总结
```
存入对象 → 计算hashCode → 定位桶位置
→ 桶内遍历：用equals判断是否已存在
→ 存在则覆盖，不存在则新增
```

如果破坏约定：
- equals相等、hashCode不等 → 分到不同桶 → **重复存储**
- equals不等、hashCode相等 → 同一个桶，equals判断后正常存储（只是哈希冲突）

---

### 总结
1. **核心约定**：equals 相等 → hashCode 必须相等
2. **不重写的后果**：HashSet/HashMap 失效，存重复值、查不到数据
3. **开发规范**：**两个方法必须同时重写**，且使用**相同的属性**
4. **工具推荐**：直接用 IDEA 自动生成（Alt+Insert），不要手写