title: 使用二分法求整数幂
date: 2015-12-3
tags: [C,C++,ACM,算法]
categories: 算法
toc: true
---

### 引言

在应用中求幂是一个经常使用到的运算。
那么我们求幂的时候是不是经常这样写

```
int power(int x,  int n)
{
    int result = 1;
    while (n--)
        result *= x;
    return result;
}
```

这样写简单直观，但是时间复杂度太高了。

### 解决思路

为了减少时间的消耗，我们可以使用**二分法**。

**举个例子：求2的8次幂。**

**设结果为result** 

```
result = 2^8
设result1 = 2^4，很容易推出 result  =  result1*result1
设result2 = 2^2，同理，result1 = result2*result2
......
```

```
再举个例子,result3 = 2^7
那么 result3 = result1 * 2^3
2^3 = 2^2 *2^1
```

那么规律出来了，我们可以写程序了

### &和&&的区别

这里用了一些不常用的C的知识，有可能比较晦涩难懂。
**稳妥起见，这里再复习一下C的知识**

#### &--按位与

举个例子  
 7的二进制是0111，1的二进制是0001；
 7&1 即是  0111&0001  = 0001（二进制） = 1（十进制）；
再举个例子  
 11&6  即是 1011&0110 = 0010 = 2;

#### &&--逻辑与

这个很简单了，只要两个数都不为0 ；结果就是1
10&&1 = 1；
1&0 = 0；

#### <<，>>  位左移和位右移

依旧举例，将8向左移两位，
8 >> 2 即为 1000（二进制） 左移两位，结果就是10（二进制），化为十进制那就是2；
**P.S : n >>= 2 与 n =  n>>2 结果相同。**
但是在运算速度和内存占用上比后者好一些，这里就不给出详细的解释了。


### 核心代码

```
int power(int x, int n)
{
    if (n == 0)
        return 1;
    int result = 1;
    while (n != 0)
    {
        if ((n & 1) != 0)
            result *= x;
        x *= x;
        n >>= 1;
    }
    return result;
}
```

