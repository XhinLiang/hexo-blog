title: 安装 Ubuntu Workstation 之后要做的事儿
date: 2019-1-11
tags: [Ubuntu,Linux]
categories: Linux
toc: true
---

# 安装 Ubuntu Workstation 之后要做的事儿

## Pre

最近自己心爱的 Dell Latitude E6430s 频繁死机，以为是硬盘问题，格式化硬盘重装系统问题依旧。
硬件检查才发现是一根内存有了问题，取出问题的内存后一切正常。

但删掉的系统是需要重装的，经过一些实践后，我选择了 Ubuntu 16.04 LTS 作为我新的操作系统。

## Why

都 2019 年了，为什么还要选择老旧的 Ubuntu 16.04 呢？
其实我之前试过了几个 Linux 发行版，都有一些问题：
- Ubuntu 14.04 LTS，这也是我之前一直使用的发行版，稳定性尚可，但很快就结束维护了。
- Manjaro Xfce/i3wm，可能我的电脑硬件太老旧了，pacman -SYy 之后基本就滚挂了，试了几遍都这样，无奈放弃。
- Fedora，官方貌似只维护 Gnome 版本，不太喜欢，放弃。
- Ubuntu 18.04 LTS，桌面也换成了 Gnome，非常别扭别扭，放弃。

最后试了下 Ubuntu 16.04 LTS，安装非常顺利，基本配置以后也非常顺手，所以就硬定他了。

## Install

本次安装还是 Windows 10 + Ubuntu 16.04 双系统。
我的主硬盘是一块 480G 的固态硬盘，所以我还是依照原来的方案，把两个系统都装在这个硬盘。

### Step 0

Windows 10 安装，先格式化整个硬盘，并将分区表修改为 GPT 格式：
```
diskpart
clean
convert gpt
```

