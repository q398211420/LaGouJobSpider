# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from LaGouJob.items import LagouItemLoader  # 使用ItemLoader存储Item
from LaGouJob.items import LagoujobItem
from LaGouJob.utils.common import get_md5  # urlMd5的处理
import re
from scrapy.http import Request

class LagouSpider(CrawlSpider):
    name = 'LaGou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    # start_urls = ['https://www.lagou.com/jobs/3597508.html']

    rules = (
        Rule(LinkExtractor(allow=r'zhaopin/.*', ), follow=True),  # 职位分类Java,产品经理......
        Rule(LinkExtractor(allow=r'gongsi/j\d+.html'), follow=True),  # 匹配公司内的招聘职位
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),  # 职位详情页面匹配
    )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,cookies={"Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6":"1548161370",
                                       "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6":"1548124098,1548136685",
                                       "index_location_city":"%E5%85%A8%E5%9B%BD",
                                       "login":"true",
                                       "sajssdk_2015_cross_new_user":"1",
                                       "showExpriedIndex":"1",
                                       "showExpriedMyPublish":"1",
                                       "unick":"Coder",
                                       "user_trace_token":"20190122102816"
                                       })

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

        # title = response.xpath("//div[@class='job-name']//span/text()").get()  # 职位名字
        # salary = response.xpath(
        #     "//div[@class='position-content-l']/dd[@class='job_request']/p/span[@class='salary']/text()").get()  # 薪资水平
        # city = response.xpath(
        #     "//div[@class='position-content-l']/dd[@class='job_request']/p/span[2]/text()").get()  # 工作城市
        # years = response.xpath(
        #     "//div[@class='position-content-l']/dd[@class='job_request']/p/span[3]/text()").get()  # 工作年限
        # degree = response.xpath(
        #     "//div[@class='position-content-l']/dd[@class='job_request']/p/span[4]/text()").get()  # 任职程度
        #
        # job_type = response.xpath(
        #     "//div[@class='position-content-l']/dd[@class='job_request']/p/span[5]/text()").get()  # 工作类型
        # tags_list = response.xpath(
        #     "//ul[contains(@class,'position-label')]/li/text()").getall()  # 标签,注意有些招聘信息是单个的标签,而有些确实很多的
        # # 对职位的标签进行处理
        # tags = ",".join(tags_list)
        #
        # publish_time = response.xpath("//p[@class='publish_time']/text()").get()  # 发布时间
        # publish_time.replace('\xa0', "").strip().replace(' ', '')  # 对职位的发布时间进行处理
        # job_advantage = response.xpath("//dd[@class='job-advantage']/p/text()").get()  # 职位优势
        #
        # job_addr = response.xpath("//div[@class='work_addr']//text()").getall() # 职位地址
        # job_addr = ",".join(job_addr)   # 将列表拼接成字符串
        # job_addr = re.sub("-|\n|,| |查看地图", "", job_addr)     # 使用正则做数据处理
        # company_name = response.xpath("//*[@id='job_company']/dt/a/img/@alt").get() # 公司名字
        # company_url = response.xpath("//*[@id='job_company']/dt/a/@href").get() # 公司官方网站地址
