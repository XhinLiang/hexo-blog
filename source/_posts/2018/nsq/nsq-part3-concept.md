title: 理解 Nsq （三）基础概念
date: 2018-11-4 23:59:59
tags: [nsq,消息队列,messageQueue,go,golang]
categories: 后端
toc: true
---

上一节中，我们成功编译了 nsq 和对应的基础组件，并使用配套的 cli 工具完成了简单的生产者消费者模型。
那么在这一节中，我们就来详细地了解下 nsq 的一些基础概念吧。

本节我们主要来了解 nsq 的一些基础概念。

## Features

nsq 主要有以下功能：

- 支持分布式的拓扑结构，避免单点
- 支持无缝水平扩展（没有 broker 的概念）
- 低延迟（这个主要看benchmark）
- 负载均衡与消息多播模型结合
- 同时擅长高吞吐量的流式消息和低吞吐量的任务管理消息
- 主要在内存中操作
- 开箱可用的服务发现系统：`nsqlookupd`
- 支持 TLS（没啥吸引力）
- 协议无关（这点貌似不算啥特性了，大家都支持）
- 依赖少，部署简单（这点大家有目共睹）
- 可以用简单的 TCP 协议来交互（这意味着客户端的编写会很简单）
- 内建 HTTP 接口，可以进行大部分的管理操作（Topic增删，获取统计信息等）
- 无缝支持[statsd](https://github.com/etsy/statsd/)（这特么也是一种特点吗？？？）
- 内建 `nsqadmin`，支持集群管理功能。（对于小团队来说比较有用，大团队就呵呵了，没有权限管理的东西也敢用？？）


nsq 有以下特点：

- 默认不持久化。也没有默认的 replica 支持
- 消息有可能重发。如果需要去重，请在 Client 端做
- 消息不保证有序（好像没遇到过依靠消息队列做排序的需求）
- lookupd 保证最终一致性。

## Concept

### Message

Message（消息）是消息队列里的实体，一条消息通常是一个独立的信息。
例如：客户端的一个评论动作，可以抽象成一个消息实体。
这个评论的动作包含以下信息：
1. 发起评论的用户id
2. 评论的新闻id
3. 评论发生的时间
4. 评论的内容
...

### Topic

Topic 就是 nsq 的抽象的消息类型。
根据不同的消息类型，我们把这些消息按 Topic 区分开。
例如：评论，点赞，登录，发文章，这些消息应该按 Topic 区分开，因为他们属于不同的消息类型，他们含有的信息字段也不太一样。

### Channel

Channel 是消费者的负载均衡，对于同一个 Topic 的消息，可以定义多个 Channel，那么同一条消息会分别分发到这些 Channel 中，每个 Channel 收到同样的全量消息。

### Producer

Producer 是消息的生产者，他们会负责将消息 publish 到 nsqd 节点中。Producer 可以是任何的程序，只要能正常连接到 nsqd 的节点即可。
例如，用户的评论动作发生在 HTTP 服务器中，那么这个接收 HTTP 请求的 HTTP 服务器就可以作为 Producer 向 nsqd 节点发送评论消息（publish message to nsqd node）。

### Consumer

Comsumer 是消息的消费者，他们对指定 Topic 的消息感兴趣，并在自己定义的 Channel 中订阅这个 Topic 的消息，他们在这个 Channel 中能收到这个 Topic 的全量消息，如下图所示：
![nsq-channels](/uploads/2018/nsq/nsq-channels.png)


## Architecture

Nsq 的整体架构图也比较简单，如下图所示：

![nsq-architecture](/uploads/2018/nsq/nsq-architecture.png)

可以看到，nsq 中是不存在单点的，具体理由如下：

### nsqd 不交互

nsqd 之间是不进行交互的，各自进行自己的「生产/消费」（「接收消息/发送消息」）操作，由客户端自己来做负载均衡（这里存疑，如果有误请指出）。

举个例子，假设有个两个 nsqd 节点，分别是 nsqd-a，nsqd-b，一个 topic：topic-a。
两个 Producer 和两个 Consumer：producer-a producer-b consumer-a consumer-b。
那么这个时候理想的结果是：
1. producer-a 只连上 nsqd-a 这个节点，而 producer-b 只连上 nsqd-b 这个节点，他们各自往各自连上的节点发送消息。
2. consumer-a 和 consumer-b 分别都连上 nsqd-a nsqd-b 两个节点，他们共享同一个 channel：channel-test。
那么，对于 topic-a 这个消息来说，consumer-a 和 consumer-b 消费的消息的集合分别为 messages-a messages-b

messages-a 和 messages-b 的并集为 producer-a 和 producer-b 发送的所有的消息。
messages-a 和 messages-b 的交集为空集（这里不考虑消息重复发的情况）。

### nsqlookup 不交互，不单点

可以同时存在多个 nsqlookup 节点。nsqd 节点在他们上注册，同一个 nsqd 节点可以同时在不同的 nsqlookup 上注册。

这里可以思考下多机房的配置方案：
1. 每个机房配置多个 nsqlookup，并配置一个（或者几个）nsqlookup节点，用于容灾。
2. 机房内的所有 nsqd 节点全部都在机房内的所有 nsqlookup 节点上注册，并全都在全局 nsqlookup 节点上注册。
3. 每个机房的生产者和消费者平时只需要连接本机房内的多个 nsqlookup 节点，遇到特殊情况可以连接全局的 nsqlookup 节点。

## PostView

通过上面的学习，我们可以发现 nsq 整体的设计相当简单，理解起来没有任何难度。
因为设计简单，nsq 有很多不能保证的东西（重复性不保证，有序性也不保证）不知道他在具体的生产环境中有没有什么天坑。