<!--?xml version="1.0" encoding="UTF-8" standalone="no"?--><svg xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink" contentscripttype="application/ecmascript" contentstyletype="text/css" height="438px" preserveAspectRatio="none" style="width:858px;height:438px;" version="1.1" viewBox="0 0 858 438" width="858px" zoomAndPan="magnify"><defs><filter height="300%" id="fxoswz7k1hita" width="300%" x="-1" y="-1"><feGaussianBlur result="blurOut" stdDeviation="2.0"></feGaussianBlur><feColorMatrix in="blurOut" result="blurOut2" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .4 0"></feColorMatrix><feOffset dx="4.0" dy="4.0" in="blurOut2" result="blurOut3"></feOffset><feBlend in="SourceGraphic" in2="blurOut3" mode="normal"></feBlend></filter></defs><g><ellipse cx="434.5" cy="20" fill="#000000" filter="url(#fxoswz7k1hita)" rx="10" ry="10" style="stroke: none; stroke-width: 1.0;"></ellipse><polygon fill="#FEFECE" filter="url(#fxoswz7k1hita)" points="32,50,119,50,131,62,119,74,32,74,20,62,32,50" style="stroke: #A80036; stroke-width: 1.5;"></polygon><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="18" x="79.5" y="84.6348">yes</text><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="87" x="32" y="66.1572">1.是否取到了数据</text><polygon fill="#FEFECE" filter="url(#fxoswz7k1hita)" points="163,50,250,50,262,62,250,74,163,74,151,62,163,50" style="stroke: #A80036; stroke-width: 1.5;"></polygon><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="18" x="210.5" y="84.6348">yes</text><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="87" x="163" y="66.1572">2.是否取到了数据</text><rect fill="#FEFECE" filter="url(#fxoswz7k1hita)" height="34.1328" rx="12.5" ry="12.5" style="stroke: #A80036; stroke-width: 1.5;" width="100" x="156.5" y="106.9551"></rect><text fill="#000000" font-family="sans-serif" font-size="12" lengthAdjust="spacingAndGlyphs" textLength="80" x="166.5" y="128.5566">将数据回写到1</text><polygon fill="#FEFECE" filter="url(#fxoswz7k1hita)" points="294,50,381,50,393,62,381,74,294,74,282,62,294,50" style="stroke: #A80036; stroke-width: 1.5;"></polygon><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="18" x="341.5" y="84.6348">yes</text><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="87" x="294" y="66.1572">3.是否取到了数据</text><rect fill="#FEFECE" filter="url(#fxoswz7k1hita)" height="34.1328" rx="12.5" ry="12.5" style="stroke: #A80036; stroke-width: 1.5;" width="112" x="281.5" y="106.9551"></rect><text fill="#000000" font-family="sans-serif" font-size="12" lengthAdjust="spacingAndGlyphs" textLength="92" x="291.5" y="128.5566">将数据回写到1,2</text><polygon fill="#FEFECE" filter="url(#fxoswz7k1hita)" points="432,50,519,50,531,62,519,74,432,74,420,62,432,50" style="stroke: #A80036; stroke-width: 1.5;"></polygon><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="18" x="479.5" y="84.6348">yes</text><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="87" x="432" y="66.1572">4.是否取到了数据</text><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="14" x="531" y="59.6797">no</text><rect fill="#FEFECE" filter="url(#fxoswz7k1hita)" height="34.1328" rx="12.5" ry="12.5" style="stroke: #A80036; stroke-width: 1.5;" width="124" x="413.5" y="106.9551"></rect><text fill="#000000" font-family="sans-serif" font-size="12" lengthAdjust="spacingAndGlyphs" textLength="104" x="423.5" y="128.5566">将数据回写到1,2,3</text><rect fill="#FEFECE" filter="url(#fxoswz7k1hita)" height="34.1328" rx="12.5" ry="12.5" style="stroke: #A80036; stroke-width: 1.5;" width="292" x="555" y="103.4775"></rect><text fill="#000000" font-family="sans-serif" font-size="12" lengthAdjust="spacingAndGlyphs" textLength="272" x="565" y="125.0791">到下一级缓存中寻找数据，找到数据后回写1,2,3,4</text><rect fill="#FEFECE" filter="url(#fxoswz7k1hita)" height="34.1328" rx="12.5" ry="12.5" style="stroke: #A80036; stroke-width: 1.5;" width="104" x="382.5" y="229.5654"></rect><text fill="#000000" font-family="sans-serif" font-size="12" lengthAdjust="spacingAndGlyphs" textLength="84" x="392.5" y="251.167">返回给上级缓存</text><ellipse cx="434.5" cy="301.1318" fill="none" filter="url(#fxoswz7k1hita)" rx="10" ry="10" style="stroke: #000000; stroke-width: 1.0;"></ellipse><ellipse cx="435" cy="301.6318" fill="#000000" filter="url(#fxoswz7k1hita)" rx="6" ry="6" style="stroke: none; stroke-width: 1.0;"></ellipse><polygon fill="#FEFECE" filter="url(#fxoswz7k1hita)" points="396,181.0879,473,181.0879,485,193.0879,473,205.0879,396,205.0879,384,193.0879,396,181.0879" style="stroke: #A80036; stroke-width: 1.5;"></polygon><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="18" x="438.5" y="215.7227">yes</text><text fill="#000000" font-family="sans-serif" font-size="11" lengthAdjust="spacingAndGlyphs" textLength="77" x="396" y="197.2451">是否有上级缓存</text><rect fill="#FEFECE" filter="url(#fxoswz7k1hita)" height="34.1328" rx="12.5" ry="12.5" style="stroke: #A80036; stroke-width: 1.5;" width="92" x="388.5" y="353.1318"></rect><text fill="#000000" font-family="sans-serif" font-size="12" lengthAdjust="spacingAndGlyphs" textLength="72" x="398.5" y="374.7334">返回到应用层</text><ellipse cx="434.5" cy="417.2646" fill="none" filter="url(#fxoswz7k1hita)" rx="10" ry="10" style="stroke: #000000; stroke-width: 1.0;"></ellipse><ellipse cx="435" cy="417.7646" fill="#000000" filter="url(#fxoswz7k1hita)" rx="6" ry="6" style="stroke: none; stroke-width: 1.0;"></ellipse><line style="stroke: #A80036; stroke-width: 1.5;" x1="75.5" x2="75.5" y1="74" y2="161.0879"></line><polygon fill="#A80036" points="71.5,151.0879,75.5,161.0879,79.5,151.0879,75.5,155.0879" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="206.5" x2="206.5" y1="74" y2="106.9551"></line><polygon fill="#A80036" points="202.5,96.9551,206.5,106.9551,210.5,96.9551,206.5,100.9551" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="206.5" x2="206.5" y1="141.0879" y2="161.0879"></line><polygon fill="#A80036" points="202.5,151.0879,206.5,161.0879,210.5,151.0879,206.5,155.0879" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="337.5" x2="337.5" y1="74" y2="106.9551"></line><polygon fill="#A80036" points="333.5,96.9551,337.5,106.9551,341.5,96.9551,337.5,100.9551" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="337.5" x2="337.5" y1="141.0879" y2="161.0879"></line><polygon fill="#A80036" points="333.5,151.0879,337.5,161.0879,341.5,151.0879,337.5,155.0879" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="475.5" x2="475.5" y1="74" y2="106.9551"></line><polygon fill="#A80036" points="471.5,96.9551,475.5,106.9551,479.5,96.9551,475.5,100.9551" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="475.5" x2="475.5" y1="141.0879" y2="161.0879"></line><polygon fill="#A80036" points="471.5,151.0879,475.5,161.0879,479.5,151.0879,475.5,155.0879" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="131" x2="151" y1="62" y2="62"></line><polygon fill="#A80036" points="141,58,151,62,141,66,145,62" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="262" x2="282" y1="62" y2="62"></line><polygon fill="#A80036" points="272,58,282,62,272,66,276,62" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="393" x2="420" y1="62" y2="62"></line><polygon fill="#A80036" points="410,58,420,62,410,66,414,62" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="434.5" x2="434.5" y1="30" y2="35"></line><line style="stroke: #A80036; stroke-width:1.5;" x1="434.5" x2="75.5" y1="35" y2="35"></line><line style="stroke: #A80036; stroke-width: 1.5;" x1="75.5" x2="75.5" y1="35" y2="50"></line><polygon fill="#A80036" points="71.5,40,75.5,50,79.5,40,75.5,44" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="531" x2="701" y1="62" y2="62"></line><line style="stroke: #A80036; stroke-width: 1.5;" x1="701" x2="701" y1="62" y2="103.4775"></line><polygon fill="#A80036" points="697,93.4775,701,103.4775,705,93.4775,701,97.4775" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="701" x2="701" y1="137.6104" y2="161.0879"></line><polygon fill="#A80036" points="697,151.0879,701,161.0879,705,151.0879,701,155.0879" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="75.5" x2="701" y1="161.0879" y2="161.0879"></line><line style="stroke: #A80036; stroke-width: 1.5;" x1="434.5" x2="434.5" y1="263.6982" y2="291.1318"></line><polygon fill="#A80036" points="430.5,281.1318,434.5,291.1318,438.5,281.1318,434.5,285.1318" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="434.5" x2="434.5" y1="205.0879" y2="229.5654"></line><polygon fill="#A80036" points="430.5,219.5654,434.5,229.5654,438.5,219.5654,434.5,223.5654" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="485" x2="497" y1="193.0879" y2="193.0879"></line><polygon fill="#A80036" points="493,261.1318,497,271.1318,501,261.1318,497,265.1318" style="stroke: #A80036; stroke-width: 1.5;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="497" x2="497" y1="193.0879" y2="333.1318"></line><line style="stroke: #A80036; stroke-width: 1.5;" x1="497" x2="434.5" y1="333.1318" y2="333.1318"></line><line style="stroke: #A80036; stroke-width: 1.5;" x1="434.5" x2="434.5" y1="333.1318" y2="353.1318"></line><polygon fill="#A80036" points="430.5,343.1318,434.5,353.1318,438.5,343.1318,434.5,347.1318" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="434.5" x2="434.5" y1="161.0879" y2="181.0879"></line><polygon fill="#A80036" points="430.5,171.0879,434.5,181.0879,438.5,171.0879,434.5,175.0879" style="stroke: #A80036; stroke-width: 1.0;"></polygon><line style="stroke: #A80036; stroke-width: 1.5;" x1="434.5" x2="434.5" y1="387.2646" y2="407.2646"></line><polygon fill="#A80036" points="430.5,397.2646,434.5,407.2646,438.5,397.2646,434.5,401.2646" style="stroke: #A80036; stroke-width: 1.0;"></polygon><!--
@startuml
start
if (1.是否取到了数据) then (yes)
elseif (2.是否取到了数据) then (yes)
  :将数据回写到1;
