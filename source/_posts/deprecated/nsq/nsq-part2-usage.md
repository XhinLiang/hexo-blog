title: 理解 Nsq （二）初体验
date: 2018-10-30 01:43:29
tags: [nsq,消息队列,messageQueue,go,golang]
categories: 后端
toc: true
---

上一节已经把 Golang 环境搭好了，这一节可以正常开搞。
这一节我打算把 nsq 从源代码编译，然后简单试用下。

## Install from source code

第一步是下载源代码进行编译。

``` bash
$ git clone git@github.com:nsqio/nsq.git $GOPATH/src/github.com/nsqio/nsq
$ cd $GOPATH/src/github.com/nsqio/nsq

$ go get -u github.com/golang/dep/cmd/dep # dep 是一个 Golang 依赖管理工具，这里需要安装下

$ dep ensure # 安装 nsq 的依赖，这块耗时比较久，耐心等待
Solving failure: No versions of github.com/judwhite/go-svc met constraints:
	63c12402f579f0bdf022653c821a1aa5d7544f01: unable to deduce repository and source type for "golang.org/x/sys/windows/svc": unable to read metadata: unable to fetch raw metadata: failed HTTP request to URL "http://golang.org/x/sys/windows/svc?go-get=1": Get http://golang.org/x/sys/windows/svc?go-get=1: dial tcp 216.239.37.1:80: i/o timeout
	v1.0.0: unable to deduce repository and source type for "golang.org/x/sys/windows/svc": unable to read metadata: unable to fetch raw metadata: failed HTTP request to URL "http://golang.org/x/sys/windows/svc?go-get=1": Get http://golang.org/x/sys/windows/svc?go-get=1: dial tcp 216.239.37.1:80: i/o timeout
	master: Could not introduce github.com/judwhite/go-svc@master, as it is not allowed by constraint 63c12402f579f0bdf022653c821a1aa5d7544f01 from project github.com/nsqio/nsq.
```

超时了，挂上蹄子看看：
``` bash
$ proxychains4 dep ensure 
[proxychains] config file found: /home/xhinliang/.proxychains/proxychains.conf
[proxychains] preloading /usr/local/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.11-git-5-ge527b9e
Solving failure: No versions of github.com/judwhite/go-svc met constraints:
	63c12402f579f0bdf022653c821a1aa5d7544f01: unable to deduce repository and source type for "golang.org/x/sys/windows/svc": unable to read metadata: unable to fetch raw metadata: failed HTTP request to URL "http://golang.org/x/sys/windows/svc?go-get=1": Get http://golang.org/x/sys/windows/svc?go-get=1: dial tcp 216.239.37.1:80: i/o timeout
	v1.0.0: unable to deduce repository and source type for "golang.org/x/sys/windows/svc": unable to read metadata: unable to fetch raw metadata: failed HTTP request to URL "http://golang.org/x/sys/windows/svc?go-get=1": Get http://golang.org/x/sys/windows/svc?go-get=1: dial tcp 216.239.37.1:80: i/o timeout
	master: Could not introduce github.com/judwhite/go-svc@master, as it is not allowed by constraint 63c12402f579f0bdf022653c821a1aa5d7544f01 from project github.com/nsqio/nsq.
```

`dep` 命令依旧失败了，这怎么办呢？

看了下这个库，是个 `Windows Service wrapper`，GitHub 主页能正常访问，奇了怪了，我表示不服。

想了想，难道是因为我 `git clone` 的时候使用了 git 协议，而不是官方指导的 https 协议？

