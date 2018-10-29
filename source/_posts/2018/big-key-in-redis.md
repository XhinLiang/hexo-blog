title: 为什么不建议在 Redis 使用大 Key
date: 2018-10-30 00:57:29
tags: [后端,缓存,Java,Redis,Lua,运维,DevOps]
categories: 后端
toc: true
---

## Preview

公司里某位工程师小斌发现在一个 Redis 集群中的 some_big_list 经常出现慢查询，而且 QPS 特别高。初步定位是出现了一个热点的 Key。
``` bash
newexplore> llen some_big_list
500000
```
上面的命令发现，这个 some_big_list 是一个大 Key，导致 Redis Server 的服务器 CPU idle 很低，结果出现了慢查询。

当公司里富有经验的工程师磊哥介入调查的时候，发现这个 Redis Server 的所有响应在某一个时刻出现了 block。
磊哥是很牛逼的，怀疑是不是小斌在线上直接执行了 `del some_big_list` 操作。

结果当然是啦！

小斌 `del some_big_list` 的时候， Redis 的单线程模型只顾着删数据了（`del` 的时间复杂度是 O(N)），没有时间响应请求，直接导致出现一大堆请求超时。
而线上的 Redis 请求超时，又会让 Redis 的线程池打满，从而线上的 API Server 的 CPU 也会直接飙升。

不过还好，这个不是太大的 Key，这个业务也不是很核心的业务，所以没有造成什么影响。

## Overview

上面的例子告诉我们，Redis 大 Key 是一件很容易造成线上事故的事情，我们在业务上要尽量避免大 Key 的产生。
当不小心产生大 Key 的时候，我们也不能直接把整个 key 直接 del 掉，会影响其他的业务（不读取这个 key 的业务也会收到影响）。

那么，我们在出现 Redis 大 Key 的时候，应该怎么处理呢？
- 业务层面，可以使用更小粒度的单位（时间单位或者地点单位，what ever），先换一个 keyPrefix。
- 换了 keyPrefix 之后，需要对老的 keyPrefix 作清理
  - 如果是 Redis 4.0 以后的版本，可以把 `del` 命令换成 `unlink` 命令，使用这个命令的时候，Redis 会另起一个线程进行删除，不会影响别的业务请求。其实也很好理解，既然把这个 key 删除了，那么也很容易搞定多线程不一致的问题了。
  - 如果是更老的版本，可以设立一个准则：慢慢删...
    - 如果是 `list`，可以使用 `ltrim` 慢慢删
    - 如果是 `zset`, 可以使用 `zremrangebyscore` 之类的命令慢慢删...
    - 如果是 `hash` 或者 `set`，比较麻烦，请自己慢慢找合适的命令吧。。

## Test

好了，说了基础知识，我们来实地演练一下。

### Concept
首先说下我对分布式系统的 “响应时间” 的认知：
- `t<0.1ms`，非常快，没有优化的必要
- `0.1ms<t<1ms`，挺快的，基本不会对系统造成瓶颈
- `1ms<t<10ms`，凑活用，如果不是核心链路，基本 OK
- `10ms<t<100ms`，有点慢了，需要找时间优化
- `100ms<t<1000ms`，太慢了，赶紧查下原因吧！
- `t>1000ms`，这他妈怎么用啊，下线算了

注意这个是分布式系统的响应时间，而 Redis 作为一个最基础的缓存中间件，我认为对他的要求要更高一些（10x吧）

### Platform
这场测试在我自己的电脑上做，先来了解下我的爱机：

CPU：i5-3380m@3.6Ghz，双核四线程
``` bash
$ cat /proc/cpuinfo
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 58
model name	: Intel(R) Core(TM) i5-3380M CPU @ 2.90GHz
stepping	: 9
microcode	: 0x20
cpu MHz		: 1272.714
cache size	: 3072 KB
physical id	: 0
siblings	: 4
core id		: 0
cpu cores	: 2
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 13
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm epb ssbd ibrs ibpb stibp kaiser tpr_shadow vnmi flexpriority ept vpid fsgsbase smep erms xsaveopt dtherm ida arat pln pts flush_l1d
bugs		: cpu_meltdown spectre_v1 spectre_v2 spec_store_bypass l1tf
bogomips	: 5780.76
clflush size	: 64
cache_alignment	: 64
address sizes	: 36 bits physical, 48 bits virtual
power management:
```

