---
title: ScrapyCrawlSpider拉勾网全站抓取
author: Chen
date: 2019-01-25 17:47:24
top: true
img: http://m.qpic.cn/psb?/V10Lajvl1FgUNv/PPWwoLRM4bzhkfUzCwJU5MdXYSnbp0s9dmORMQAIUDs!/b/dDQBAAAAAAAA&bo=CwU4BAAAAAARBwI!&rf=viewer_4
categories: Python
tags:
  - Python爬虫
  - Scrapy
---

# 数据展示

![数据展示](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/dJPWyOHbTHAkjjbqjRafuNpAoylQIyQKswTjeegFcH8!/b/dLYAAAAAAAAA&bo=yAUWAwAAAAADB*o!&rf=viewer_4)


# 网站分析

## 分析首页

![首页](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/S4KN..H..ModSavlRJ4jqX*wMb0sII20jcpAJEVV77A!/b/dDYBAAAAAAAA&bo=YQd.AwAAAAADNwk!&rf=viewer_4)

首页中有职位的分类,抓取所有的职位,点击进去看职位分类的url

## 分析职位分类

![职位分类](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/RCszUk30b7oFdvndszLE0BIBj5IEI.tjiQoV*rR10qM!/b/dLYAAAAAAAAA&bo=DAbQAwAAAAADJ9s!&rf=viewer_4)

在职位分类的页面下有具体的详情页面

## 分析公司页面
![公司](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/6FlT7RVC0lql6hlza9cbxdvcvFm65rFvvp*xxnPytRY!/b/dL8AAAAAAAAA&bo=dwWJAwAAAAADF8o!&rf=viewer_4)

## 分析职位的详情页面
![详情页面](http://m.qpic.cn/psb?/V10Lajvl1FgUNv/4PC4iH*mIsqMhVqTyg6IONJGBrdXlvWRVRf7oIKPNeg!/b/dDUBAAAAAAAA&bo=ogaRAwAAAAADJzQ!&rf=viewer_4)


进入详情页面获取我们想要的数据

我们的爬虫访问路径,先进入首页,然后匹配职位分类的url,公司的url,以及详情页的url,职位分类和公司的url匹配到之后接着对页面进行跟踪匹配,因为我们做的全站爬虫.

# 编写代码

## 定义Item

根据想获取的数据定义Item

	url# 职位url
	url_object_id职位url对应的id
	title职位名字
	salary薪资水平
	city工作城市
	years工作年限
	degree任职程度
	job_type工作类型
	publish_time发布时间
	tags标签
	job_advantage职位优势
	job_desc职位描述
	job_addr职位地址
	company_url公司官方网站地址
	company_name公司名字
	crawl_time抓取时间
	crawl_update_time抓取更新时间

## 定义根据网站的Url定义CrawlSpider的抓取Rule

	rules = (
	        Rule(LinkExtractor(allow=r'zhaopin/.*', ), follow=True),  # 职位分类
	        Rule(LinkExtractor(allow=r'gongsi/j\d+.html'), follow=True),  # 匹配公司内的招聘职位
	        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),  # 职位详情页面匹配
	    )

## 设置随机请求头

	class UserAgentDownloadMiddleware(object):
	    # 请求头列表
	    USER_AGENT = [
	        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
	        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
	        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931",
	        "Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
	        "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
	        "Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0",
	        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0",
	        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
	        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
	        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
	    ]
	
	    def process_request(self, request, spider):
	        user_agent = random.choice(self.USER_AGENT)  # 随机选择请求头
	        request.headers["User-Agent"] = user_agent  # 给request添加随机请求头

## 详情页的抓取规则

这里使用的Itemloaders填充的Item,使用add_xpath和add_value将值收集到itemloades中.

	    def parse_job(self, response):
	        # 解析拉勾网的职位
	        item_loader = LagouItemLoader(item=LagoujobItem(), response=response)  # 创建ItemLoader的实例
	        item_loader.add_xpath("title", "//div[@class='job-name']//span/text()")  # 职位名字
	        item_loader.add_value("url", response.url)  # 职位url
	        item_loader.add_value("url_object_id", get_md5(response.url))  # 职位url对应的id
	        item_loader.add_xpath("salary",
	                              "//div[@class='position-content-l']/dd[@class='job_request']/p/span[@class='salary']/text()")
	        item_loader.add_xpath("city",
	                              "//div[@class='position-content-l']/dd[@class='job_request']/p/span[2]/text()")  # 工作城市
	        item_loader.add_xpath("years",
	                              "//div[@class='position-content-l']/dd[@class='job_request']/p/span[3]/text()")  # 工作年限
	
	        item_loader.add_xpath("degree",
	                              "//div[@class='position-content-l']/dd[@class='job_request']/p/span[4]/text()")  # 任职程度
	        item_loader.add_xpath("job_type",
	                              "//div[@class='position-content-l']/dd[@class='job_request']/p/span[5]/text()")  # 工作类型
	        item_loader.add_xpath("tags", "//ul[contains(@class,'position-label')]/li/text()")  # 标签,注意有些招聘信息是单个的标签,而有些确实很多的
	
	        item_loader.add_xpath("publish_time", "//p[@class='publish_time']/text()")  # 发布时间,需要进行处理
	        item_loader.add_xpath("job_advantage", "//dd[@class='job-advantage']/p/text()")  # 职位优势
	
	        job_desc_list = response.xpath(
	            "//dd[@class='job_bt']/div[@class='job-detail']/p/text()").getall()  # 职位描述  注意返回的是一个列表,需要进行处理
	        job_desc = ",".join(job_desc_list)
	        item_loader.add_value("job_desc", job_desc)  # 职位描述  注意返回的是一个列表,需要进行处理
	
	        job_addr = response.xpath("//div[@class='work_addr']//text()").getall()  # 职位地址
	        job_addr = ",".join(job_addr)  # 将列表拼接成字符串
	        job_addr = re.sub("-|\n|,| |查看地图", "", job_addr)  # 使用正则做数据处理
	        item_loader.add_value("job_addr", job_addr)  # 职位地址
	
	        item_loader.add_xpath("company_name", "//*[@id='job_company']/dt/a/img/@alt")  # 公司名字
	        item_loader.add_xpath("company_url", "//*[@id='job_company']/dt/a/@href")  # 公司官方网站地址
	        item_loader.add_value("crawl_time", datetime.datetime.now())  # 抓取时间
	
	        job_item = item_loader.load_item()  # 加载Item
	        return job_item

