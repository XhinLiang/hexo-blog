title: 【译】写下你的第一个 Django 应用 part 1
date: 2016-4-1 16:55:29
tags: [Python,Django]
categories: Python
toc: true
---


让我们从例子学起

通过这个教程，我们就可以简单地完成一个投票应用 应用。

这包含两个部分：
1. 一个关于投票的公共的网站，用户可以查看可以投票的项目，也可以对项目进行投票。

2. 一个后台管理界面，管理员可以增加，修改，删除公共网站里的待投票项目。

我们这里假设你已经在你的电脑中安装了 `Django` 。如果你不确定是否已经安装，可以在 `Terminal` 中输入这行命令：

``` bash
python -c "import django; print(django.get_version())"
```

如果 `Django`已经被安装，这时候你可以看到你安装的 `Django` 版本。如果你没有安装，这里会有提示

```
 “No module named django”
```

这个教程是在 `Django` 1.9 ，`Python` 3.4 中测试的，如果 `Django` 的版本不对，你可以参考以前的版本的教程，或者更新你的 `Django` 版本。如果你还在使用 `Python` 2.7，你可能要对教程里的代码进行一些调整。

[安装 `Django` 看这里](https://docs.djangoproject.com/en/1.9/topics/install/)

### 创建一个工程
如果这是你第一次使用 `Django`，你必须注意一下这些初始化安装动作。就像这个名称一样，你需要一些自动生成的代码来建立一个 `Django` 工程。所谓的 `Django` [工程](https://docs.djangoproject.com/en/1.9/glossary/#term-project)，就是一些 `Django` 设置，数据库设置，`Django` 特有选项和应用特有设置。
> `Django` project -- a collection of settings for an instance of `Django`, including database configuration, `Django`-specific options and application-specific settings.

在你的工作目录中输入这行命令

```
django-admin startproject mysite
```

这行命令会在当前目录生成一个叫做`mysite `的目录。[遇到问题？](https://docs.djangoproject.com/en/1.9/faq/troubleshooting/#troubleshooting-django-admin)

> 注意：
> 你必须避免建立一个名称与现有的 `Python` 或者 `Django` 组件冲突的工程。特别地，你不能建立一个名字为 `Django` 或者 test 的工程（test 是 `Python` 自带的包名）

使用 `tree` 命令查看当前的目录结构：
- mysite/
   - manage.py
   - mysite/
       - __init__.py
       - settings.py
       - urls.py
       - wsgi.py

这些文件的意义如下：

- 根目录`mysite `只是一个你的工程的容器，他的名字对于 `Django` 而言没有任何意义，你可以随意改名。
- manage.py 是一个让你操作你这个 `Django` 工程的命令行工具。[详情](https://docs.djangoproject.com/en/1.9/ref/django-admin/)
- 根目录里的`mysite `目录是你这个工程的真正的 `Python` 包目录。它的名字就是你所需要导入的 `Python` 包名。（如 `mysite.urls`）
- `mysite/__init__.py`是一个空白的 [`Python` 包初始化文件](https://docs.python.org/tutorial/modules.html#packages)。
- `mysite/settings.py` 这个 `Django` 工程的设置文件。[详情](https://docs.djangoproject.com/en/1.9/topics/settings/)
- `mysite/urls.py` 这个文件包含了这个工程的 **URL 定义** 和 **内容列表**。[关于 **URL** 分发](https://docs.djangoproject.com/en/1.9/topics/http/urls/)
- `mysite/wsgi.py` 这个文件是这个 `Django` 工程的兼容服务器网关（WSGI-compatible）的服务器入口。[详情](https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/)。

### 开发环境的测试
让我们验证一下我们新建的 `Django` 工程。在我们的工程根目录中输入这行命令：
```
python manage.py runserver
```
在 `Terminal` 中你可以看到如下输出：

```
Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

March 31, 2016 - 15:50:53
`Django` version 1.9, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
*注意，先忽略这里的数据库迁移警告，我们会很快讨论到它*

你已经启动了 `Django` 的开发环境服务器，一个清亮的 Web 纯 `Python` 服务器。
到这里，我们已经成功导入了 `Django` ，所以我们可以愉快地在这个基础上进行开发了。注意我们这里忽略了生产环境的服务器（例如 `Apache`）设置 -- 当我们准备好要部署的时候再来讨论它。

*注意：不要将这个开发环境的服务器用于任何生产环境*

现在，我们可以访问在浏览器中输入 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  来访问我们刚刚启动的服务器。你会看到 `“Welcome to Django”` 这个界面，证明我们这一步已经完成了。

> **更改启动的端口**
这里 `Django` 默认启动的端口为 8000，如果你想要设置为别的端口，只需要加个参数即可，例如：
> ```
> python manage.py runserver 8080
> ```
> 如果你还想设置启动的 IP ，也很简单：
> ```
> python manage.py runserver 0.0.0.0:8000
> ```
> [更多详情](https://docs.djangoproject.com/en/1.9/ref/django-admin/#django-admin-runserver)。

> **自动重载服务器**
>生产环境的服务器可以自动重载（修改代码后不需要重新启动服务器）。不过有些动作（例如添加文件）不会触发重载，在这种情况，你需要手动重启服务器。

### 创建投票应用
现在我们的生产环境已经设置完毕了，我们的工作可以正式开始了。

按照惯例，每一个 `Django` 应用都是由一个 `Python` 包组成的。`Django` 会自动生成通用的目录结构给我们的应用，所以我们可以把精力集中在业务代码上面。

> **工程和应用**
> 工程和应用的区别是什么呢？一个应用是一个完成一些功能的 Web 应用，例如一个博客，一个储存服务或者是一个投票界面。一个工程是很多应用的集合，用来建设一个网站。一句讲噻，一个工程可以包含很多个应用，一个应用可以被很多个不同的工程同时使用。

我们的应用可以在任何 [`Python` path](https://docs.python.org/tutorial/modules.html#the-module-search-path) 中使用。在这个教程中，我们会在项目的根目录中创建我们的应用，因为这样我们能将它作为我们的 `mysite` 工程的顶级模块。

在我们的根目录中（`manage.py` 所在的目录）执行以下命令：
```
python manage.py startapp polls
```
这回创建我们的 `polls` 应用，结构如下：
-polls/
   - __init__.py
   - admin.py
   - apps.py
   - migrations/
       - __init__.py
   - models.py
   - tests.py
   - views.py

整个投票应用都会在这个目录里。

### 写下第一个 view
打开 `polls/views.py` ，输入以下代码：

```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

这是在 `Django` 里能做到的最简单的 `view` 了。为了获得这个 `view` ，我们需要将它与一个 `URL` 链接起来，所以我们需要 `URLconf`。

为了在 `polls` 文件夹里创建一个 `URLconf` ，我们先创建一个文件 `urls.py` 。现在我们的应用文件树应该是这样的：
- polls/
   - __init__.py
   - admin.py
   - apps.py
   - migrations/
       - __init__.py
   - models.py
   - tests.py
   - urls.py
   - views.py

在刚刚创建的 `polls/urls.py` 里写下这段代码：
```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

下一步就是在根目录里的 URLconf 里添加 polls.urls 这个模块了。
在 mysite/urls.py 里，添加依赖 `django.conf.urls.include` 并在 `urlpatterns` 里插入一个 `include()` 方法。
现在 `mysite/urls.py` 应该是这样的：

```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]
```

这个 `include()` 函数可以导入别的 `URLconfs` 。
注意这里的正在表达式不包含 `$` （正则表达式里的尾匹配），不过这并不代表我们要把尾字符串截掉。在 `Django` 中出现 `include()`，就代表砍掉了 `URL` 前面的部分，留下尾字符串，并把尾字符串传给导入的 `URLconf` 以便做进一步处理。

这个 `include()` 的处理方法让 `URL` 的处理更容易。我们的应用 `polls`在它自己的`URLconf`下，所以他可以不管它前面的路径，例如 `/polls/` 或者 `/fun_polls/` 或者 `/content/polls` 。例如 `google.com/polls/result/1` 它只需要处理后面的部分，`result/1/` 即可，而对于前面的 `google.com/polls/`它完全不需要关心。

> **什么时候使用 `include()`**
> 当我们需要匹配另外一个 URL 模式时，我们就应该使用 `include`。`admin.site.urls` 是唯一的例外

> **不匹配任何模式时会怎样**
> 如果你看到有代码使用`include(admin.site.urls)` 而不是直接 `admin.site.urls` ，这份代码应该是旧版本的，你需要更新你的 `Django` 版本

你现在在你的 `URLconf` 里连接了一个 **index view**，让我们来运行服务器测试一下：
```
python manage.py runserver
```

在浏览器中输入 ` http://localhost:8000/polls/` 来进行测试。
这时候你应该看到一句话:
**"Hello, world. You’re at the polls index."** 
这也是我们之前所定义的。

`url()` 函数接受四个参数，包含两个必要参数和两个可选参数：
#### regex
正则表达式。 `Django` 从第一个正则表达式开始，遍历整个列表，直到找到一个匹配的为止。
注意，这个正则表达式不会搜索 GET 或者 POST 的参数，或者域名。例如`https://www.example.com/myapp/`,  `URLconf` 只会匹配 `myapp/`. 又`https://www.example.com/myapp/?page=3`,  `URLconf` 也是只匹配 `myapp/`.
有关[正则表达式](https://en.wikipedia.org/wiki/Regular_expression)。

#### view
当 `Django` 找到一个匹配的正则表达式， `Django` 会调用一个特定的 `view` 方法，并加上参数 [`HttpRequest`](https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpRequest)
作为第一个参数，在正则表达式中，所有的被捕获的值都将作为参数传给这个方法。如果这个正则使用了简单捕获，所有的值会按位置赋值，如果使用了命名捕获，所有的捕获的值会用作一个键值对赋值。接下来我们会讨论到它。

#### kwargs
人员的关键字参数都可以放到一个字典（`dictionary`）中被传到目标 `view` 中，在这系列教程中，我们不会用到这个特性。

#### name
命名你的 `URL` 让你在任何地方都能更清楚地处理它，特别是在模板中。这个强有力的特性能让你只需要在一个文件稍作改变就能做出全局的 `url` 匹配规则改变。