elseif (3.是否取到了数据) then (yes)
  :将数据回写到1,2;
elseif (4.是否取到了数据) then (yes)
  :将数据回写到1,2,3;
else (no)
  :到下一级缓存中寻找数据，找到数据后回写1,2,3,4;
endif
if (是否有上级缓存) then (yes)
  :返回给上级缓存;
  stop
endif
:返回到应用层;
stop
@enduml

PlantUML version 1.2018.11(Sun Sep 23 00:43:53 CST 2018)
(GPL source distribution)
Java Runtime: Java(TM) SE Runtime Environment
JVM: Java HotSpot(TM) 64-Bit Server VM
Java Version: 1.8.0_181-b13
Operating System: Mac OS X
OS Version: 10.13.6
Default Encoding: US-ASCII
Language: zh
Country: CN
--></g></svg>

然后分出 200G 给 Windows 10，Windows 安装程序会自动再分出三个小分区，我们只需要关注其中 100M 的那个 EFI 分区，此分区的文件系统是 FAT32，应该非常好辨认。

### Step 1

Windows 10 顺利安装完成，用 xxx 把 Ubuntu 的 ISO 文件写入U盘。
然后重启进入 Ubuntu Live 系统。

选择安装。
手动分区。
分出一个 EXT4 文件系统的分区，大小是 12G，分区类型是 `SWAP`（事实上就是虚拟内存）。
剩下的 250G 再分出一个 EXT4 的分区，没有分区类型，此分区直接挂载到 `/`（根目录）。
然后最下方的启动磁盘直接选择整个固态硬盘（我这边好像是 SDA ）

