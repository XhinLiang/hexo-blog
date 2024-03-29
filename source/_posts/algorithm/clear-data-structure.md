title: 简明数据结构
date: 2016-03-8 13:28:29
tags: [Python,C,算法,数据结构]
categories: 算法
toc: true
---

> 数据结构是一门很重要的计算机基础课，知识点多而且难度不小，这里列出了数据结构中比较容易遗忘的内容。

*在这篇博客中，我尽量用我觉得最好理解的方式描述一个算法，简明扼要，相关的代码可能不完全，如果有兴趣的话欢迎访问我的 GitHub *

#### 字符串快速匹配 - KMP

- next 数组的求解，即部分匹配值
``` c
int q = 1, k = 0;
next[0] = 0;
for (q = 1; q < length; ++q){
    while (k > 0 && pattern[q] != pattern[k])
        k = next[k - 1];
    if (pattern[q] == pattern[k])
        ++k;
    next[q] = k;
}
```

- 根据 next 数组进行匹配跳跃
``` c
// 移动位数 = 已匹配的字符数 - 对应的部分匹配值
int i = -1, q = 0;
while(++i < source_length) {
    while(q > 0 && pattern[q] != source[i])
        q = next[q-1];
    if (pattern[q] == source[i])
        ++q;
    if (q == pattern_length)
        return i - pattern_length + 1;
}
```
[参考链接](http://www.cnblogs.com/c-cloud/p/3224788.html)

#### 二叉树的遍历 - 先序，中序，后序

- 先序，首先访问根结点，然后遍历左子树，最后遍历右子树
``` c
void pre_order(TreeNode* node) {
    if(node != NULL) {
        printf("%d ",node->data);
        pre_order(node->left);
        pre_order(node->right);
    }
}
```
- 中序，首先遍历左子树，然后访问根结点，最后遍历右子树
``` c
void mid_order(TreeNode* node) {
    if(node != NULL) {
        mid_order(node->left);
        printf("%d ",node->data);
        mid_order(node->right);
    }
}
```
- 后序，首先遍历左子树，然后遍历右子树，最后访问根结点
``` c
void post_order(TreeNode* node) {
    if(node != NULL) {
        post_order(node->left);
        post_order(node->right);
        printf("%d ",node->data);
    }
}
```

#### 二叉树应用

- 线索二叉树，利用空的左右指针，加上左右 tag 标志，快速定位二叉树的前趋和后继，使二叉树更容易遍历。
- 赫夫曼树，所有叶子结点的带权路径长度之和最小的二叉树。
``` c
赫夫曼树构成方法
1. 将所有节点各看成一颗树；
2. 在森林中选出两个根结点的权值最小的树合并，作为一棵新树的左、右子树，且新树的根结点权值为其左、右子树根结点权值之和；
3. 从森林中删除选取的两棵树，并将新树加入森林；
4. 重复 2, 3 步，直到森林中只剩一棵树为止，该树即为所求得的哈夫曼树。
```
#### 二叉查找树

**特性**
- 若任意节点的左子树不空，则左子树上所有结点的值均小于它的根结点的值；
- 任意节点的右子树不空，则右子树上所有结点的值均大于它的根结点的值；
- 任意节点的左、右子树也分别为二叉查找树；
- 没有键值相等的节点。

**查找**
- 若b是空树，则搜索失败，否则：
- 若x等于b的根节点的数据域之值，则查找成功；否则：
- 若x小于b的根节点的数据域之值，则搜索左子树；否则：
- 查找右子树。

**插入**
- 若b是空树，则将s所指结点作为根节点插入，否则：
- 若s->data等于b的根节点的数据域之值，则返回，否则：
- 若s->data小于b的根节点的数据域之值，则把s所指节点插入到左子树中，否则：
- 把s所指节点插入到右子树中。（新插入节点总是叶子节点）

**删除**
- 若*p结点为叶子结点，即PL（左子树）和PR（右子树）均为空树。由于删去叶子结点不破坏整棵树的结构，则只需修改其双亲结点的指针即可。
- 若*p结点只有左子树PL或右子树PR，此时只要令PL或PR直接成为其双亲结点*f的左子树（当*p是左子树）或右子树（当*p是右子树）即可，作此修改也不破坏二叉查找树的特性。
- 若*p结点的左子树和右子树均不空。在删去*p之后，为保持其它元素之间的相对位置不变，可按中序遍历保持有序进行调整，可以有两种做法：其一是令*p的左子树为*f的左/右（依*p是*f的左子树还是右子树而定）子树，*s为*p左子树的最右下的结点，而*p的右子树为*s的右子树；其二是令*p的直接前驱（in-order predecessor）或直接后继（in-order successor）替代*p，然后再从二叉查找树中删去它的直接前驱（或直接后继）。

#### 图的存储 - 出边表，入边表，邻接矩阵

- 出边表，每个节点的所有出边用链表表示，表头即本节点，所有节点的出边链表构成一个数组。
- 入边表，每个节点的所有入边用链表表示，表头即本节点，所有节点的入边链表构成一个数组。
- 邻接矩阵，节点到节点的距离构成一个矩阵，即二维数组，当边不存在时对应的值为无穷大。

#### 图的遍历 - BFS，DFS

- BFS 即广度遍历，先访问自己，然后访问所有的子节点，每访问一个子节点将其加入队列，遍历完子节点就出队一个节点，接着遍历其子节点并入队，直到所有能到达的节点都访问完毕且队列为空。
- DFS 即深度遍历，先访问自己，然后深度优先遍历任意一个未访问过的子节点（递归），直到所有能到达的节点都被访问。

#### 最小生成树 - Prime，Kruskal

- Prime，典型贪心算法
``` c
Prime
1. 在 G 中任取一个顶点加入生成树 V ，并在 G 中删除。
2. 选取一条连接 V 和 G 的权最小的边，将它和另一个端点加进 V 。
3. 重复步骤 2，直到所有的顶点都进入 V 为止。
```
- Kruskal，也是一种贪心算法
``` c
Kruskal
1. G 去掉所有的边，构成有 n 棵树的森林，同时边的集合为 E。
2. 在 E 中找到一条权值最小且连接不同的树的边 e，将连接的两棵树变成一棵树，同时在 E 中删除 e。
3. 重复 2，直到森林只有一棵树。
```

#### 最短路径

- Dijkstra
``` c
1. 设定集合 S，S 仅含起点 o 。
2. 起点为 o ，选取其出边权值最小的边及对应的点 i，添加到 S 中。对于添加进 S 的 i，遍历起每一条出边，如果 A[o][i] + A[i][j] < A[o][j] ，更新 A[o][j] ，重复本次动作，直到能到达的点都遍历完为止。
```

- Floyd
``` c
//对于每一对顶点 i j ，考虑一个中间点 k ，看从 i 经过 k 到 j 是否比不经过近，如果近则更新边值。
for(k=0;k<n;k++) { 
  　　for(i=0;i<n;i++)
     　　for(j=0;j<n;j++)
         　　if(A[i][j]>(A[i][k]+A[k][j])) {
                 A[i][j]=A[i][k]+A[k][j];
                 path[i][j]=k;
             } 
} 
```
#### 二分查找

对于有序列表，给定查找数值，先查找列表中间位置，如果中间数值根据中间位置数值大小进行递归。
```
int binSearch(int array[], int low, int high, int key) {  
    if (low<=high) {  
        int mid = (low + high) / 2;  
        if(key == array[mid])  
            return mid;  
        else if(key < array[mid])  
            return binSearch(array, low, mid-1,key);  
        else if(key > array[mid])  
            return binSearch(array, mid+1, high,key);  
    }  
    else  
        return -1;  
}  
```
[参考链接](http://blog.csdn.net/q3498233/article/details/4419285)

#### 不需要中间数据交换两个数

``` c
void swap(int &a, int &b) {  
    if (a != b) {  
        a ^= b;  
        b ^= a;  
        a ^= b;  
    }  
}  
```
#### 直接插入排序

每次将 **第一个** 待排序的数据，插入到前面已经排好序的序列之中，直到全部数据插入完成。
[参考链接](http://blog.csdn.net/morewindows/article/details/6665714)

#### 直接选择排序

每次将 **最小的一个** 待排序的数据，插入到前面已经排好序的序列的 **最后**，直到全部数据插入完成。
[参考链接](http://blog.csdn.net/morewindows/article/details/6671824)

#### 希尔排序

分裂原序列进行 **直接插入排序**，在逐渐合并子序列，直到合并成一个序列为止。
[参考链接](http://blog.csdn.net/morewindows/article/details/6668714)

#### 二叉堆

- 特性：父结点的键值总是大于或等于（小于或等于）任何一个子节点的键值，称为最大堆（最小堆）。
- 存储：一般都用数组来表示堆，i 结点的父结点下标就为 (i – 1) / 2。它的左右子结点下标分别为2 * i + 1和2 * i + 2。如第0个结点左右子结点下标分别为 1 和 2 。
- 插入：将新数据放在数组最后，然后对二叉堆进行调整。
- 删除：删除第一个节点，然后把最后一个节点赋值给第一个节点，调整。
[参考链接](http://blog.csdn.net/morewindows/article/details/6709644)

#### 堆排序

将首节点与末节点交换，然后调整此时的首节点到倒数第二个节点为新的二叉堆，再将首节点与倒数第二节点交换。如此往复，直到堆仅为首节点为止。
**最大堆获得升序，最小堆获得降序**
[参考链接](http://blog.csdn.net/morewindows/article/details/6709644)

#### 快速排序

选一个基准数 x，在序列中比它小的放在它前面，比它大的放在它后面，形成 A x B （A ， B 为集合）这样的分布，再对 A B 进行同样的操作，直到 A B 只包含一个元素为止。
``` python
def qsort(nums_list):
    def qsort_exec(nums, left, right):
        l = right - left + 1
        if l < 2:
            return
        if l == 2:
            if nums[left] > nums[right]:
                nums[left], nums[right] = nums[right], nums[left]
            return
        start, end = left, right
        stand = nums[start]
        while start < end:
            while nums[end] > stand and start < end:
                end -= 1
            if start < end:
                nums[start] = nums[end]
                start += 1
            while nums[start] < stand and start < end:
                start += 1
            if start < end:
                nums[end] = nums[start]
                end -= 1
        nums[start] = stand
        qsort_exec(nums, left, start - 1)
        qsort_exec(nums, start + 1, right)
    qsort_exec(nums_list, 0, len(nums_list) - 1)
    return nums_list
```
[参考链接](http://blog.csdn.net/morewindows/article/details/6684558)

#### 归并排序

递归分解数列直至只含一个元素，然后对分解的数列进行有序合并。
[参考链接](http://blog.csdn.net/morewindows/article/details/6678165)

### 参考代码

只知道原理是不行的，很多算法需要自己写出来才有感觉，对于以上的数据结构和算法，这里 **[Structure](https://github.com/XhinLiang/Structure)** 提供一部分参考代码，项目更新中，有兴趣的同学可以跟我一起完善它。
