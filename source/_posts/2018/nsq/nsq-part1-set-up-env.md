title: 理解 Nsq （一）设置 Golang 开发环境
date: 2018-10-30 01:43:29
tags: [Golang,GOPATH,GOROOT,Golang环境搭建,Go,go,golang]
categories: 后端
toc: true
---

Nsq 是一个 Golang 实现的消息队列，现在应该特性已经比较稳定了。
看了下代码量，还 OK，那么最近开始倒腾倒腾他。

开始倒腾之前，先把环境搭好，那么我来在我的两个主要工作环境上把 Golang 环境搭好。

## macOS

首先我在公司的电脑的 macOS 系统装上 Golang 吧，直接最新版本开怼：
``` bash
brew install go
```

可以说安装是相当傻瓜化了。

准备一个 hello world 程序（感觉回到了大一）
注意一下，这个 go 程序的风格有问题。
``` bash
$ cat hello.go
package main

import "fmt"

func main   (){
   fmt.Printf("hello, world\n")
}

$ go run hello.go
hello, world
```
能正常运行。

试下 gofmt

``` bash
$ go fmt hello.go
hello.go

$ cat hello.go
package main

import "fmt"

func main() {
	fmt.Printf("hello, world\n")
}
```

可以看到 go fmt 将代码自动格式化了。

Golang 的代码目前来看基本各家都是统一的，相比 Java，省去了大家的成本。

不过这语法是有点丑哈，哈哈哈哈哈

## Ubuntu

我家里的 Ubuntu 电脑很久以前装了 Golang 了（忘了咋装的了，应该是 apt-get 装的）
隐约记得，好像 go fmt 功能有一点问题的。

回到家了，发现我不知道啥时候已经把 Go 删除了，正好，我要重装一个

在官网找到下载链接： (下载)[https://golang.org/dl/]
官网说，已经事先为大家编译好二进制了，大家直接下载编译好的结果就行了。

嗯，编译 Golang 应该挺麻烦的，所以我还是选择下载 releases 包。
有时间折腾的同学可以下载源代码编译。

三个平台分别有三个 release 包，证明 Golang 的兼容是相当好了（不同 Linux 发行版间差异还是挺大的，很多软件是需要根据发行版来重新编译的）。
``` bash
$ pwd
/home/xhinliang/software

$ wget https://dl.google.com/go/go1.11.1.linux-amd64.tar.gz
  # ... 一些下载进度输出

$ tar zxvf go1.11.1.linux-amd64.tar.gz
  # ... 一大堆输出

$ pwd
/home/xhinliang/software/go

$ ls
api  AUTHORS  bin  CONTRIBUTING.md  CONTRIBUTORS  doc  favicon.ico  lib  LICENSE  misc  PATENTS  pkg  README.md  robots.txt  src  test  VERSION

$ bin/go version
go version go1.11.1 linux/amd64
```

至此 Golang 在 Linux 环境就安装好了

## Workspaces

Golang 有个 Workspace 的概念，其实就是一个文件夹，默认是 $HOME/go/。

假设 /home/xhinliang/code/GoProjects/go-hello 这个文件夹是一个 Workspace，那么这个文件夹需要包含两个子文件夹
- bin # 编译后的二进制文件
- src # 源代码文件

为了让大家理解，官网给了一个例子：
```
bin/
    hello                          # command executable
    outyet                         # command executable
src/
    github.com/golang/example/
        .git/                      # Git repository metadata
	    hello/
	        hello.go               # command source
    	outyet/
     	    main.go                # command source
	        main_test.go           # test source
    	stringutil/
	        reverse.go             # package source
	        reverse_test.go        # test source
    golang.org/x/image/
        .git/                      # Git repository metadata
    	bmp/
    	    reader.go              # package source
    	    writer.go              # package source
    ... (many more repositories and packages omitted) ...
```

可以注意到， src 的 github.com/golang/example/ 类似的文件夹，这些显然是第三方的库。

一个典型的 Golang Workplace 应该包含很多第三方的库的源代码，和一些必要的二进制的文件，这点跟 $HOME/node_modules 差不多。

大多数的 Golang 开发者都会只使用一个 Golang Workplace。

如果有需要的话，可以设置多个，通过设置 GOPATH 环境变量来实现。

## 环境变量的设置

为了开发顺利，安装 Golang 开发环境最好配置几个环境变量。
在 $HOME 目录下创建一个配置文件 `.shrc_golang`

## GOROOT

首先把 Golang 的 bin 目录加到 PATH 环境变量中。
``` bash
export GOROOT="$HOME/software/go"
export PATH="$GOROOT/bin:$PATH"
```

### GOPATH

GOPATH 环境变量指明 Golang Workplace 的目录。
默认值是 `$HOME/go`，可以用 `go env` 查询当前的 GOPATH：
``` bash
$ go env GOPATH
/home/xhinliang/go
```

我使用 Golang 的默认 Workplace 路径，但是还是显式配置下 GOPATH 吧，以后想改的话也方便。
在 ~/.shrc_golang 中加入这一行：
```
export GOPATH="$HOME/go"
```

上面说了，Workplace 下可能有第三方的二进制文件，为了能方便使用，我这里把路径加到 PATH 环境变量中。
在 ~/.shrc_golang 中加入这一行：
```
export PATH="$GOPATH/bin:$PATH"
```

### 测试 && zshrc 配置

``` bash
$ cat ~/.shrc_golang 
# 设置 Golang 的安装目录
export GOROOT="$HOME/software/go"
export PATH="$GOROOT/bin:$PATH"

# 设置 GOPATH
export GOPATH="$HOME/go"
export PATH="$GOPATH/bin:$PATH"


$ source ~/.shrc_golang
$ go version
go version go1.11.1 linux/amd64

$ echo $GOPATH
/home/xhinliang/go

# 装个第三方的库试试
$ go get github.com/cjbassi/gotop
$ gotop
## 炫哭的界面，哈哈
```

测试没啥问题，我们把 .shrc_golang 加到 zshrc 中吧。
在 ~/.zshrc 的最后加入这行：
```
source  ~/.shrc_golang
```

重启 zsh，再试下，没问题。