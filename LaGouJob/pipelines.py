# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.exporters import JsonLinesItemExporter
from twisted.enterprise import adbapi
import MySQLdb.cursors


class LagoujobPipeline(object):
    def __init__(self):
        self.fileProject = open("LaGou.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.fileProject, ensure_ascii=False, encoding="utf-8")

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fileProject.close()

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