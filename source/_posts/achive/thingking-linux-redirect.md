title: Linux 的重定向
date: 2016-6-14 15:16:29
tags: [Linux]
categories: 工具
toc: true
---

在 Linux 命令行中，重定向是一个非常重要的操作。

这里简单列举一下常见的三种操作。

### 重定向到文件中（覆盖）

```
# 快捷写入一个文件
> echo '<?php phpinfo ?>' > index.php

# 执行命令，将输出重定向到文件
> git log > git.log

# 把命令交给指定的程序执行
> echo '<?php echo 'hello' ?>' > php
```
### 重定向到文件中（向后添加）

```
# 向文件后添加一条记录
> cal >> git.log

# curl 并添加的文件末尾
> curl crawl.xhinliang.com/baidu/rank/beyond >> beyond_rank.log
```

### 重定向到文件的同时，在屏幕输出

这里会稍微麻烦一点，需要用到管道和 `tee` 命令。

如果对管道还不够熟悉，尽情地 Google 吧。

```
# 写入并输出
> curl google.com | tee google.out
```
