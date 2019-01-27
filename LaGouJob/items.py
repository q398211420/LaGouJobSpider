# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

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


