title: PHP 在 Vim 上的使用问题
date: 2016-4-14 13:16:29
tags: [Linux, Vim]
categories: 工具
toc: true
---


## 问题
最近在写 PHP 。写这种脚本语言当然是用 Vim 最舒服啦，方便起见我一直用的 Vim 设置[懒人包](https://github.com/spf13/spf13-vim)。

但是很奇怪的是在编辑 .php 文件时，Vim 变得非常慢，同时由于 CPU 负荷过高电脑风扇也不停地转，简直到了无法忍受的地步。

## 尝试 Atom
无奈只好转战 Atom ，为了方便我还安装了 vim-mode 和 ex-mode 插件。

Atom 其实也不习惯，首先是一些快捷键不知道换成了哪些，比如切换页面的快捷键，切换到目录的快捷键，这些对我来说都很重要 。

我甚至还把 vim-mode 的 keymap 翻了一遍，愣是没找到我需要的快捷键，无奈还是转回 Vim 。

## 解决问题
其实问题很好解决，针对 PHP 这一种文件类型做一些调整即可。

首先我们打开文件类型检测功能，在 `.vimrc` 中添加一行：
```
filetype plugin indent on 
```
然后针对 `PHP` 这一类型，做出特别的处理。

在 `.vim` 文件夹中新建一个文件夹 `after`：
```
sudo mkdir ~/.vim/after
```
在 `after` 中新建一个文件夹 `ftplugin` ：
```
sudo mkdir ~/.vim/after/ftplugin
```
在刚刚新建的文件夹新建一个文件 `php.vim` ：
```
sudo vim ~/.vim/after/ftplugin/php.vim
```

在文件中输入以下内容：
```
set nocursorcolumn
set nocursorline
syntax sync minlines=128
syntax sync maxlines=256
set synmaxcol=800
```
这几项设置我就不多解释了，有兴趣的可以自行搜索。

## 扩展
我们这里可以看到，在 Vim 中，针对某一文件类型进行个性化是一件非常方便的事情。

例如，我们的 C 代码需要以四个空格作为缩进，并以四个空格取代一个 TAB ，这时候我们就可以这样
```
sudo vim ~/.vim/after/c.vim
```
然后添加这两行命令即可：
```
set shiftwidth=4
set expandtab 
```


