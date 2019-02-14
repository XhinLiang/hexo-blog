title: 两道算法题
date: 2016-03-23 21:02:29
tags: [算法,面试,C]
categories: 算法
toc: true
---
## 前言
昨天参与了某个互联网公司的在线笔试，里面有两道算法题，无奈时间不够只写了一道。

更糟糕的是，今天醒来才发现自己花了好大心思写的那道题，却由于粗心把题意弄反了。

遗憾之余，今天用现代化的编程工具写一遍，弥补自己悲伤的情绪。


## 题目

### 第 k 大数
#### 描述
输入两个数 n 和 k ，给出一个长度为 n 的数组，参考快速排序，输出出数组里第 k 大的数并换行。
多组数据，当输入的 n 为 0 时结束。

*诡异的是，题目给出来两个个函数声明，让答题者提供这两个函数的具体实现*

不管他，姑且当做 ACM 来写吧。
 
#### 示例输入
5 2
11 4 22 45 2 21
0 0

#### 示例输出
21

#### 解析
题目已经提示参考快速排序，那么解题的思想肯定跟快速排序有关。

快速排序的原理我就不多说了，没有接触过快速排序或者说已经忘了的同学，可以看一看我这篇博客 [简明数据结构](xhinliang.github.io/2016/03/08/Clear_data_structure/) ，还有快速排序的参考代码 [Quick_sort](https://github.com/XhinLiang/Structure/blob/master/sort/quick_sort.c) 。

经过排序，我们肯定可以直接找出数组里第 k 大的元素。问题是，有必要吗？

在快速排序中，我们每次找出一个基准数，经过处理，在这一步排序中，我们把这个基准数放在它最终排序的位置，接着对目前排在这个基准数前面和后面的两个子数组进行快速排序。

如果我们在某一次排序中，找出来的基准数安置的位置恰好是我们提供的 k ，那么这个基准数就一定是我们要找的第 k 大的数。

#### 代码
``` c
/*
 * XX2016实习生招聘
 * 根据快速排序的算法，找出数组中第 k 大的数，k 从 0 开始数。
 */
#include <stdio.h>
#include <stdlib.h>

#define N 10000

int kth_number(int *array, const int length, const int k) {
    int stand = array[0];
    int start = 0;
    int end = length - 1;
    while (start < end) {
        while (start < end && array[end] < stand)
            --end;
        array[start] = array[end];
        if (start == end)
            break;
        while (start < end && array[start] > stand)
            ++start;
        array[end] = array[start];
    }
    array[start] = stand;
    // 这时候所在的这个部分已经排好序了，这也是这个算法的最坏情况
    if (length < 3)
        return array[k];
    if (start == k)
        return stand;
    if (k < start) {
        if (start < 2)
            return array[k];
        return kth_number(array, start, k);
    }
    // k > start
    if (length - start < 3)
        return array[k];
    return kth_number(array + start + 1, length - start - 1, k - start - 1);
}

int main() {
    int i, n, k;
    int *array = (int *) malloc(N * sizeof(int));
    scanf("%d%d", &n, &k);
    while (n > 0) {
        for (i = 0; i < n; ++i)
            scanf("%d", array + i);
        printf("%d\n", kth_number(array, n, k));
        scanf("%d%d", &n, &k);
    }
    free(array);
    return 0;
}
```


### 钻石比重量
有一堆钻石，每个钻石有唯一的编号 0，1，2，3 ... 其中有些钻石已经比较过重量（每个钻石比较的次数大于等于 1 ），这里有两个没有直接比较过的钻石，求这两个钻石的重量比较结果。

#### 待续
这道题更过分，没有给输入和输出，只提供一个 C++ 的函数头，我这个用 C 的可怜家伙直接就懵了。这没有函数头，不给规范输入输出的，实在没办法做。

再加上这道题的输入有点麻烦，就先不写了。

#### 我的想法
应该可以使用有向图搜索（这里深度或者广度搜索应该是一样的）解题，具体也没试过。

## 吐槽
我自己的错误不怪人家，但是这笔试的环境着实糟糕，必须吐槽。

作为编程题目，需要绝对明确的题目要求。要么使用标准 ACM Judge 的方法 -- 标准输入输出，要么借鉴 LeetCode 的方案，给出函数声明，要求完善函数体。而这次笔试，又给出来函数头（只有 C++ 版本的函数头），又有输入输出，真是不知道闹哪样了。

在线笔试，不让切换网页窗口，必须在网页端写代码，这无可厚非。但是这糟糕的自动换行，让我写起代码来就想泡浆糊里一样难受。还有，代码字体不等宽是要逼死我等强迫症吗？？ 

还有，在编程环境极差的网页端写完代码，能不能让跑一下示例数据啊？？我就是这么样被一波带走的。


