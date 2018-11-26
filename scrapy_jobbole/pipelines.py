# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines import images
import json
import codecs
from scrapy.exporters import JsonItemExporter
import MySQLdb
from MySQLdb import cursors
from twisted.enterprise import adbapi


# pipeline主程序，暂时没有任何功能
class ScrapyJobbolePipeline(object):
    def process_item(self, item, spider):
        return item


# pipeline图像保存程序
class AtricleItemImagePipeline(images.ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path
        return item


# JSON保存pipeline
class JsonSavePipeline(object):
    def __init__(self):
        # 通过codecs打开文件
        self.file = codecs.open('article.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        # 将item读取为JSON形式字符串
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# JSON使用JsonExplorer保存的pipeline
class JsonExplorterPipeline(object):
    def __init__(self):
        # 调用scrapy提供的json_explorter方法到处json文件
        self.file = open('artile_explorter.json', 'wb')
        self.explorter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.explorter.start_exporting()

    def process_item(self, item, spider):
        # 将item读取为JSON形式字符串
        self.explorter.export_item(item)
        return item

    def spider_closed(self, spider):
        # 关闭导出器和文件
        self.explorter.finish_exporting()
        self.file.close()


# 使用MySql保存Item数据的pipeline
class ItemSaveMySqlPipeline(object):
    # init方法中初始化链接以及cursor
    def __init__(self):
        # 初始化链接参数，charset设置utf8，use_unicode设置为True
        self.conn = MySQLdb.connect('localhost', 'root', '50122294', 'jobbole_article', charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 写sql语句
        insert_sql = '''
            insert into article_scrapy(title,url,create_date,enjoy)
            VALUES(%s,%s,%s,%s)
        '''
        # 进行查询
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['enjoy']))
        # 提交事务
        self.conn.commit()
        return item


# 使用Mysql异步保存Item数据的pipeline
class ItemSaveTwistedPipeline(object):
    # 初始化连接池
    def __init__(self, dbpool):
        self.dbpool = dbpool
        pass

    # 默认方法，获取settings中数据库相关链接配置，并初始化连接池
    @classmethod
    def from_settings(cls, settings):
        # 连接参数
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        # 初始化连接池，param1:数据库驱动程序，param2：链接参数
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    # 异步插入
    def process_item(self, item, spider):
        # 调用连接池do_insert方法，将item数据插入
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 错误异常方法
        query.addErrback(self.handle_error, item, spider)
        return item

    # 处理异常方法
    def handle_error(self, failure, item, spider):
        print(failure)

    # 数据插入方法
    def do_insert(self, cursor, item):
        # 写sql语句
        insert_sql = '''
                   insert into article_scrapy(title,url,create_date,enjoy)
                   VALUES(%s,%s,%s,%s)
               '''
        # 进行查询
        cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['enjoy']))
        # 使用twisted异步提交，不需要commit
