# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi

import pymysql



class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ElasticsearchPipeline(object):

    def process_item(self,item,spider):
        item.save_to_es()

        return item
class MysqlPipline(object):
    def __init__(self, dbconn):
        self.dbconn = dbconn

    @classmethod
    def from_settings(cls, settings):
        dbconn = pymysql.connect(settings["MYSQL_HOST"], settings["MYSQL_USER"], settings["MYSQL_PASSWORD"], settings["MYSQL_DBNAME"],charset='utf8')

        return cls(dbconn)

    def process_item(self, item, spider):


        with self.dbconn.cursor()as cursor:
            insert_sql, params = item.get_insert_sql()
            result = cursor.execute(insert_sql,params)

        self.dbconn.commit()


