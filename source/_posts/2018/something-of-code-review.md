title: Code Review 二三事
date: 2018-5-29 22:26:29
tags: [生活,随笔]
categories: 生活
toc: true
---

最近对 Code Review 这套流程有比较多的想法，不吐不快。

首先 Code Review 属于 “结对编程” 的一种实现，而且是一种比较高效的实现。

在快手的 Server 端，Code Review 是一个不可或缺的工作流程，主要因为这几个原因：

- 快手开发节奏很快，但鉴于目前整套自动化测试设施不够完善，可能很多代码修改过后没有经过测试就直接上线了，这非常考验一次性写对代码的能力。
- 团队对代码质量的要求很高，需要做到按照团队的代码规范做到 Clean Code，而 CheckStyle 不能把代码规范全部覆盖到，所以有些 Style 需要人工来检查。
- Code Review 能让至少另一个工程师知道这个代码改动，在工程师层面有一个备份。

服务端开发和客户端开发对 Code Review 的诉求可能不太一样。
因为通常不能在开发机本地进行运行，服务端的代码错误一般暴露得会更晚一些，所以一般希望能够尽量早地发现问题，而 Code Review 就是中间非常重要的一环。



Code Review 注意以下几点：

第一，Code Review 发出前，先自己给自己 Code Review 一遍，这个工作可以通过 Git diff 完成，也可以通过 Code Review 工具完成。
这点非常重要，自己都没看过，就让别人看，是一个非常不礼貌的行为，会浪费别人的时间。
而且更需要强调的一点是，不要把别人的 ship 当做测试通过的标志，**Code Review 不是 Reviewer 给你的挡箭牌**
有些工程师拿到 reviewer 的 ship 之后，觉得这已经是测试通过了，可以对代码进行发布了，其实这是本末倒置。
**Code Review 并不是让 Reviewer 帮你背锅**

第二，**Code Review 不是熟悉业务代码，不能走马观花！**
Code Review 目的是今早发现问题，而提 Review 的工程师既然已经自己检查过了，那么走马观花的 Code Review 自然是不能发现问题的。Code Review 需要非常仔细非常仔细地去读每一行代码，甚至一些 Typo 也需要注意到。
曾经有一次我自己提了一次 Code Review，这次修改把一个需要用 authorId 的地方误用了 visitorId，自己没发现问题，Reviewer 也没发现问题，测试也没发现问题（量太小体现不出来），等到上线之后才发现问题再回滚。
上线回滚大家都不希望发生，那么这样的问题该如何避免呢？其实只要 Code Review 的时候细心一点就能发现了。

第三，每一个 Code Review 的内容要尽量内聚，最好不要把好几个方向的修改放到同一个 Code Review 中。
因为 Code Review 会占用另外一位工程师的相当大一部分的时间，如果对同时好几个方向的修改（例如某个 Code Review 中包含了 数据库配置添加 && 某个任务的超时重试功能 && 某个文件的命名修改），Reviewer 会需要更多的时间来理解这个代码，同时浪费不必要的沟通时间。

末了，我们使用的 Code Review 工具是 GitLab + ReviewBoard。
