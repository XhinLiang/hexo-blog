title: 那些年，我们一起该过的配置文件 -- 常见配置文件类型简介
date: 2018-11-25
tags: [后端,xml,yaml,json,json5,toml,ini,properties]
categories: 后端
toc: true
---
# Overview

在程序员日常开发中，配置文件是一个非常常见的需求。

配置文件可以定制程序的逻辑，一段代码生成的程序可以灵活地适应多个需求。
几乎所有的程序都需要或者隐形需要配置文件，因为它们需要根据配置文件来决定在代码中使用怎样的逻辑来运行。

对于大部分的程序来说，他们需要的配置文件常常是一个 K-V 类型的结构，可以理解为一个 Key 为字符串， Value 也为字符串的一个 Map。字符串可以被转化成大部分通用的数据结构，只需要程序自己做好解析就可以了。

但随着程序的复杂度的增加，配置文件用纯字符串 K-V 来表示的局限性就越来越明显。
例如，我们如果需要一个 List，我们可以自定义分隔符。但如果一个 List 里我需要嵌套，那么用纯字符串 K-V 来表示就非常吃力了。

计算机编程的本质是抽象。因为配置文件是可以被抽象出来的，所以，各个程序员根据自己对配置文件的理解，定义了不同的对配置文件的抽象，这就是我们今天看到的五花八门的配置文件类型。

今天我就来侃侃常见的几种配置文件类型。

# Body

## JSON

毫无疑问，JSON 是目前使用最广泛的一个数据交换格式。大量的 Web 前后端交互使用 JSON 作为数据载体，同时也触发了 JSON 在数据传输之外的用途 -- 配置文件。

我们用一个 empty 的 npm project 的配置文件作为例子：
``` json
{
  "name": "dev_2018_11",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC"
}
```
JSON 是 JavaScript 的亲儿子，所以在 JavaScript 相关的世界中被广泛用作配置文件。
例如：
- npm 依赖描述文件是 JSON
- PHP composer 的依赖描述文件是 JSON
- 大量的 npm 第三方包的配置文件是 JSON

优点：
- 抽象程度高。JSON 能表示大部分的数据结构，对于嵌套的 List，Map 等需求，也能支持得非常好
- 通用性好。绝大部分的编程语言都内置了 JSON 解析器，所以 JSON 的通用性也非常好
- 合法性校验方便，有现成的 JSON-Schema 校验工具

缺点：
- 可读性较差。
  - JSON 不支持注释，一些复杂配置的可读性非常差
  - 灵活性欠佳
  - 不支持嵌套配置文件（不能在一个配置文件中 import 另外一个配置文件）
  - JSON 严格的格式校验（Array 的最后一个元素后面不能加逗号），导致修改起来不够方便
  - Key 必须被双引号包裹，编写起来也不太方便

## JSON5

JSON 的缺点非常致命，优点又非常明显，所以一些程序员希望在 JSON 的基础上新定义一个数据类型，对 JSON 扬长补短，这就是我们看到的 JSON5 结构。

举个官方的例子：
```
{
    name: 'ManerFan',
    // address
    addr: 'KunMing Road,\
        ShannXi,\
        China',
    nickname: '\u5c0f\u5e08\u59b9'
}
```

JSON5 完全兼容 JSON，而且对 JSON 做了一些扩展：
- 支持注释
- 属性key可以不使用引号包含，而且可以使用单引号包含
- 可以在尾部有多余逗号
- 支持多行字符串
- etc..

JSON5 解决了 JSON 大部分的问题，但是依然不支持嵌套的配置文件。

## XML

XML 在 `Java` 和 `Spring` 中使用非常广泛，他能描述大部分的数据结构，但是缺点是太罗嗦了，罗嗦到我现在都不想贴示例出来。

好吧，还是随便贴一个：
``` xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>com.xhinliang</groupId>
    <artifactId>xcall</artifactId>
    <version>1.0.1</version>
    <packaging>jar</packaging>
    <name>${project.artifactId}</name>
    ...
```

我只想说，XML 的「罗嗦」这个缺点，成功地掩盖了它的其它缺点，因为已经罗嗦到不能忍了...

## INI

