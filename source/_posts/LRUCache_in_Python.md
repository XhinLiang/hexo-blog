title: 双向链表和哈希表实现 LRUCache
date: 2017-12-29 00:36:29
tags: [Python,算法,数据结构]
categories: 算法
toc: true
---

> LRUCache 是一个很常用的缓存实现，我们简单用 Python 实现它

#### 定义
LRU 是 Least Recently Used 的缩写，近期最少使用算法。
LRUCache 意味着一个带有容量的缓存，当缓存的容量已满而且需要插入新值的时候，缓存需要淘汰一个旧值。
如何去淘汰呢，这个时候就需要用到 LRU 算法。

LRU 意味着这样的功能
``` python
# 如果 Cache 里有两个 key => `a` 和 `b`，而且 Cache 的容量是 2
cache.get('a')
# ... 无数次
cache.get('a')
cache.get('b')
cache.put('c', 'c-value')
# cache => {'b': 'b-value', 'c': 'c-value'}
```

我们可以看到，无论 `a` 之前 `get`，过多少次，只要最后一个 `get('b')` 的操作在最后一个 `get('a')` 的操作之后，那么 淘汰 `b` 的优先级肯定在 `a` 之后。

#### 实现
为了保证 LRUCache 的读写复杂度都是 O(1)，我们不能简单地只用一个 map 来实现。
简单来说，我们可以使用双向链表和字典来实现它。

为了能很快找到双向链表的头和尾，我们需要一个虚拟头节点，这个头节点的 next 指针始终指向真实的头节点（以下称为头节点）；类似地，也有一个虚拟尾节点，它的 pre 指针始终指向真实的尾节点（以下称为尾节点）。

双向链表的头节点就是淘汰优先级最低的点，尾节点就是淘汰优先级最低的点。

双向链表的 val 字段指向一个数组 [key, value]，这样，我们找到这个链表节点，就能很快找到它在 map 中的位置。

map 的 key 还是原来的 key，但是 value 是对应的双向链表的节点。

那么对应 LRUCache 的两个方法 `get` `put`，我们可以想出以下思路：

##### get(key)
get 不影响目前的长度。
如果这个 key 存在，那么只需要把对应这个 key 的节点移动到链表的头部即可

##### put(key, value)
- 如果这个 key 原本就存在，那么我们只需要更新 node 对应的 value 即可。

- 如果这个 key 存在，那么我们需要构造一个 node，并插入到链表头
  - 如果容量未满，不用管
  - 如果容量满了，那么我们需要移除链表尾部的 node，并将其从 map 中也移除


``` python
# -*- coding: utf-8 -*-

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

    def insert_head(self, val):
        """
        insert a value to head
        :param val: the value
        :return: ListNode the node has been inserted
        """
        newNode = ListNode(val)
        newNode.next = self.head.next
        newNode.pre = self.head
        self.head.next = newNode
        self.length += 1
        return newNode

    def insert_tail(self, val):
        """
        insert a value to tail
        :param val: the value
        :return: ListNode the node has been inserted
        """
        newNode = ListNode(val)
        newNode.pre = self.tail.pre
        newNode.next = self.tail
        self.tail.pre = newNode
        self.length += 1
        return newNode

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

    @staticmethod
    def remove_node(node):
        """
        remove a node from linkedlist
        :param node: ListNode
        :return: ListNode the node has been removed
        """
        if node is None:
            return
        node.next.pre = node.pre
        node.pre.next = node.next

    def pop_tail(self):
        """
        pop a node from tail
        :return: ListNode the node has been popped
        """
        if self.length == 0:
            return None
        tempNode = self.tail.pre.pre
        tempNode.next = self.tail
        self.tail.pre = tempNode
        self.length -= 1
        return tempNode


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
            return

        # not exist yet, insert this value to head and put this node to map
        newNode = self.linkedlist.insert_head([key, value])
        self.map[key] = newNode

        # check the capacity, remove the tail node if LRUCache is full
        if self.linkedlist.length + 1 >= self.cap:
            oldNode = self.linkedlist.pop_tail()
            self.map.pop(oldNode.val[0])

    def get(self, key):
        if key not in self.map:
            return None

        # get the node, move this node to head
        node = self.map[key]
        LinkedList.remove_node(node)
        self.linkedlist.insert_head(node)
        # return the value
        return node.val[1]
```