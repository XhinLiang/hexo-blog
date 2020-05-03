title: 常见数据库简介
date: 2018-11-18
tags: [后端,随笔]
categories: 计算机
toc: true
---

# Overview

![overview](https://cdn.lynda.com/course/548706/548706-637199619492944531-16x9.jpg)

数据库在后端程序员中应该是最常使用到的中间件了，今天我们来侃一侃常见的数据库。

## MySQL 派系

MySQL 无疑是世界上最火热的数据库了。因为太过火热，它也有很多不同的分支，这些分支会有一些不同的特点。

### MySQL

在国内来说，MySQL 是一个最常见的数据库了，也是 MySQL 派系中最主流的分支，目前由 Oracle 公司维护。

特点：
1. 源代码使用 C 和 C++ 编写，性能稳定。
2. 支持多种数据库引擎（MyISAM，InnoDB，Memory，MyRocks etc..）可以满足不同场景下的需要。
3. InnoDB 支持事务，但 MyISAM 不支持。
4. 索引使用 B+ 数实现，大部分操作都是顺序读取，对 HDD 友好。
5. MyISAM 中每个索引都是一级索引，但 InnoDB 中除主键外的索引都是二级索引（二级索引找到主键，主键再找到数据）。
6. 分为社区版（免费）和商业版（收费）两种授权模式。
7. 支持主从配置，主库读写，从库只读。

### MariaDB

MariaDB 是 MySQL 的一个开源分支，其目标是对 MySQL 实现 100% 的兼容。
特点：
1. 她的存储引擎跟 MySQL 的不一致。
2. 她独特的存储引擎叫 Maria，是 InnoDB 的变体，支持事务。除此之外还支持 FederatedX，XtraDB 等别的存储引擎。
3. 跟 MySQL 100% 兼容：
   1. 数据和表定义文件（.frm）是二进制兼容的
   2. 所有客户端 API、协议和结构都是完全一致的
   3. 所有文件名、二进制、路径、端口等都是一致的
4. 整体性能上跟 MySQL 类似。

### TiDB

TiDB 是 PingCAP 公司推出的一种开源分布式关系型数据库。
简介可以看看官网：https://pingcap.com/docs-cn/

特点：
- 基本兼容 MySQL 的协议。（不是 100% 兼容）
- 支持分布式事务。（这个牛逼了）
- 支持在线 DDL。
- 100% 支持标准的 ACID 事务。
- 不同于于 MySQL 主从复制方案，基于 Raft 的多数派选举协议可以提供金融级的 100% 数据强一致性保证，且在不丢失大多数副本的前提下，可以实现故障的自动恢复 (auto-failover)，无需人工介入。（这个牛逼了）
- 对大部分 OLAP 场景也提供支持。（OLAP：联机分析处理）

### AliSQL

AliSQL 是另一个 MySQL 的分支版本，目前由 Alibaba 维护。[GitHub](https://github.com/alibaba/AliSQL)

官方的描述是：「在通用基准测试场景下，AliSQL 版本比 MySQL 官方版本有着 70% 的性能提升；在秒杀场景下，性能提升 100 倍。」

特点：
- 100% 兼容 MySQL。
- 又是另外一个存储引擎。
- 虽然是 Alibaba 在维护，但国内相关的资料极少。
- 开源轰轰烈烈，但源代码已经很久没有更新（估计是在内部有开发，对外开放的版本滞后了）

## PostgreSQL

PostgreSQL 跟 MySQL 类似，也是一个关系型数据库，但他又多了一个特点，它是对象关系数据库管理系统(ORDBMS)。

提起 PostgreSQL，那就不得不拿他跟 MySQL 对比一下，[这里有简单的对比](https://blog.csdn.net/tiandao2009/article/details/79839037)。

特点：
- 更学院派。这个是个哲学问题，不多说。
- 多进程架构。相比之下，MySQL 是多线程的。
- 支持同步，异步，半同步的 replica，是一种物理复制。
- JOIN 性能比 MySQL 有很大优势。

## MongoDB

MongoDB 不是一种关系型数据库。是一种 NoSQL。
特点：
- 天生支持分布式，对扩展友好。
- 不支持事务 ACID，但作为替代，有个新的概念：BASE。	基本可用(Basically Available)，软状态/柔性事务(Soft state)，最终一致性 (Eventual consistency)。
- 在一些场景下可以基本替代 MySQL 使用。

## HBase

HBase 是建立在 HDFS 之上的分布式面向列的数据库。是 Google 的著名论文《BigTable》的开源实现。

[这篇文章讲得不错](https://blog.csdn.net/nosqlnotes/article/details/79647096)。

HBase 是一个面向列的数据库，在表中它由行排序。表模式定义只能列族，也就是键值对。一个表有多个列族以及每一个列族可以有任意数量的列。后续列的值连续地存储在磁盘上。表中的每个单元格值都具有时间戳。

HBase常被用来存放一些结构简单，但数据量非常大的数据。

特点：
- 较大的表中能快速查找。
- 数十亿条记录低延迟访问单个行记录（随机存取）。
- 面向列的数据库。
- 不具有固定列模式的概念，仅定义列族，每个列族可以包含多个列。
- 大宽表，列值是稀疏的，而且是半结构化的数据。
- 不支持任何事务。
- 索引能力有限。
- 自动故障支持。

## InfluxDB

InfluxDB 是一个开源的时序数据库，使用 Golang开发，特别适合用于处理和分析资源监控数据这种时序相关数据。

InfluxDB 自带的各种特殊函数如求标准差，随机取样数据，统计数据变化比等，使数据统计和实时分析变得十分方便。

特点：
- 数据可以被标记，允许非常灵活的查询。
- 支持一部分 SQL 语句。
- 适合 OLAP 或者监控需求。

## OpenTSDB

也是一种时序数据库，但跟 InfluxDB 不同的是，他是依赖 HBase 实现的。

## GpDB -- Greenplum

Greenplum 数据库，也叫 GPDB，是一个分布式数据库，数据仓库快速查询工具。

特点：
- 支持 SQL。
- 支持分布式事务。
- 支持线性扩展。

## ClickHouse

最近兴起的一个 OLAP 数据库，由俄罗斯公司 Yandex 开发，性能强劲。

## LevelDb

LevelDb 是一个 google 实现的非常高效的 KV 数据库，能够支持 billion 级别的数据量。 在这个数量级别下还有着非常高的性能，主要归功于它的良好的设计。特别是 LSM 算法。

## RocksDb

RocksDB 是使用 Facebook 基于 C++ 编写的嵌入式 KV 存储引擎，其键值均允许使用二进制流，提供向后兼容的 LevelDB API。

RocksDB 针对 Flash 存储进行优化，延迟极小。RocksDB使用 LSM 存储引擎，纯C++编写。Java 版本 RocksJava 正在开发中。

我理解 RocksDb 应该是 LevelDb 的另一种实现，从功能上算是超集吧。

## MyRocks

MySQL 兼容的 RocksDb，底层实现基本上跟 RocksDB 一致，但是作为一种存储引擎在 MySQL 中使用。国内有一些公司在使用。