确认安装，应该没问题了。

## Init

### 修改 home 目录下的文件夹目录为英文

``` bash
export LANG=en_US
xdg-user-dirs-gtk-update

# 此时会弹出弹框，确认即可
# 再把语言设回来
export LANG=zh_CN
```
### Softwares

以下软件手动寻找 deb 安装文件，使用 dpkg 安装即可
VS Code
Chrome
S1h1a1d1o1w1s1o1c1k1s1-QT5
Nutcloud
网易云音乐

### Sogoupingying
官网下载 deb 格式的安装包
``` bash
sudo dpkg -i sogoupinyin_2.2.0.0108_amd64.deb
sudo apt-get -f install # 解决依赖冲突问题
```

### 删掉亚马逊
``` bash
sudo apt-get remove unity-webapps-common
```

## 美化命令行
以下步骤按对应的说明安装即可
安装 oh-my-zsh
安装 ZSH 主题 https://github.com/bhilburn/powerlevel9k
安装 Powerline 字体 https://github.com/powerline/fonts 直接 clone 代码库，install 完事儿

### 安装几个 ZSH 插件
自行安装
zsh-autosuggestions
zsh-syntax-highlighting


## 安装必备开发工具
安装 `n` && `node`
k-vim https://github.com/wklken/k-vim

安装 `golang`
https://xhinliang.win/2018/10/30/2018/nsq/nsq-part1-set-up-env/

安装 Oracle JDK 11
https://www.oracle.com/technetwork/java/javase/downloads/jdk11-downloads-5066655.html

### 设置 Golang 的安装目录
export GOROOT="$HOME/cli-utils/golang/go"
export PATH="$GOROOT/bin:$PATH"

### 设置 GOPATH
export GOPATH="$HOME/go"
export PATH="$GOPATH/bin:$PATH"

### Java
export JAVA_HOME="/usr/lib/jvm/jdk-11.0.1"
export JRE_HOME="$JAVA_HOME/jre"
export CLASSPATH=".:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH"
export PATH="$JAVA_HOME/bin:$JRE_HOME/bin:$PATH"

### 配置小飞机
地址忽略

小飞机的本地代理可以直接使用 HTTP 形式，所以可以直接用 HTTP 代理暴露出来，然后使用
`google-chrome --proxy-server="http://localhost:1080"`
这个命令给 chrome 配置 proxy 并启动，然后登录原来的账号，就可以安装上各种插件，包括 SwitchyOmega

安装 proxychains 并配置
``` bash
sudo apt install proxychains
sudo vim /etc/proxychains.conf
```

### autojump
https://github.com/wting/autojump

``` bash
git clone git://github.com/wting/autojump.git
cd autojump
./install.py
```

.zshrc 加上 plugin，并加上 autojump 提示的那两行
``` bash
plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  # ...
  autojump
)

# autojump
[[ -s /home/xhinliang/.autojump/etc/profile.d/autojump.sh ]] && source /home/xhinliang/.autojump/etc/profile.d/autojump.sh
autoload -U compinit && compinit -u
```

### 配置舒适的日志记录环境
我习惯使用 VSCode + 坚果云 + Markdown 记日志。
但默认的 Markdown 不支持 PlantUML 的绘制，我们加上插件让他更完美些。
1. 在 VSCode 中安装 markdown preview enhanced 插件
2. `sudo apt-get install graphviz`
3. 下载 plantuml.jar 放到$HOME/cli-utils/jars文件夹并配置 .shrc_software
``` bash
export PLANTUML_JAR="$HOME/cli-utils/jars"
export PATH="$JAVA_HOME/bin:$PLANTUML_JAR:$PATH"
```
4. 安装图床上传工具 [fu](https://github.com/klesh/fu)
```
tar 包编译失败了
源代码编译成功，但是运行失败。。
```
