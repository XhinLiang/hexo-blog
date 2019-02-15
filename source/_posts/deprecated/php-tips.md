title: PHP Tips
date: 2016-6-9 15:16:29
tags: [Linux, PHP]
categories: 工具
toc: true
---
### 在 web 页面呈现错误

公司在用 PHP 5.3 + Nginx，我这边用 PHP 7 跑得好好的程序，在服务器上就一直报 500 。查 Nginx 日志又查不到信息（服务器的配置有点混乱）。

无奈之下，只好一行一行地测试。最后把自己挖的坑给填上了。

其实有个更加简单的办法，就是在 PHP 文件的开头加上几行代码。

```
# 设置报告所有错误
error_reporting(E_ALL);
# 设置在命令行或者web界面输出错误
ini_set('display_errors', 1);

# 输出的文件
ini_set('error_log', 'path/to/file');
```
### `array_merge()` 的陷阱

`array_merge()` 函数中，如果参数中前后两个不同的数组含有相同的键，那么后面的数组的值将会覆盖掉前面的数组的值。

还有更重要的一点，**上面的条件仅仅在都是字符串键的时候成立！！**

