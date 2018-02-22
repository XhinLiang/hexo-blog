title: 构造函数需要加锁吗
date: 2018-02-20 22:58:29
tags: [Java]
categories: Java
toc: true
---

我们在写 Java 的时候，经常会使用到 `synchronized` 关键字。
`synchronized` 是一个相对重量级的锁，它有两种使用形式。


1. 对一个具体的变量加锁。
```
        Logger l = LoggerFactory.getLogger(getClass().getName());
        synchronized (l) {
            // do something
        }
        
        synchronized (this) {
            // do something
        }
```

2. 修饰方法，可以是普通方法，也可以是静态方法。这事实上也是对 `this` 加锁。
```
    // 普通方法
    private synchronized void doSomething() {
        // something
    }

    // 上面等效
    private void doNothing() {
        synchronized (this) {
            // do something
        }
    }

    private static synchronized void doSomethingStatic() {
        // something
    }
```

`synchronized` 非常常见，但是大家有没有见过在构造函数里用 `synchronized` 修饰的呢？

事实上，如果在构造函数里加上 `synchronized` 修饰符，你的编译会失败。

聪明的编译器会告诉你 **此处不允许使用修饰符synchroniz**

明确一点，如果在构造函数里使用 `synchronized` 修饰符的话，事实上是对 `this` 加锁。

但是为什么这个地方不允许使用 `synchronized` 修饰符呢？

我认为有两个原因：

1. 在构造函数中，`this` 事实上没有完全构造好，还没有准备好。

2. 构造函数中， `this` 还没有被传递出去，事实上不存在并发问题。

第一个原因大家都能懂，第二个可能要好好说下。

在 Java 的并发模型里，最重要的就是变量的可见性。
多个线程同时对一个对象调用其某个方法，那么这个时候就有可能出现并发问题。

那么，对一个对象进行 `new` 的时候，事实上不可能存在多个线程同时 `new` 同一个对象，那么也就是正常情况下，不存在对 `this` 的并发安全性问题，所以，在构造函数中，对 `this` 加锁，是完全没有意义的。

有个情况例外，如果你在构造函数中，提前把 `this` 暴露到某个地方，就有可能存在构造函数中也存在并发安全性问题。例如：
```
    private static Object that;
    
    // 请不要这样做
    public Server() {
        that = this;
    }
```
这是个非常不好的习惯，我们在实际应用中应该尽量避免这样做。

有些朋友可能会问，那如果在构造函数中传递某个对象，会不会出现并发安全性问题。
答案当然是会。如果要规避这些问题，那么你在构造函数里，不应该是对 `this` 加锁，而是应该**在构造函数中对所涉及到的有并发安全性问题的对象进行加锁**，或者在构造函数之外对这个对象进行加锁（不常用）。

记住：构造函数本身是并发安全的，只是因为额外添加了不安全的参数，导致了构造函数的不安全。