INI 配置文件在一些 Windows 程序中用得比较多，它事实上是一种非常朴素的字符串 K-V 的配置文件。

``` ini
[section1]  
; this is comment
key=value
key2=value2

[section2]
```

ini 配置文件现在用得不多了，优点也不多说了，几乎没有。
缺点也不多说，关键是注释长得很丑。

## Properties

Properties 跟 INI 类似，事实上是一个简单的字符串 K-V。

``` properties

# comment
db=xxxxxx
```
特点也跟 INI 差不多吧，抽象描述能力有限。

## PHP

没错，PHP 也是一种配置文件格式，在 80% 的网站 PHP 覆盖率面前颤抖吧！
PHP 的数组（array）即能表示普通的数组，也能表示Map，甚至能同时包含（这个特性能逼疯很多人...）

在 PHP 程序中， `config.php` 文件非常常见，事实上，大部分的 PHP 框架都使用 PHP 文件作为他们的配置文件。
举个 Yii 框架的配置文件作为例子：
``` php
<?php

$config= [
    'components' => [
        'db' => [
            'class' => 'yii\db\Connection',
        ],
        'mailer' => [
            'class' => 'yii\swiftmailer\Mailer',
            'viewPath' => '@common/mail',
            // send all mails to a file by default. 
            'useFileTransport' => true,
        ],
    ],
];
if (YII_ENV_DEV) {
    // configuration adjustments for 'dev' environment
    $config['bootstrap'][] = 'debug';
}


```

PHP 文件作为配置文件，有以下优点：
- 灵活性非常好，能更灵活地定制程序的逻辑，因为你能在 PHP 文件里干任何事情，在一个配置文件中 require 另外一个配置文件，是一个非常常见，非常 easy 的事情
- 抽象性非常棒，几乎没有用 PHP 配置文件描述不出来的数据结构

但缺点也很明显：
- 跨语言通用性几乎为 0
- 太过灵活导致安全性欠佳（你见过 import 之后会删除本地文件的配置文件吗...）

## YAML

YAML 不是一种标记语言。他是一种数据描述语言（DDL）。有一些程序支持使用 YAML 作为配置文件，例如 `Spring Boot` 和 `Hexo`，`Ruby on Rails`。

典型的 YAML 配置格式如下：
``` yaml
house:
  family:
    name: Doe
    parents:
      - John
      - Jane
    children:
      - Paul
      - Mark
      - Simone
  address:
    number: 34
    street: Main Street
    city: Nowheretown
    zipcode: 12345
```

可以看到 YAML 的可读性和易修改性都非常好，目前大部分语言都直接支持了。

## Toml

TOML 是前 GitHub CEO 于2013年创建的语言，其目标是成为一个小规模的易于使用的语义化配置文件格式。

``` toml
# 这是一个TOML文件

title = "TOML Example"

[owner]
name = "Lance Uppercut"
dob = 1979-05-27T07:32:00-08:00 # 日期是一等公民

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]
  # 可以使用空格、制表符进行缩进，或者根本不缩进。TOML不关心缩进。
  [servers.alpha]
  ip = "10.0.0.1"
  dc = "eqdc10"
```
乍看和 INI 差不多，但事实上扩展性比 INI 强多了，基本上能完整描述大部分的数据结构了。

## 自定义 Conf 配置文件

有一些程序会自己定义配置文件格式，例如 `Redis` `Nginx` `Supervisor`。
举个 Nginx 的配置文件作为例子：

``` conf
user  www www;
worker_processes  2;
error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
pid        logs/nginx.pid;
events {
    use epoll;
    worker_connections  2048;
}
```

自定义配置文件一般来说基本不需要跨语言访问了（甚至同语言也不需要访问，只需要他自己一个程序访问就够了）
Nginx 自定义的配置文件可读性应该比用 JSON 描述会高很多，但合法性的校验目前没有太多的标准。

# PostView

配置文件的发展和变革，事实上也是编程语言的发展和变革，我们知道，在计算机领域通常「没有银弹」。但事实上有一些更优秀的配置文件格式正在渐渐替代老旧的格式。

但目前来看，并不存在一种配置文件格式能通杀所有的需求。所以，长期来看，还是会出现多种配置文件并存的现象的。
