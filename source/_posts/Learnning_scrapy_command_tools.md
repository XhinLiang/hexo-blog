title: Scrapy 的命令行工具
date: 2016-04-17 19:28:29
tags: [Scrapy,Python]
categories: Python
toc: true
---

### 默认设置
系统，用户，项目。优先级从低到高
- 系统`/etc/scrapy.cfg`
- 用户`~/.config/scrapy.cfg`和`~/.scrapy.cfg`
- 项目`./scrapy.cfg`

另外可以通过环境变量来设置

### 默认项目结构
```
scrapy.cfg
myproject/
    __init__.py
    items.py
    pipelines.py
    settings.py
    spiders/
        __init__.py
        spider1.py
        spider2.py
        ...
```

#### 创建项目
```
scrapy startproject myproject
```

#### 创建爬虫
```
scrapy genspider mydomain mydomain.com
```

#### 快速获取响应
```
scrapy fetch --nolog http://www.example.com/some/page.html
```

#### 快速获取响应头
```
scrapy fetch --nolog --headers http://www.example.com/
```

#### 快速在浏览器中打开界面
```
scrapy view http://www.example.com/some/page.html
```

#### 指定一个 Spider 爬取一个指定页面
```
scrapy parse http://www.example.com/ -c parse_item
```

#### 运行一个单独的 Python 文件爬虫
```
scrapy runspider myspider.py
```