``` bash
rm -rf $GOPATH/src/github.com/nsqio
git clone https://github.com/nsqio/nsq $GOPATH/src/github.com/nsqio/nsq

$ cd $GOPATH/src/github.com/nsqio/nsq
$ dep ensure
Solving failure: No versions of github.com/judwhite/go-svc met constraints:
	63c12402f579f0bdf022653c821a1aa5d7544f01: unable to deduce repository and source type for "golang.org/x/sys/windows/svc": unable to read metadata: unable to fetch raw metadata: failed HTTP request to URL "http://golang.org/x/sys/windows/svc?go-get=1": Get http://golang.org/x/sys/windows/svc?go-get=1: dial tcp 216.239.37.1:80: i/o timeout
	v1.0.0: unable to deduce repository and source type for "golang.org/x/sys/windows/svc": unable to read metadata: unable to fetch raw metadata: failed HTTP request to URL "http://golang.org/x/sys/windows/svc?go-get=1": Get http://golang.org/x/sys/windows/svc?go-get=1: dial tcp 216.239.37.1:80: i/o timeout
	master: Could not introduce github.com/judwhite/go-svc@master, as it is not allowed by constraint 63c12402f579f0bdf022653c821a1aa5d7544f01 from project github.com/nsqio/nsq.
```

还是不能正常安装，真是有点意思啊。

怀疑 `proxychains` 没生效，用环境变量的 HTTP 代理试试：
``` bash
export http_proxy=http://127.0.0.1:8118
export https_proxy=http://127.0.0.1:8118
```

另外说下，我的机子上时常有两个蹄子，一个是 `SOCKS` 协议的蹄子，另一个是用 `privoxy` 做的 `HTTP` 协议的二层代理。
所以对于我来说，两个代理事实上是一样的，只不过一般不用环境变量的代理而已。

``` bash
$ dep ensure
# 居然好了...

# 跑个测试看看
$ ./test.sh
?   	github.com/nsqio/nsq/apps/nsq_stat	[no test files]
?   	github.com/nsqio/nsq/apps/nsq_tail	[no test files]
?   	github.com/nsqio/nsq/apps/nsq_to_file	[no test files]
ok  	github.com/nsqio/nsq/apps/nsq_to_http	0.003s
?   	github.com/nsqio/nsq/apps/nsq_to_nsq	[no test files]
?   	github.com/nsqio/nsq/apps/nsqadmin	[no test files]
ok  	github.com/nsqio/nsq/apps/nsqd	0.005s
?   	github.com/nsqio/nsq/apps/nsqlookupd	[no test files]
?   	github.com/nsqio/nsq/apps/to_nsq	[no test files]
?   	github.com/nsqio/nsq/bench/bench_channels	[no test files]
?   	github.com/nsqio/nsq/bench/bench_reader	[no test files]
# ... 一大堆输出
```

官网的文档到此结束，感觉有点突然，我还不知道怎么运行呢。

算了，直接看 Makefile 吧：
``` bash
$ cat Makefile

PREFIX=/usr/local
BINDIR=${PREFIX}/bin
DESTDIR=
BLDDIR = build
BLDFLAGS=
EXT=
ifeq (${GOOS},windows)
    EXT=.exe
endif

APPS = nsqd nsqlookupd nsqadmin nsq_to_nsq nsq_to_file nsq_to_http nsq_tail nsq_stat to_nsq
all: $(APPS)

$(BLDDIR)/nsqd:        $(wildcard apps/nsqd/*.go       nsqd/*.go       nsq/*.go internal/*/*.go)
$(BLDDIR)/nsqlookupd:  $(wildcard apps/nsqlookupd/*.go nsqlookupd/*.go nsq/*.go internal/*/*.go)
$(BLDDIR)/nsqadmin:    $(wildcard apps/nsqadmin/*.go   nsqadmin/*.go nsqadmin/templates/*.go internal/*/*.go)
$(BLDDIR)/nsq_to_nsq:  $(wildcard apps/nsq_to_nsq/*.go  nsq/*.go internal/*/*.go)
$(BLDDIR)/nsq_to_file: $(wildcard apps/nsq_to_file/*.go nsq/*.go internal/*/*.go)
$(BLDDIR)/nsq_to_http: $(wildcard apps/nsq_to_http/*.go nsq/*.go internal/*/*.go)
$(BLDDIR)/nsq_tail:    $(wildcard apps/nsq_tail/*.go    nsq/*.go internal/*/*.go)
$(BLDDIR)/nsq_stat:    $(wildcard apps/nsq_stat/*.go             internal/*/*.go)
$(BLDDIR)/to_nsq:      $(wildcard apps/to_nsq/*.go               internal/*/*.go)

$(BLDDIR)/%:
	@mkdir -p $(dir $@)
	go build ${BLDFLAGS} -o $@ ./apps/$*

$(APPS): %: $(BLDDIR)/%

clean:
	rm -fr $(BLDDIR)

.PHONY: install clean all
.PHONY: $(APPS)

install: $(APPS)
	install -m 755 -d ${DESTDIR}${BINDIR}
	for APP in $^ ; do install -m 755 ${BLDDIR}/$$APP ${DESTDIR}${BINDIR}/$$APP${EXT} ; done
```

