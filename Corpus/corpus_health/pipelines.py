# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymongo
import os
import urllib
from datetime import datetime
import re
from urllib import parse
from scrapy.exceptions import DropItem

from corpus_health import settings
from corpus_health.items import CorpusHealthItem
from corpus_health.items import MedicineItem
from corpus_health.items import NewsItem

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=False)

class CorpusHealthPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if item.__class__ == CorpusHealthItem:
            try:
                # 判断表是否存在，不存在则创建表(图片信息表)
                self.cursor.execute("""SELECT table_name FROM information_schema.TABLES WHERE table_name ='corpus_120ask';""")
                table_is_none = self.cursor.fetchone()
                if table_is_none is None:
                    sql_create = """CREATE TABLE corpus_120ask (
                                id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                                url VARCHAR(100) NOT NULL,
                                question VARCHAR(500),
                                answer VARCHAR(2000),
                                create_time VARCHAR(20),
                                update_time VARCHAR(20))"""
                    self.cursor.execute(sql_create)
                self.cursor.execute("""select * from corpus_120ask where url = %s""", item["url"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update corpus_120ask set question = %s,answer = %s,url = %s,update_time = %s
                            where url = %s""",
                        (item['question'],
                         item['answer'],
                         item['url'],
                         cur_time,
                         item['url']))
                else:
                    self.cursor.execute(
                        """insert into corpus_120ask(question,answer,url,create_time,update_time)
                          value (%s,%s,%s,%s,%s)""",
                        (item['question'],
                         item['answer'],
                         item['url'],
                         cur_time,
                         cur_time))
                self.connect.commit()
            except Exception as e:
                logger.info("保存数据库出错。错误原因:")
                logger.info(e)
            return item
        else:
            pass

class MongoCorpusHealthPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings.MONGODB_URI)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for data in item:
            if not data:
                raise DropItem("Missing {0}".format(data))
        self.collection.update_one(
            {'url': item['url']},
            {
                "$set": {
                    'question': item.get('question'),
                    'answer': item.get('answer'),
                    'url': item.get('url'),
                    'update_time': cur_time
                }
            },
            upsert=True
        )
        return item

class MongoMedicinePipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings.MONGODB_URI)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for data in item:
            if not data:
                raise DropItem("Missing {0}".format(data))
        self.collection.update_one(
            {'ApprovalNumber': item['ApprovalNumber']},
            {
                "$set": {
                    'Url': item.get('Url'),
                    'ImgUrl': item.get('ImgUrl'),
                    'DosageForm': item.get('DosageForm'),
                    'Specifications': item.get('Specifications'),
                    'PrescribedDrug': item.get('PrescribedDrug'),
                    'ApprovalNumber': item.get('ApprovalNumber'),
                    'ApprovalDate': item.get('ApprovalDate'),
                    'DrugNames': item.get('DrugNames'),
                    'Composition': item.get('Composition'),
                    'Indications': item.get('Indications'),
                    'DosageAndAdministration': item.get('DosageAndAdministration'),
                    'AdverseReactions': item.get('AdverseReactions'),
                    'Contraindications': item.get('Contraindications'),
                    'Precautions': item.get('Precautions'),
                    'SpecialDrugUse': item.get('SpecialDrugUse'),
                    'Interactions': item.get('Interactions'),
                    'PharmacologicalActions': item.get('PharmacologicalActions'),
                    'Storage': item.get('Storage'),
                    'Validity': item.get('Validity'),
                    'RevisionDate': item.get('RevisionDate'),
                    'ManufacturingEnterprise': item.get('ManufacturingEnterprise'),
                    "DrugCategory": item.get("DrugCategory"),
                    "DrugProperties": item.get("DrugProperties"),
                    "MedicalInsurance": item.get("MedicalInsurance"),
                    'update_time': cur_time
                }
            },
            upsert=True
        )
        return item

class MongoNewsPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings.MONGODB_URI)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for data in item:
            if not data:
                raise DropItem("Missing {0}".format(data))
        self.collection.update_one(
            {'url': item['url']},
            {
                "$set": {
                    'title': item.get('title'),
                    'content': item.get('content'),
                    'category': item.get('category'),
                    'url': item.get('url'),
                    'update_time': cur_time
                }
            },
            upsert=True
        )
