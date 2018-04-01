title: 后端基本素养 - FailFast
date: 2018-3-26 21:26:29
tags: [后端基本素养,随笔]
categories: 生活
toc: true
---

很多语言都会有异常机制。

对于 `Java` 而言，异常机制可以说是非常完善（或者说非常难用）了。

为什么这么说，举个栗子：
``` java
    private Map<String, VideoTransferTemplate> getTemplateMapByPath(String path) {
        InputStream input = this.getClass().getClassLoader().getResourceAsStream(path);
        try {
            String jsonString = StreamUtils.copyToString(input, Charset.defaultCharset());
            return ObjectMapperUtils.fromJSON(jsonString, HashMap.class, String.class,
                    VideoTransferTemplate.class);
        } catch (IOException e) {
            // WTF .....
        }
    }
```

这是一段很平常的涉及文件 IO 的代码，代码不长，逻辑也很简单。
但是我们发现这段代码需要用一个 `try` 裹住才能正常通过编译。这就是 `Java` 中集万千宠爱与一身的 `Checked Exception`。只要你调用的方法里生命有 `Checked Exception` 你就必须显式地用 `try` 把他裹住，然后在附带的 `catch` 中编写你根本不知道应该怎么编写的代码。

`catch` 中写什么好呢？

在我见过的程序员中，分成以下几个流派。

##### IDE 生成代码就不管派
``` java
        try {
            String jsonString = StreamUtils.copyToString(input, Charset.defaultCharset());
        } catch (IOException e) {
            // TODO 这是一个 IDE 生成的 TODO，被程序员原原本本地保存下来了
            e.printStackTrace();
        }
```

这个流派的程序员会使用快捷键生成一个 `try .. catch` 语句，并在方法的最后返回一个 `null` 。
这可能是最简单便捷的让编译器继续工作的方式，但却是最坏的逃避问题的方式，我们简单称为 “吃掉异常”。

这样处理有两个很显著的问题：
首先，返回一个 `null`，调用者可能会发生 `NPE`。因为你把异常吃掉了而给我返回空指针，我啥也不知道就直接用它了。这个时候相当于把 `Checked Exception` 转换成了 `RuntimeException`。而这个转换糟糕的是，调用者根本不知道到底是什么原因造成了他的  `NPE`.

而那行经典的 `e.printStackTrace();` 更是令人觉得无可奈何...这个不说了。

##### 添加 `throws` 声明派
好吧，`StreamUtils#copyToString` 方法会抛一个 `IOException` 我不知道怎么处理，那还是把这个异常直接抛给调用方吧。

典型代码如下：
``` java
    private Map<String, VideoTransferTemplate> getTemplateMapByPath(String path)
            throws IOException {
        InputStream input = this.getClass().getClassLoader().getResourceAsStream(path);
        String jsonString = StreamUtils.copyToString(input, Charset.defaultCharset());
        return ObjectMapperUtils.fromJSON(jsonString, HashMap.class, String.class,
                VideoTransferTemplate.class);
    }
```

这个时候，这个方法的代码不需要处理讨厌的异常了，如果有方法调用抛出异常，那么就直接把这个异常交给我的调用方去处理吧。

有的时候会有一些不是很严重的异常，我需要通知给调用方。

举个栗子，一个 `LoginService` 中，组合了一些 `UserService` 和 `PasswordService` 。而需要调用的 `UserService` 和 `PasswordService` 的一些方法中都会抛出一些 `Checked Exception` 。 `UserService` 的调用方希望能直接捕捉到这些异常，并分类做 `log` 和 `kafka` 上报。

在这样的时候，这样处理是最科学的，因为调用的上层很关心这些异常，而且希望将这些异常都捕获到。

##### `RuntimeException` 派
这个流派可能是目前最流行的流派：把 `Checked Exception` 转成 `Runtime Exception` ，典型做法是：
``` java
    private Map<String, VideoTransferTemplate> getTemplateMapByPath(String path) {
        InputStream input = this.getClass().getClassLoader().getResourceAsStream(path);
        try {
            String jsonString = StreamUtils.copyToString(input, Charset.defaultCharset());
            return ObjectMapperUtils.fromJSON(jsonString, HashMap.class, String.class,
                    VideoTransferTemplate.class);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
```

这样处理异常的做法，也叫做 `Fail Fast`。
为什么这样处理，只有一个理由：发生了这个 Exception，后面的事情都干不下去了，尽快把程序结束掉吧！

这就是 `Fail Fast`，在发生不可预期的错误的时候，直接抛 `Runtime Exception` （在 Go 中是一个 `panic` ），及时地让程序异常退出。


#### Fail Fast 的引申
其实 Fail Fast 不仅仅用在异常上，其他的很多情况也需要用 Fail Fast。

比如你读取一个 `ZooKeeper` 上的配置（很关键的一个配置，涉及到很重要的资源调度）。这个时候读取到的数据格式不合法，那么资源调度这个配置怎么处理呢？

有两种处理方式：
1. 使用默认的配置（这个配置可能没有，或者说有些“默认配置”实现起来很恶心）
2. 直接抛异常，也即是我们所说的 Fail Fast。

可能很多人对 Fail Fast 觉得很不可思议，觉得这么轻易就把程序结束掉了，不符合“程序怎么都不能挂”这个所谓的“程序员真谛”。

在另外一个角度来说，有错误或者异常应该及早暴露出来，让程序员去解决，而不是默默待在角落哭泣，因为等大家发现的时候很可能已经造成很大损失了。

在一个完备的灰度上线，失败报警的后端系统中，使用 Fail Fast，是非常合适的。
