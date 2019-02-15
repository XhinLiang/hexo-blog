title: 在 macOS 中使用命令行打开 VSCode
date: 2019-02-15
tags: [工具,macOS,MAC,OSX]
categories: 计算机
toc: true
---

VSCode 相信已经是大家的必备编辑器了，轻量，免费。
在 Linux 环境中， VSCode 可以通过图标启动，也可以通过命令行启动。
例如，我想在 VSCode 中打开这个文件夹，可以这样：
``` bash
$ code someCodeProject
```

但是在 macOS 下默认是不能操作的，因为没有 `code` 这个程序。
我们可以伪造一个：

``` bash
$ cat code
#!/bin/bash

TARGET_DIR="."
if [ -n "$1" ]; then
	TARGET_DIR="$1"
fi
nohup /Applications/Visual\ Studio\ Code.app/Contents/MacOS/Electron $TARGET_DIR > /dev/null 2>&1 &
```

然后，把 `code` 所在的目录加入到 `PATH` 环境变量中，即可。
