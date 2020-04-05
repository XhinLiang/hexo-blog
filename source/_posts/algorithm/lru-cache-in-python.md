title: 双向链表和哈希表实现 LRUCache
date: 2017-12-29 00:36:29
tags: [Python,算法,数据结构]
categories: 算法
toc: true
---

### 背景

LRUCache 是一个很常用的缓存实现，本文会首先介绍一下 LRUCache 的定义，然后尝试用 Python 实现它。

#### 定义

LRUCache 首先是一个 Cache，那么对于一个 Cache 而言，肯定需要提供 `get` 和 `set` 两个方法，而且，这两个方法的时间复杂度越低越好，最好达到 O(1) 级别。

LRU 是 Least Recently Used 的缩写，近期最少使用策略。
LRUCache 意味着一个带有容量的缓存，当缓存的容量已满而且需要插入新值的时候，缓存需要淘汰一个旧值。具体淘汰的策略就是 LRU。

LRU 意味着这样的功能：
```python
# 如果 Cache 里有两个 key => `a` 和 `b`，而且 Cache 的容量是 2
cache.get('a')
# ... 无数次
cache.get('a')
cache.get('b')
cache.put('c', 'c-value')
# cache => {'b': 'b-value', 'c': 'c-value'}
```

我们可以看到，无论 `a` 之前 `get`，过多少次，只要最后一个 `get('b')` 的操作在最后一个 `get('a')` 的操作之后，那么 淘汰 `b` 的优先级肯定在 `a` 之后，这就是 LRU 策略的实例化解释。


#### 实现

通常使用双向链表和字典来实现 LRUCache。

为了能很快找到双向链表的头和尾，我们需要一个虚拟头节点，这个头节点的 `next` 指针始终指向真实的头节点（以下称为头节点）；类似地，我们也需要一个虚拟尾节点，它的 pre 指针始终指向真实的尾节点（以下称为尾节点）。

双向链表的头节点就是淘汰优先级最低的点，尾节点就是淘汰优先级最高的点。
当 LRUCache 容量达到上限后，应该首先淘汰尾节点。

链表节点的 val 字段指向一个数组 [key, value]。这个 key 和 value 就是整个 LRUCache 中 `get` 和 `set` 方法的 key 和 value。

map 的 key 也是 LRUCache 的 key，但是 map 的 value 是双向链表的节点。

那么对应 LRUCache 的两个方法 `get` `put`，我们可以想出以下思路：

##### get(key)

`get` 方法需要考虑两件事情：
1. 找到 key 对应的 value 值
2. 更新 key 的淘汰优先级

具体思路如下：
- 如果这个 key 在 map 中不存在，那么我们只需返回 null 即可
- 如果这个 key 在 map 中存在，那么我们此时能马上获取到这个 key 对应的链表节点，通过链表节点我们能读取到真正的缓存的值。此时我们需要先将这个链表节点挪动到链表的头部，然后再返回链表的 value 字段

##### put(key, value)

`put` 方法需要考虑三个事情：
1. 更新 key 对应的 value
2. 更新 key 对应的淘汰优先级
3. 如果当前缓存容量达到上限，淘汰一个链表节点。

具体思路如下：
- 如果这个 key 原本就存在需要通过 map 找到链表节点，然后更新链表节点中的 value，然后将这个链表节点挪动到链表的头部
- 如果这个 key 存在，那么我们需要构造一个 node，并插入到链表头部
  - 如果容量未满，不用管
  - 如果容量满了，那么我们需要移除链表尾部的 node，并将其从 map 中也移除