内存： 2×8G DDR3L 1600Mhz
``` bash
$ free -m
             total       used       free     shared    buffers     cached
Mem:         15951      13847       2103        445       2331       6722
-/+ buffers/cache:       4794      11156
Swap:        15624          0      15624
```
系统版本：
``` bash
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="14.04.5 LTS, Trusty Tahr"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 14.04.5 LTS"
VERSION_ID="14.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
```


系统限制
``` bash
$ ulimit -a
-t: cpu time (seconds)              unlimited
-f: file size (blocks)              unlimited
-d: data seg size (kbytes)          unlimited
-s: stack size (kbytes)             8192
-c: core file size (blocks)         0
-m: resident set size (kbytes)      unlimited
-u: processes                       63332
-n: file descriptors                65535
-l: locked-in-memory size (kbytes)  64
-v: address space (kbytes)          unlimited
-x: file locks                      unlimited
-i: pending signals                 63332
-q: bytes in POSIX msg queues       819200
-e: max nice                        0
-r: max rt priority                 0
-N 15:                              unlimited

```

硬盘：美光 M500,480G
``` bash
$ dd if=/dev/zero of=test bs=64k count=512 oflag=dsync
记录了512+0 的读入
记录了512+0 的写出
33554432字节(34 MB)已复制，5.16719 秒，6.5 MB/秒
```

Redis版本：2.8，很老的版本了，连 Redis-Cluster 都不支持的版本
``` bash
$ redis-server -v
Redis server v=2.8.4 sha=00000000:0 malloc=jemalloc-3.4.1 bits=64 build=a44a05d76f06a5d9
```

### Upgrade Redis

非常尴尬，我的机器上的 Redis 居然是 2.8 这个上古世纪的版本，既然这样我就把它先删了吧（笑）

``` bash
sudo apt-get remove redis-server
```

一顿操作猛如虎，编译源代码走起！
``` bash
$ wget http://download.redis.io/releases/redis-5.0.0.tar.gz
$ tar xzf redis-5.0.0.tar.gz
$ cd redis-5.0.0
$ make # 编译走起
$ make test # 编译完了跑个测试吧
```
Redis 是很轻量的，按理说编译不会有什么坑，果然顺滑无比，编译加测试总共只花了三分钟。

那么现在来试下新版本的 Redis 吧！
``` bash
$ src/redis-server -v
Redis server v=5.0.0 sha=00000000:0 malloc=jemalloc-5.1.0 bits=64 build=792f3c7998732f3c

$ src/redis-server
21176:C 29 Oct 2018 00:24:32.717 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
21176:C 29 Oct 2018 00:24:32.717 # Redis version=5.0.0, bits=64, commit=00000000, modified=0, pid=21176, just started
21176:C 29 Oct 2018 00:24:32.717 # Warning: no config file specified, using the default config. In order to specify a config file use src/redis-server /path/to/redis.conf
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 5.0.0 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 21176
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           http://redis.io        
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                                               

21176:M 29 Oct 2018 00:24:32.720 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
21176:M 29 Oct 2018 00:24:32.720 # Server initialized
21176:M 29 Oct 2018 00:24:32.720 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
21176:M 29 Oct 2018 00:24:32.720 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
21176:M 29 Oct 2018 00:24:32.720 * DB loaded from disk: 0.000 seconds
21176:M 29 Oct 2018 00:24:32.720 * Ready to accept connections
```

Server 成功跑起来了，我们来开启另一个 Shell 窗口来启动 Client：
```
$ src/redis-cli
127.0.0.1:6379>
```

So Easy～
先看看现在 Redis 占用了多少内存吧
``` bash
$ ps aef -o command,vsize,rss,%mem,size | grep redis-server 
src/redis-server *:6379  63004  5532  0.0 40964
```
好吧，0%，先忽略。。


