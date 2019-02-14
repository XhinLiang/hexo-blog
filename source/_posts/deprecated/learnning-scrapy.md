title: Scrapy 入门
date: 2016-04-17 13:28:29
tags: [Scrapy,Python]
categories: Python
toc: true
---

### 创建一个名为 project_name 的项目
```
scrapy startproject project_name
```

### 定义 Item 
Item 使用方法与 Python 的字典类似，提供了额外保护机制避免拼写和未定义字段错误。

``` Python
class Example_Item(scrapy.Item):
    field_name = scrapy.Field()
    second_name = scrapy.Field()
```

### 创建爬虫
创建的爬虫需要放在 project_name/spiders 目录下。
```
vim project_name/spider_name.py
```

```
import scrapy

class Spider_name(scrapy.Spider):
    # 这里定义了爬虫的名字，下一步会用到
    name = "spider_name"
    # 允许爬取的域名
    allowed_domains = ["example.com"]
    # 开始爬取的页面
    start_urls = [
        "http://www.example.com/list"
    ]

    # 这里是具体的爬取逻辑
    def parse(self, response):
```

### 开始爬
```
scrapy crawl spider_name
```


### 选择器
#### XPath 表达式示例
- `/html/head/title` 选择一个元素 
- `/html/head/title/text()` 选择一个标签内的文字
- `//td` 选择所有的`td`元素
- `//div[@link="fine"]` 选择一个具有特定属性的元素

#### XPath 嵌套
```
# 在根目录中选择一个 doc 元素
doc = response.xpath('/doc')[0]
divs = doc.xpath('div')
divs_same = doc.xpath('./div')
all_divs_in_doc = doc.xpath('.//div')
all_in_doc = doc.xpath('//div')
for item in divs:
    print(item.xpath('./li/a/text()').extract_first())
```

#### 正则
```
>>> from scrapy import Selector
>>> doc = """
... <div>
...     <ul>
...         <li class="item-0"><a href="link1.html">first item</a></li>
...         <li class="item-1"><a href="link2.html">second item</a></li>
...         <li class="item-inactive"><a href="link3.html">third item</a></li>
...         <li class="item-1"><a href="link4.html">fourth item</a></li>
...         <li class="item-0"><a href="link5.html">fifth item</a></li>
...     </ul>
... </div>
... """
>>> sel = Selector(text=doc, type="html")
>>> sel.xpath('//li//@href').extract()
[u'link1.html', u'link2.html', u'link3.html', u'link4.html', u'link5.html']
>>> sel.xpath('//li[re:test(@class, "item-\d$")]//@href').extract()
[u'link1.html', u'link2.html', u'link4.html', u'link5.html']
>>>
```

#### Set
```
>>> doc = """
... <div itemscope itemtype="http://schema.org/Product">
...   <span itemprop="name">Kenmore White 17" Microwave</span>
...   <img src="kenmore-microwave-17in.jpg" alt='Kenmore 17" Microwave' />
...   <div itemprop="aggregateRating"
...     itemscope itemtype="http://schema.org/AggregateRating">
...    Rated <span itemprop="ratingValue">3.5</span>/5
...    based on <span itemprop="reviewCount">11</span> customer reviews
...   </div>
...
...   <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
...     <span itemprop="price">$55.00</span>
...     <link itemprop="availability" href="http://schema.org/InStock" />In stock
...   </div>
...
...   Product description:
...   <span itemprop="description">0.7 cubic feet countertop microwave.
...   Has six preset cooking categories and convenience features like
...   Add-A-Minute and Child Lock.</span>
...
...   Customer reviews:
...
...   <div itemprop="review" itemscope itemtype="http://schema.org/Review">
...     <span itemprop="name">Not a happy camper</span> -
...     by <span itemprop="author">Ellie</span>,
...     <meta itemprop="datePublished" content="2011-04-01">April 1, 2011
...     <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
...       <meta itemprop="worstRating" content = "1">
...       <span itemprop="ratingValue">1</span>/
...       <span itemprop="bestRating">5</span>stars
...     </div>
...     <span itemprop="description">The lamp burned out and now I have to replace
...     it. </span>
...   </div>
...
...   <div itemprop="review" itemscope itemtype="http://schema.org/Review">
...     <span itemprop="name">Value purchase</span> -
...     by <span itemprop="author">Lucas</span>,
...     <meta itemprop="datePublished" content="2011-03-25">March 25, 2011
...     <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
...       <meta itemprop="worstRating" content = "1"/>
...       <span itemprop="ratingValue">4</span>/
...       <span itemprop="bestRating">5</span>stars
...     </div>
...     <span itemprop="description">Great microwave for the price. It is small and
...     fits in my apartment.</span>
...   </div>
...   ...
... </div>
... """
>>> sel = Selector(text=doc, type="html") # 生成 Selector 对象
>>> for scope in sel.xpath('//div[@itemscope]'): # 遍历每个含有 itemscope 属性的 div 元素
...     print "current scope:", scope.xpath('@itemtype').extract() # 先把这个元素的 itemtype 属性打印出来
...     props = scope.xpath(''' # 利用集合抓取元素
...                 set:difference(./descendant::*/@itemprop, # 这里暂时看不懂
...                                .//*[@itemscope]/*/@itemprop)''') # 选择一个含有 itemscope 属性的元素，再选择他的含有 itemprop 属性的元素
...     print "    properties:", props.extract()
...     print
...
```

```
current scope: [u'http://schema.org/Product']
    properties: [u'name', u'aggregateRating', u'offers', u'description', u'review', u'review']

current scope: [u'http://schema.org/AggregateRating']
    properties: [u'ratingValue', u'reviewCount']

current scope: [u'http://schema.org/Offer']
    properties: [u'price', u'availability']

current scope: [u'http://schema.org/Review']
    properties: [u'name', u'author', u'datePublished', u'reviewRating', u'description']

current scope: [u'http://schema.org/Rating']
    properties: [u'worstRating', u'ratingValue', u'bestRating']

current scope: [u'http://schema.org/Review']
    properties: [u'name', u'author', u'datePublished', u'reviewRating', u'description']

current scope: [u'http://schema.org/Rating']
    properties: [u'worstRating', u'ratingValue', u'bestRating']

>>>
```

#### Selector 方法
- `xpath()` 传入一个 XPath 表达式，返回一个 selector list。
- `css()` 同上，但是传入的是 CSS 表达式。
- `extract()` 序列化节点，返回list。
- `re()` 传入正则表达式进行提取，返回 unicode 的 list。

### Selector Shell
```
scrapy shell "http://www.example.com"
```
得到一个 `response` 变量。

### 嵌套选择器示例
```
for sel in response.xpath('//ul/li'):
    title = sel.xpath('a/text()').extract()
    link = sel.xpath('a/@href').extract()
    print title, link
```


### 将爬取的数据返回

```
import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = Example_Item()
            item['title'] = sel.xpath('a/text()').extract_first()
            item['link'] = sel.xpath('a/@href').extract_first()
            item['desc'] = sel.xpath('text()').extract_first()
            yield item
```

### 追踪链接
注意看 `start_urls` 的部分
```
import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(response.url, href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
```

### 更常见的一遍爬取一遍追踪
```
def parse_articles_follow_next_page(self, response):
    for article in response.xpath("//article"):
        item = ArticleItem()

        ... extract article data here

        yield item

    next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
    if next_page:
        url = response.urljoin(next_page[0].extract())
        yield scrapy.Request(url, self.parse_articles_follow_next_page)
```

### 保存爬取到的数据为 JSON 格式
```
scrapy crawl spider_name -o items.json
```