``` python
# -*- coding: utf-8 -*-

import sys


class ListNode(object):
    """
    LinkedListNode
    """
    __slots__ = ['val', 'next', 'pre']

    def __init__(self, x):
        self.val = x
        self.next = None
        self.pre = None


class LinkedList(object):
    """
    LinkedList
    """
    __slots__ = ['head', 'tail', 'length']

    def __init__(self):
        """
        init
        """
        self.head, self.tail = ListNode(-1), ListNode(-1)
        self.head.next = self.tail
        self.tail.pre = self.head
        self.length = 0

    def insert_head(self, node):
        """
        insert a value to head
        :param node: the value
        :return: ListNode the node has been inserted
        """
        node.next = self.head.next
        self.head.next.pre = node
        node.pre = self.head
        self.head.next = node
        self.length += 1
        return node

    def insert_tail(self, node):
        """
        insert a node to tail
        :param node: the value
        :return: ListNode the node has been inserted
        """
        node.pre = self.tail.pre
        node.next = self.tail
        self.tail.pre = node
        self.length += 1
        return node

    def pop_head(self):
        """
        pop a node from head
        :return: ListNode the node has been popped
        """
        if self.length == 0:
            return None
        tempNode = self.head.next.next
        tempNode.pre = self.head
        self.head.next = tempNode
        self.length -= 1
        return tempNode

    def remove_node(self, node):
        """
        remove a node from linkedlist
        :param node: ListNode
        :return: ListNode the node has been removed
        """
        node.next.pre = node.pre
        node.pre.next = node.next
        self.length -= 1

    def pop_tail(self):
        """
        pop a node from tail
        :return: ListNode the node has been popped
        """
        if self.length == 0:
            return None
        shouldRemoveNode = self.tail.pre
        tempNode = shouldRemoveNode.pre
        tempNode.next = self.tail
        self.tail.pre = tempNode
        self.length -= 1
        return shouldRemoveNode

    def print_self(self):
        if self.length == 0:
            print('none')
            return
        current_node = self.head.next
        while current_node.next is not None:
            sys.stdout.write(str(current_node.val[0]) + ":" + str(current_node.val[1]) + " => ")
            current_node = current_node.next
            if current_node.next is None:
                break
        sys.stdout.write(" None ")
        sys.stdout.write(" :: Length: " + str(self.length))
        sys.stdout.flush()
        print('')


class LRUCache(object):
    """
    LRUCache
    """
    __slots__ = ['map', 'linkedlist', 'cap']

    def __init__(self, cap):
        self.cap = cap
        self.map = {}
        self.linkedlist = LinkedList()

    def put(self, key, value):
        # if this key is exist, just update the value of the node and move this node to head
        if key in self.map:
            node = self.map[key]
            node.val[1] = value
            self.get(key)
            self.linkedlist.print_self()
            return

        # not exist yet, insert this value to head and put this node to map
        newNode = self.linkedlist.insert_head(ListNode([key, value]))
        self.map[key] = newNode

        # check the capacity, remove the tail node if LRUCache is full
        if self.linkedlist.length > self.cap:
            oldNode = self.linkedlist.pop_tail()
            oldKey = oldNode.val[0]
            self.map.pop(oldKey)

        self.linkedlist.print_self()

    def get(self, key):
        if key not in self.map:
            self.linkedlist.print_self()
            return -1

        # get the node, move this node to head
        node = self.map[key]
        self.linkedlist.remove_node(node)
        self.linkedlist.insert_head(node)
        # return the value
        self.linkedlist.print_self()
        return node.val[1]


cmds = ["put", "put", "put", "put", "put", "get", "put", "get", "get", "put", "get", "put", "put", "put", "get",
        "put", "get", "get", "get", "get", "put", "put", "get", "get", "get", "put", "put", "get", "put", "get", "put",
        "get",
        "get", "get", "put", "put", "put", "get", "put", "get", "get", "put", "put", "get", "put", "put", "put", "put",
        "get",
        "put", "put", "get", "put", "put", "get", "put", "put", "put", "put", "put", "get", "put", "put", "get", "put",
        "get",
        "get", "get", "put", "get", "get", "put", "put", "put", "put", "get", "put", "put", "put", "put", "get", "get",
        "get",
        "put", "put", "put", "get", "put", "put", "put", "get", "put", "put", "put", "get", "get", "get", "put", "put",
        "put",
        "put", "get", "put", "put", "put", "put", "put", "put", "put"]

params = [[10, 13], [3, 17], [6, 11], [10, 5], [9, 10], [13], [2, 19], [2], [3], [5, 25], [8], [9, 22], [5, 5], [1, 30],
          [11], [9, 12], [7], [5], [8], [9], [4, 30], [9, 3], [9], [10], [10], [6, 14], [3, 1], [3], [10, 11], [8],
          [2, 14], [1],
          [5], [4], [11, 4], [12, 24], [5, 18], [13], [7, 23], [8], [12], [3, 27], [2, 12], [5], [2, 9], [13, 4],
          [8, 18],
          [1, 7], [6], [9, 29], [8, 21], [5], [6, 30], [1, 12], [10], [4, 15], [7, 22], [11, 26], [8, 17], [9, 29], [5],
          [3, 4],
          [11, 30], [12], [4, 29], [3], [9], [6], [3, 4], [1], [10], [3, 29], [10, 28], [1, 20], [11, 13], [3], [3, 12],
          [3, 8],
          [10, 9], [3, 26], [8], [7], [5], [13, 17], [2, 27], [11, 15], [12], [9, 19], [2, 15], [3, 16], [1], [12, 17],
          [9, 1],
          [6, 19], [4], [5], [5], [8, 1], [11, 7], [5, 2], [9, 28], [1], [2, 2], [7, 4], [4, 22], [7, 24], [9, 26],
          [13, 28],
          [11, 26]]




def print_list(l):
    sys.stdout.write('[')
    sys.stdout.write(', '.join(str(p) for p in l))
    sys.stdout.write(']')

cache = LRUCache(10)

for i in xrange(len(cmds)):
    cmd = cmds[i]
    param = params[i]

    sys.stdout.write(str(i) + " " + cmd + " ")
    print_list(param)
    sys.stdout.write("\n")
    val = getattr(cache, cmd)(*param)
    print("result " + str(val))
```