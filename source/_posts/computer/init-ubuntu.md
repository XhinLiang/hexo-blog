title: 安装 Ubuntu Workstation 之后要做的事儿
date: 2019-1-11
tags: [Ubuntu,Linux]
categories: 计算机
toc: true
---

# 安装 Ubuntu Workstation 之后要做的事儿

![logo](/uploads/new--2000px-Former_Ubuntu_logo.png)
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

Windows 10 安装，先格式化整个硬盘，并将分区表修改为 GPT 格式
使用配置好的 UEFI U盘启动后，在第一个界面 Shift + F10 进入命令行环境：
``` bash
diskpart
clean
convert gpt
```

然后分出 200G 给 Windows 10，Windows 安装程序会自动再分出三个小分区，我们只需要关注其中 100M 的那个 EFI 分区，此分区的文件系统是 FAT32，应该非常好辨认。

### Step 1

Windows 10 顺利安装完成，用 UltraISO（还可以使用别的工具，随意了） 把 Ubuntu 的 ISO 文件写入U盘。
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