对于我这种古典 Unix 程序员来说，用 Makefile 来构建程序是司空见惯的事情。
其实现在的 `package.json` `Dockerfile` 都是类似的作用，不过用在了不同的地方而已，哈哈。

扯远了，我们回归正题。
按脚本说的，如果执行 `make install`，会把 nsq 和对应的扩展包安装在 `/usr/local/bin` 文件夹。

对于我来说，我不喜欢把 `nsq` 安装在这个文件夹，所以我这里把路径改成 ${HOME}/software 了。
其他的同学可以按需求看看要不要改。不管你改不改，反正我是改了，嘿嘿。

接下来开始编译，体验一下 Golang 传说中飞一般的编译速度：
``` bash
$ make install
make install
go build  -o build/nsqd ./apps/nsqd
go build  -o build/nsqlookupd ./apps/nsqlookupd
go build  -o build/nsqadmin ./apps/nsqadmin
go build  -o build/nsq_to_nsq ./apps/nsq_to_nsq
go build  -o build/nsq_to_file ./apps/nsq_to_file
go build  -o build/nsq_to_http ./apps/nsq_to_http
go build  -o build/nsq_tail ./apps/nsq_tail
go build  -o build/nsq_stat ./apps/nsq_stat
go build  -o build/to_nsq ./apps/to_nsq
install -m 755 -d /home/xhinliang/software/bin
for APP in nsqd nsqlookupd nsqadmin nsq_to_nsq nsq_to_file nsq_to_http nsq_tail nsq_stat to_nsq ; do install -m 755 build/$APP /home/xhinliang/software/bin/$APP ; done
```

看起来正常编译了，没啥问题。

编译完了，自然要把程序跑起来：
``` bash
$ cd ~/software/bin
$ ./nsqd &
[1] 20709
[nsqd] 2018/11/03 19:17:47.574971 INFO: nsqd v1.1.0 (built w/go1.11.1)                                                                                                                            
[nsqd] 2018/11/03 19:17:47.575047 INFO: ID: 493
[nsqd] 2018/11/03 19:17:47.575184 INFO: NSQ: persisting topic/channel metadata to nsqd.dat
[nsqd] 2018/11/03 19:17:47.583173 INFO: HTTP: listening on [::]:4151
[nsqd] 2018/11/03 19:17:47.583295 INFO: TCP: listening on [::]:4150
```

再跑个 nsqadmin 看看
``` bash
$ ./nsqadmin --nsqd-http-address [::]:4151
zsh: no matches found: [::]:4151
```

用浏览器看看，nsqadmin已经跑起来了：
![nsqadmin](/uploads/2018/nsq/nsqadmin.png)

## Components

