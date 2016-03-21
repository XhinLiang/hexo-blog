title: 在Ubuntu下录制屏幕GIF
date: 2016-03-9 17:28:29
tags: [工具,Linux]
categories: Android
toc: true
---

> Ubuntu 是一个十分完善的 Linux 发行版，目前也是我的主要生产力工具栖息的地方，不像 Windows 或者 OS X，Ubuntu 现在没有一种非常完备的屏幕 GIF 录制工具，今天稍微折腾了一小会，总结一套比较方便完美的解决方案

### 安装 byzanz 
在我的 Ubuntu 14.04 LTS 当中，byzanz 不需要添加源
``` bash
sudo apt-get install byzanz
```
如果有同学的版本没有发现这个软件包的话，需要手动添加源
``` bash
sudo add-apt-repository ppa:fossfreedom/byzanz
sudo apt-get update
sudo apt-get install byzanz
```
### byzanz 使用说明
**byzanz** 的图形界面智能在 **gnome** 环境下使用，而我现在使用的是默认的 **Unity** 桌面，所以不能使用 **byzanz** 的图形界面，只能通过命令行来使用。
``` bash
byzanz-record --cursor --x=0 --y=52 --width=312 --height=521 /home/xhinliang/picture/sample.gif
```
参数稍微有点多，大家可以根据这行命令来查看
``` bash
byzanz-record --help
```
其中我们通过 **width** **height** 来限定了屏幕录制的宽高；**x** **y** 来定义了屏幕开始录制的顶点，也就是录制屏幕的矩形的左上角在屏幕中的位置。

### 屏幕坐标的获取
**byzanz** 的使用其实挺简单的，但获取要截取的矩形在屏幕的坐标和宽高有点棘手。

这里我给大家推荐一个工具 **xdotool**，通过它我们可以很方便地获取到鼠标光标的坐标，从而轻易计算出我们需要的坐标和宽高。

首先来安装它
``` bash
sudo apt-get install xdotool
```
安装完成后，将鼠标光标移动到屏幕任意位置，	然后在 **Terminal** 中输入命令
``` bash
xdotool getmouselocation
```

获得了坐标，**byzanz** 的使用我也不赘述了。

