![](assets/第12讲%20Java有几种文件拷贝方式？哪一种最高效？/file-20260513151434941.png)

我在专栏上一讲提到，NIO 不止是多路复用，NIO 2 也不只是异步 IO，今天我们来看看 Java IO 体系中，其他不可忽略的部分。

今天我要问你的问题是，**Java 有几种文件拷贝方式？哪一种最高效？**

# 典型回答

Java 有多种比较典型的文件拷贝实现方式，比如：

利用 java.io 类库，直接为源文件构建一个 FileInputStream 读取，然后再为目标文件构建一个 FileOutputStream，完成写入工作。
```java
public static void copyFileByStream(File source, File dest) throws
        IOException {
    try (InputStream is = new FileInputStream(source);
         OutputStream os = new FileOutputStream(dest);){
        byte[] buffer = new byte[1024];
        int length;
        while ((length = is.read(buffer)) > 0) {
            os.write(buffer, 0, length);
        }
    }
 }
```

或者，利用 java.nio 类库提供的 transferTo 或 transferFrom 方法实现。
```java
public static void copyFileByChannel(File source, File dest) throws
        IOException {
    try (FileChannel sourceChannel = new FileInputStream(source)
            .getChannel();
         FileChannel targetChannel = new FileOutputStream(dest).getChannel
                 ();){
        for (long count = sourceChannel.size() ;count>0 ;) {
            long transferred = sourceChannel.transferTo(
                    sourceChannel.position(), count, targetChannel);            sourceChannel.position(sourceChannel.position() + transferred);
            count -= transferred;
        }
    }
 }
```

