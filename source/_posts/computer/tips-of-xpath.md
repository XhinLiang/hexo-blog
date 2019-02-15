title: 【译】XPath 实用技巧
date: 2016-04-17 15:28:29
tags: [Scrapy,Python]
categories: 计算机
toc: true
---


原文链接：[XPath Tips from the Web Scraping Trenches](https://blog.scrapinghub.com/2014/07/17/xpath-tips-from-the-web-scraping-trenches/)

## 简介
在网页抓取的过程中， XPath 是一个很好的工具，因为它可以选择文档里的元素而且比 CSS 选择器更灵活。如果你正在寻找一个教程，这是一个好的选择。

在这篇文章中，我们将向你展示一些我们在使用 XPath 的过程中发现的技巧。


### 考虑使用 text 元素
当你需要使用元素的内容（the text content of Element）作为 XPath 的 [string](http://www.w3.org/TR/xpath/#section-String-Functions) 函数的参数时，考虑使用 `.` 而不是 `.//text()`

这是因为 `.//text()` 表达式生产一个关于元素内容的集合（*node-set*）。当这个集合被转成 string 的时候（例如使用 `contains()`或者`start-with`），他只会返回第一个元素的数据。

举个例子：
```
>>> from scrapy import Selector
>>> sel = Selector(text='<a href="#">Click here to go to the <strong>Next Page</strong></a>')
```

把他转成一个 *node-set* 的 string：
```
>>> sel.xpath('//a//text()').extract() # take a peek at the node-set
[u'Click here to go to the ', u'Next Page']
>>> sel.xpath("string(//a//text())").extract() # convert it to string
[u'Click here to go to the ']
```

直接把一个元素本身的和它的子元素的文本转成 string
```
>>> sel.xpath("//a[1]").extract() # select the first node
[u'<a href="#">Click here to go to the <strong>Next Page</strong></a>']
>>> sel.xpath("string(//a[1])").extract() # convert it to string
[u'Click here to go to the Next Page']
```

所以，使用 `.//text()` 得到的元素集合不会包含任何东西：
```
>>> sel.xpath("//a[contains(.//text(), 'Next Page')]").extract()
[]
```

不过直接使用 `.` 反而可以取到元素：
```
>>> sel.xpath("//a[contains(., 'Next Page')]").extract()
[u'<a href="#">Click here to go to the <strong>Next Page</strong></a>']
```

### 留意 `//node[1]` 和 `(//node)[1]` 的区别
`//node[1]` 在整个文档中选择所有的第一次在他们的父节点出现的元素。
`(//node)[1]` 在整个文档中选择所有的元素，并返回取得的第一个元素。

举个例子，先构造好整个文档：
```
>>> from scrapy import Selector
>>> sel = Selector(text="""
....:     <ul class="list">
....:         <li>1</li>
....:         <li>2</li>
....:         <li>3</li>
....:     </ul>
....:     <ul class="list">
....:         <li>4</li>
....:         <li>5</li>
....:         <li>6</li>
....:     </ul>""")
>>> xp = lambda x: sel.xpath(x).extract()
```

这段代码会获取到所有在他们的父节点中第一次出现的 `<li>` 元素：
```
>>> xp("//li[1]")
[u'<li>1</li>', u'<li>4</li>']
```

这段代码会获取到在整个文档中第一次出现的 `<li>` 元素：
```
>>> xp("(//li)[1]")
[u'<li>1</li>']
```

这段代码会获取到所有的 `<ul>` 元素中第一次出现的 `<li>` 元素：
```
>>> xp("//ul/li[1]")
[u'<li>1</li>', u'<li>4</li>']
```

这段代码会获取到在整个文档中第一个在一个 `<ul>` 元素中出现的 `<li>` 元素（有点绕，慢慢理解）：
```
>>> xp("(//ul/li)[1]")
[u'<li>1</li>']
```

### 当根据 class 来查找元素的时候，考虑使用 CSS
因为一个元素可以包含多重 CSS class，如果使用 XPath 去选择一个元素会显得很累赘：
```
*[contains(concat(' ', normalize-space(@class), ' '), ' someclass ')]
```

如果你在使用形如 `@class='someclass'` 时，你可能会在还有别的 class 的时候结束一个元素。还有，如果你使用 `contains(@class, 'someclass')` 去查找的话，当有两个不同的 class 共享同一个class 名字时，你有可能会获取到比你想要的更多的元素（你获取到的元素不全是你想要的）。

所以， Scrapy 允许你链式使用 `Selector` ，所以在这些情况下，你可以考虑使用 CSS 来选择元素，然后继续使用 XPath （或 CSS ）来进行下一步操作。
```
>>> from scrapy import Selector
>>> sel = Selector(text='<div class="hero shout"><time datetime="2014-07-23 19:00">Special date</time></div>')
>>> sel.css('.shout').xpath('./time/@datetime').extract()
[u'2014-07-23 19:00']
```
这段代码比之前的代码更优雅。
不过，再提醒一下，在接下来的操作中，记得使用 `.` 。