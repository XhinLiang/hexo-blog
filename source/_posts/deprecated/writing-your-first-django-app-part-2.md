title: 【译】写下你的第一个 Django 应用 part 2
date: 2016-4-2 10:25:29
tags: [Python,Django]
categories: Python
toc: true
---


### 设置数据库
现在，编辑你的 `mysite/settings.py`，这是一个课业设置模块级别的变量的普通 `Python` 模块。

`Django`使用`SQLite`作为默认的数据库，如果你只对`Django`感兴趣，这是最好的选择。`SQLite`包含在`Python`里，所以你不需要安装任何东西来支持你的数据库。当你真正开启你的项目的时候，你可能需要更加鲁棒的数据库，例如`PostgreSQL`，来避免一些在数据库中令人头痛的问题。

如果你想要使用另外的数据库，请先安装相对应的[数据库支持包](https://docs.djangoproject.com/en/1.9/topics/install/#database-installation)并在`DATABASES 'default'`中修改键值。
- `ENGINE`：数据库支持包，如`django.db.backends.sqlite3`或者 `django.db.backends.postgresql`或者`django.db.backends.mysql`或者`django.db.backends.oracle`，[更多](https://docs.djangoproject.com/en/1.9/ref/databases/#third-party-notes)
- `NAME`：你的数据库的名字，如果你在使用`SQLite`，数据库仅仅是你电脑上的一个文件，这时`NAME`应该是这个数据库文件的绝对地址（包含文件的名字）。如果你不作修改，`os.path.join(BASE_DIR'db.sqlite3')`会是你默认的设置。

如果你使用另外的数据库，就必须添加一些额外的设置信息，例如`USER``PASSWORD``HOST`等等。[更多](https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-DATABASES)。

> **给使用另外数据库的人**
> 如果你在使用另外的数据库，请确认你已经创建了数据库，例如`CREATE DATABASE datebase_name`等等。
> 还有，确认`mysite/settings.py`有**创建数据库**的权限，这些权限我们接下来会使用到。
> 如果你在使用`SQLite`，你不需要额外创建任何东西，数据库的文件在它需要被创建的时候已经准备妥当。

当你在修改`mysite/settings.py`文件是，在`TIME_ZONE`设置你当前的时区。

这时候，把注意力集中到`INSTALLED_APPS`的设置上。这个设置持有了所有这个项目中需要的`Django`应用。一个`Django`应用可以被不同的项目使用，你可以在不同的项目中随意打包和分配。

默认地，`INSTALLED_APPS`包含了以下的应用，他们都来自`Django`:
- [`django.contrib.admin`](https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#module-django.contrib.admin) 管理界面，你很快会看到它
- [`django.contrib.auth`](https://docs.djangoproject.com/en/1.9/topics/auth/#module-django.contrib.auth) 认证系统
- [`django.contrib.contenttypes`](https://docs.djangoproject.com/en/1.9/ref/contrib/contenttypes/#module-django.contrib.contenttypes) 关于内容类型的框架
- [`django.contrib.sessions`](https://docs.djangoproject.com/en/1.9/topics/http/sessions/#module-django.contrib.sessions) Session框架
- [`django.contrib.messages`](https://docs.djangoproject.com/en/1.9/ref/contrib/messages/#module-django.contrib.messages) 消息传送框架
- [`django.contrib.staticfiles`](https://docs.djangoproject.com/en/1.9/ref/contrib/staticfiles/#module-django.contrib.staticfiles) 静态文件框架
为了使用上的方便这些应用默认会被包含。

以上的有些应用会使用至少一个数据库表，所以，在使用他们之前，我们需要在数据库中创建表：
```
python manage.py migrate
```

这个`migrate`命令会查看`INSTALLED_APPS`设置并根据你的`mysite/setting`中的设置创建所需要的数据库表，并完成数据库的迁移。你可以看到每一条迁移的消息。

> 给最小需求者
> 就想我们所说的，默认的应用已经被包含到工程里，不过不是每一个工程都需要他们，如果你不需要他们中的一个或者多个，你可以在执行`migrate`命令之前把他（们）在`INSTALLED_APPS`中删掉。

### 创建模型
在`polls/models.py`文件中添加如下代码
``` python
import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

@python_2_unicode_compatible  # only if you need to support Python 2
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
```
这段代码就像我一样耿直，所有的模型都是 `django.db.models.Model`的子类，每个模型都有他自己的变量，每个变量都代表了一个数据库字段。

每个字段都由一个[`Field`](https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.Field)类型来表示，例如`CharField`用来表示字符串字段`DateTimeField`用来表示时间字段。这些都是用来告诉`Django`每个字段持有的类型的。

每个`Field`实例的名字（例如`question_text``pub_date`）就是一个字段的名字，使用机器友好的格式。在这里我们使用`Python`代码，相应的数据库会使用他们的列的名字。

在`Field`的构造方法中，可以添加可选的首个参数，这个参数用来指定一个人类可读的名字。这被`Django`在内部使用，并在文档中有所展现。如果这个字段没有被提供，`Django`会使用一个机器可读的名字。在这个例子中，我们只给`Question.pub_date`声明了一个人类可读的名字。其他的字段都只有机器可读的名字，这些机器可读的名字会同时作为他们的人类可读的名字。

一些`Field`类的构造函数需要参数，例如`CharField`，需要一个`max_length`参数，这不仅仅会在数据库的计划中被使用，还会用来确认，我们很快就会看到它。

一个`Field`当然也可以有可选参数，这里，我们把`vote`的`default`数值设为0

最后，我们使用`ForeignKey`定义了`Choice`和`Question`的一对一关系。`Django`支持所有的数据库关系：多对一，一对一，多对多。

### 让你的 model 生效
很少的`model`的`Python`代码就可以给`Django`很多信息：
- 给应用创建一个数据库模式（`CREATE TABLE`声明）
- 给`Question`和`Choice`创建一个数据库连接的 API 。

不过我们首先需要告诉工程我们的`polls`应用已经被安装。

修改`mysite/settings.py`文件，在`INSTALLED_APPS`当中添加一行，看起来就像这样：
```
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
现在`Django`已经添加了`polls`这个应用，我们通过这行命令来进行数据库的迁移：
```
python manage.py makemigrations polls
```
你可以看到如下的输出：
```
Migrations for 'polls':
  0001_initial.py:
    - Create model Choice
    - Create model Question
    - Add field question to choice
```
通过执行`makemigrations`命令，`Django`就能根据你的 Model 的改变而做出多方面的调整。

你可以通过这条指令看到`Django`对上一条指令执行的`SQL`代码：
```
python manage.py sqlmigrate polls 0001
```
接下来你可以在`Terminal`中看到类似的输出：
```
BEGIN;
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" serial NOT NULL PRIMARY KEY,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL
);
--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" serial NOT NULL PRIMARY KEY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
--
-- Add field question to choice
--
ALTER TABLE "polls_choice" ADD COLUMN "question_id" integer NOT NULL;
ALTER TABLE "polls_choice" ALTER COLUMN "question_id" DROP DEFAULT;
CREATE INDEX "polls_choice_7aa0f6ee" ON "polls_choice" ("question_id");
ALTER TABLE "polls_choice"
  ADD CONSTRAINT "polls_choice_question_id_246c99a640fbbd72_fk_polls_question_id"
    FOREIGN KEY ("question_id")
    REFERENCES "polls_question" ("id")
    DEFERRABLE INITIALLY DEFERRED;

COMMIT;
```
注意：
- 这个输出取决于你所使用的数据库。
- 表的名字会自动转成小写（你可以修改这个行为）
- 主键会自动加上（可以修改这个行为）
- 关联属性会自动加上`_id`（可以修改这个行为）
- 关联属性会被明确指明`FOREIGN KEY`的约束，不要担心`DEFERRABLE`这个部分，这只是告诉`PostgreSQL`在这段事务结束之前不要执行关联属性键。
- 这行命令不会真正执行这些`SQL`指令。

你可以执行这行命令来检查不进行数据库迁移（不执行下面这行命令）是否会有问题：
```
python manage.py check
```

一切完毕之后，执行这行指令来进行数据库迁移：
```
python manage.py migrate
```


你会看到如下的输出：
```
Operations to perform:
  Apply all migrations: admin, contenttypes, polls, auth, sessions
Running migrations:
  Rendering model states... DONE
  Applying polls.0001_initial... OK
```

这个`migrate`命令会做好所有未执行的数据库迁移操作，还会造好所有的数据库更新操作。

总而言之，我们就进行了三步操作：
- 更新 Models
- 执行`python manage.py makemigrations`
- 执行`python manage.py migrate`

### 完成你的管理界面
首先我们需要创建一个超级用户：
```
python manage.py createsuperuser
```
然后按照提示进行操作即可，

然后我们编辑`polls/admin.py`文件，输入以下代码：
```
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

现在我们来运行服务器：
```
python manage.py runserver
```

这时候我们可以通过`/admin/`来访问我们的管理界面，例如`http://127.0.0.1:8000/admin/`

你可以看到如下的管理界面
![Alt text](/uploads/writing-your-first-django-app/admin01.png)

登陆之后，你就可以随意在管理界面玩耍了
![Alt text](/uploads/writing-your-first-django-app/admin02.png)
![Alt text](/uploads/writing-your-first-django-app/admin02.png)
![Alt text](/uploads/writing-your-first-django-app/admin03t.png)
![Alt text](/uploads/writing-your-first-django-app/admin04t.png)
![Alt text](/uploads/writing-your-first-django-app/admin05t.png)
![Alt text](/uploads/writing-your-first-django-app/admin06t.png)



