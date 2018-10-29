title: Java 计数器的 “线程安全” 和 “非线程安全” 实现
date: 2018-1-1 00:36:29
tags: [Java,Concurrent,并发,计数器,线程安全]
categories: Java
toc: true
---

> 计数器是一个很常见的需求，这里使用 Java 实现了计数器的线程安全和非线程安全版本

#### `ICounter` 接口
``` java
public interface ICounter<E> {
    void add(E e);
    long get(E e);
}
```

#### `Counter` 非线程安全版本
``` java
public class Counter<E> implements ICounter<E>{
    private Map<E, long[]> map;

    public Counter() {
        this.map = new HashMap<>();
    }

    @Override
    public void add(E e) {
        long[] mutableLong = map.get(e);
        if (mutableLong == null) {
            map.put(e, new long[]{1L});
            return;
        }
        mutableLong[0] += 1L;
    }

    @Override
    public long get(E e) {
        long[] mutableLong = map.get(e);
        if (mutableLong == null) {
            return 0L;
        }
        return mutableLong[0];
    }

    public static void main(String[] args) throws InterruptedException {
        ICounter<String> counter = new Counter<>();
        for (int i = 0; i < 1; ++i) {
                for (int j = 0; j < 1000000; ++j) {
                    counter.add("a");
                }
        }
        System.out.println(counter.get("a"));
    }
}
```

#### 线程安全版本
``` java
public class ConcurrentCounter<E> implements ICounter<E>{
    private Map<E, AtomicLong> map;

    public ConcurrentCounter() {
        this.map = new ConcurrentHashMap<>();
    }

    public void add(E e) {
        AtomicLong atomicLong = map.putIfAbsent(e, new AtomicLong(1L));
        if (atomicLong != null) {
            atomicLong.getAndAdd(1L);
        }
    }

    public long get(E e) {
        AtomicLong atomicLong = map.get(e);
        if (atomicLong == null) {
            return 0L;
        }
        return atomicLong.get();
    }

    public static void main(String[] args) throws InterruptedException {
        ConcurrentCounter<String> counter = new ConcurrentCounter<>();
        Thread[] threads = new Thread[10000];

        for (int i = 0; i < 10000; ++i) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10000; ++j) {
                    counter.add("a");
                }
            });
            threads[i].start();
        }
        for (int i = 0; i < 10000; ++i) {
            threads[i].join();
        }
        System.out.println(counter.get("a"));
    }
}
```