我们到 $HOME/software/bin 目录下看看，nsq总共编译出来的文件还挺多的，这里结合官网简单介绍一下：
``` bash
$ ll
总用量 73M
-rwxr-xr-x 1 xhinliang xhinliang  11M 11月  3 19:16 nsqadmin      # web 管理界面
-rwxr-xr-x 1 xhinliang xhinliang  11M 11月  3 19:16 nsqd          # nsq 后台核心服务
-rw------- 1 xhinliang xhinliang   31 11月  3 19:17 nsqd.dat      # 应该是临时生成的文件
-rwxr-xr-x 1 xhinliang xhinliang 9.8M 11月  3 19:16 nsqlookupd    # nsq 注册中心，客户端在这里获取指定 topic 的 producer 信息
-rwxr-xr-x 1 xhinliang xhinliang 6.7M 11月  3 19:16 nsq_stat      # cli 工具，查看 producer 的详情
-rwxr-xr-x 1 xhinliang xhinliang 7.0M 11月  3 19:16 nsq_tail      # cli 工具，一个集成的 consumer，接受指定的 topic，然后打印到标准输出
-rwxr-xr-x 1 xhinliang xhinliang 7.2M 11月  3 19:16 nsq_to_file   # 与楼上类似，但输出到指定文件
-rwxr-xr-x 1 xhinliang xhinliang 7.2M 11月  3 19:16 nsq_to_http   # 与楼上类似，但会通过 HTTP （GET/POST）请求输出消息内容
-rwxr-xr-x 1 xhinliang xhinliang 7.1M 11月  3 19:16 nsq_to_nsq    # 与楼上类似，但会转发到另外的 nsq topic
-rwxr-xr-x 1 xhinliang xhinliang 6.8M 11月  3 19:16 to_nsq        # 标准输入重定向到 nsq
```

## Run with lookupd

刚刚跑的 standalone 模式，在 `nsqadmin` 上不能创建 topic，所以现在结合 `nsqlookupd` 再跑一遍：
``` bash
$ ./nsqlookupd &

$ ./nsqd -lookupd-tcp-address localhost:4160 &

$ ./nsqadmin --lookupd-http-address localhost:4161 &
```

可以看到，这里已经可以生成 Topic 了：
![nsqadmin-lookup-panel](/uploads/2018/nsq/nsqadmin-lookup-panel.png)

创建一个 Topic 试试看：
![nsqadmin-create-topic](/uploads/2018/nsq/nsqadmin-create-topic.png)

跑一个 `nsq_tail`，消费刚刚的 Topic：
``` bash
$ ./nsq_tail -lookupd-http-address localhost:4161 -channel test-channel -topic plain-text
```

再跑一个 `to_nsq`，将命令行的内容重定向到我们定义的 Topic：
``` bash
$ ./to_nsq -nsqd-tcp-address localhost:4150  -topic plain-text
```

可以看到，生产者和消费者正常运行：
![nsq-cli-test](/uploads/2018/nsq/nsq-cli-test.png)

同时，因为我在同一个 topic 中创建了两个不同的 channel，但只有一个 channel 有消费，可以看到另外一个 channel 造成了堆积：

![nsqadmin-topic](/uploads/2018/nsq/nsqadmin-topic.png)

这个时候，我们再启动一个 Consumer，消费 `test-channel1` 中的消息：
``` bash
./nsq_tail -lookupd-http-address localhost:4161 -channel test-channel1 -topic plain-text
2018/11/04 00:46:56 Adding consumer for topic: plain-text
2018/11/04 00:46:56 INF    1 [plain-text/test-channel1] querying nsqlookupd http://localhost:4161/lookup?topic=plain-text
2018/11/04 00:46:56 INF    1 [plain-text/test-channel1] (Latitude:4150) connecting to nsqd
fefef
fefef
wfefef
wefwef
wfewfwevv
abc
ccc
fwefe
efwf
wfwef
wefef
efef
wefwef
fewf
```

可以看到堆积的消息一下子全发过来了，`nsqadmin` 中的堆积也清除掉了。

## PostView

这一次的操作中，我们编译了 nsq 及一些 cli 工具，并成功运行 nsq，在命令行完成了生产者和消费者模型的测试。
nsq 整体设计跟 Kafka 类似，但得益于配套的 cli 工具，跑起整套流程还是比较简单。

下一篇博文中，我会跟大家一起学习下 nsq 的一些基本概念，包括 Topic，Producer，Channel 等概念。