准备一个 lua 脚本，我们保存为 add-test-big-key.lua
``` lua
local bulk = 1000
local fvs = {}
local j
for i = 1, ARGV[1] do
  j = i % bulk
  if j == 0 then
    fvs[2 * bulk - 1] = "field" .. i
    fvs[2 * bulk] = "value" .. i
    redis.call("HMSET", KEYS[1], unpack(fvs))
    fvs = {}
  else
    fvs[2 * j - 1] = "field" .. i
    fvs[2 * j] = "value" .. i
  end
end
if #fvs > 0 then
  redis.call("HMSET", KEYS[1], unpack(fvs))
end
return "OK"
```
此脚本参考 [how to load lua script from file for redis](https://groups.google.com/d/msg/redis-db/0UzLhSkAziQ/H-35GJfqtisJ)


灌数据，然后看下内存占用
``` bash
$ src/redis-cli --eval add-test-big-key.lua big_hash1 , 1000000
"OK"
$ ps aef -o command,vsize,rss,%mem,size | grep redis-server
src/redis-server *:6379 134660 74044  0.4 112620
```

可以看到虽然这个大Key里有100w条数据，但内存占用依然很低。
我们现在尝试把这个 key 删除，并查看 SLOWLOG。

``` bash
127.0.0.1:6379> del big_hash1
(integer) 1
127.0.0.1:6379> SLOWLOG GET 2
1) 1) (integer) 2009
   2) (integer) 1540777173
   3) (integer) 373285
   4) 1) "del"
      2) "big_hash1"
   5) "127.0.0.1:57110"
   6) ""
2) 1) (integer) 2008
   2) (integer) 1540777157
   3) (integer) 2325250
   4) 1) "EVAL"
      2) "local bulk = 1000\nlocal fvs = {}\nlocal j\nfor i = 1, ARGV[1] do\n  j = i % bulk\n  if j == 0 then\n    fvs[2 * bulk - 1] = \"field\" .... (254 more bytes)"
      3) "1"
      4) "big_hash1"
      5) "1000000"
   5) "127.0.0.1:57234"
   6) ""
```

可以看到 del 操作持续了 373ms，在线上环境中，这个影响应该不算大。

我们把数据量增大 100 倍看下吧，预期 redis-server 会占用 40% 左右的内存（redis好像没有这方面的优化。。）：

``` bash
$ src/redis-cli --eval add-test-big-key.lua big_hash1 , 100000000 
"OK"
$ ps aef -o command,vsize,rss,%mem,size | grep redis-server    
src/redis-server *:6379 7804420 6656092 40.7 7782380
```

果不其然。。

``` bash
127.0.0.1:6379> del big_hash1
(integer) 1
(62.95s)
127.0.0.1:6379> SLOWLOG GET 2
1) 1) (integer) 102012
   2) (integer) 1540777822
   3) (integer) 62952411
   4) 1) "del"
      2) "big_hash1"
   5) "127.0.0.1:57110"
   6) ""
2) 1) (integer) 102011
   2) (integer) 1540777634
   3) (integer) 279820829
   4) 1) "EVAL"
      2) "local bulk = 1000\nlocal fvs = {}\nlocal j\nfor i = 1, ARGV[1] do\n  j = i % bulk\n  if j == 0 then\n    fvs[2 * bulk - 1] = \"field\" .... (254 more bytes)"
      3) "1"
      4) "big_hash1"
      5) "100000000"
   5) "127.0.0.1:57324"
   6) ""
```

牛逼了，删这个 key 花了一分钟，在线上肯定爆炸了。。（其实灌数据的脚本花了更久，这个忽略吧。。）
这个数据量是 100m 条数据（简单数据），对于线上还是有参考意义的。

接下来我们是下 `unlink` 的性能

``` bash
$ src/redis-cli --eval add-test-big-key.lua big_hash3 , 100000000 &

127.0.0.1:6379> unlink big_hash2
(integer) 1

$ top
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND                                                         
 3512 xhinlia+  20   0 7806468 6.349g   3720 S 102.9 40.8  11:24.49 redis-server   
```

可以看到， `unlink` 立刻就返回了，但是 redis-server 还是会消耗很多 CPU。

接下来我们看一下大 key 自然过期的时候会发生什么事情：
``` bash
$ src/redis-cli --eval add-test-big-key.lua big_hash3 , 100000000 

127.0.0.1:6379> expire big_hash3 5
(integer) 1

127.0.0.1:6379> set abc xxx EX 10
（卡住了。。。）
```
可以看到，自然过期的大 key 也出现了阻塞。

## PostScript

总结一下：
- 尽量从业务上避免 Redis 大 Key，无论从性能角度（hash成本）还是过期删除成本，都会比较高
- 尽量使用 `unlink` 代替 `del` 删除大 key
- key 的自然活期和手动删除，都会阻塞 Redis