## 使用ItemLoaders进行数据处理
	import scrapy
	from scrapy.loader import ItemLoader
	from scrapy.loader.processors import TakeFirst, MapCompose
	import re
	from w3lib.html import remove_tags  # 这个模块专门用来去除Html中的标签的
	class LagouItemLoader(ItemLoader):
	    default_output_processor = TakeFirst()
	
	
	def process_input_city_and_degree_years(value):
	    # 对输入的城市进行处理
	    value = re.sub("/", "", value).strip()
	    return value
	
	
	def process_input_salary(value):
	    # 对输入的薪水进行处理
	    result = re.sub("k", "000", value).replace("-", ' ').strip()
	    return result
	
	
	def process_input_publish_time(value):
	    # 对输入的发布时间进行处理
	    result = re.sub("\xa0", "", value).strip()
	    return result
	
	def process_input_desc(value):
	    # 职位详情的处理
	    if value == "":
	        return "无"
	    else:
	        return value
	
	
	class LagoujobItem(scrapy.Item):
	    url = scrapy.Field()  # 职位url
	    url_object_id = scrapy.Field()  # 职位url对应的id
	    title = scrapy.Field()  # 职位名字
	    salary = scrapy.Field(
	        input_processor=MapCompose(process_input_salary)
	    )  # 薪资水平
	    city = scrapy.Field(
	        input_processor=MapCompose(process_input_city_and_degree_years),
	    )  # 工作城市
	    years = scrapy.Field(
	        input_processor=MapCompose(process_input_city_and_degree_years),
	    )  # 工作年限
	    degree = scrapy.Field(
	        input_processor=MapCompose(process_input_city_and_degree_years),
	    )  # 任职程度
	    job_type = scrapy.Field()  # 工作类型
	    publish_time = scrapy.Field(
	        input_processor=MapCompose(process_input_publish_time)
	    )  # 发布时间
	    tags = scrapy.Field(
	        input_processor=MapCompose(process_input_desc),
	    )  # 标签
	    job_advantage = scrapy.Field()  # 职位优势
	    job_desc = scrapy.Field(
	        input_processor=MapCompose(process_input_desc),
	    )  # 职位描述
	    job_addr = scrapy.Field()  # 职位地址
	    company_url = scrapy.Field()  # 公司官方网站地址
	    company_name = scrapy.Field()  # 公司名字
	    crawl_time = scrapy.Field()  # 抓取时间
	    crawl_update_time = scrapy.Field()  # 抓取更新时间

## 对url连接进行MD5

	import hashlib
	
	
	def get_md5(url):
	    """
	    将url链接转换成md5
	    :param url:
	    :return:
	    """
	    if isinstance(url, str):
	        url = url.encode("utf-8")       # 设置url的编码为utf-8
	    m = hashlib.md5()
	    m.update(url)
	    return m.hexdigest()

## 使用Twisted进行异步IO插入

当我们处理大量的请求的时候,异步插入要比同步插入速度快很多

	class MysqlTwistedPipeline(object):
	    '''
	    使用Twisted框架完成异步Mysql插入
	    '''
	
	    def __init__(self, dbpool):
	        self.dbpool = dbpool
	
	    @classmethod
	    def from_settings(cls, settings):
	        """
	        读取Scrapy的Setting文件,Scrapy自动调用此方法
	        """
	        # 该字典中的参数名称必须和MySQLdb.connections.Connection类中的参数名称要一致
	        dbparms = dict(
	            host=settings["MYSQL_HOST"],
	            db=settings["MYSQL_DBNAME"],
	            user=settings['MYSQL_USER'],
	            password=settings['MYSQL_PASSWORD'],
	            charset='utf8',
	            cursorclass=MySQLdb.cursors.DictCursor,
	            use_unicode=True,
	        )
	
	        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
	        return cls(dbpool)
	
	    def process_item(self, item, spider):
	        # 使用Twisted将Mysql插入变成异步执行
	
	        query = self.dbpool.runInteraction(self.do_insert, item)
	        query.addErrback(self.handle_error, item, spider)  # 处理异常
	
	    def handle_error(self, failure, item, spider):
	        """
	        该函数用来处理异步插入的异常
	        """
	        print(failure)
	
	    def do_insert(self, cursor, item):
	        # 执行具体的插入
	        insert_sql = """
	            insert into lagoujob(url,url_object_id,title,salary,city,years,degree,job_type,publish_time,tags,job_advantage,job_desc,job_addr,company_url,company_name,crawl_time)
	            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
	                       """
	        cursor.execute(insert_sql,
	                       (item['url'], item['url_object_id'], item['title'], item['salary'], item['city'],
	                        item['years'], item['degree'], item['job_type'], item['publish_time'], item['tags'],
	                        item['job_advantage'],item['job_desc'],item['job_addr'],item['company_url'],item['company_name'],item['crawl_time']))











