#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/5'

__QQ__ = '376205871'

"""

import pymysql
import pymongo
from datetime import datetime

class MongodbToMysql(object):
    def __init__(self):
        MYSQL_HOST = 'localhost'
        MYSQL_DBNAME = 'healthdata'
        MYSQL_USER = 'root'
        MYSQL_PASSWD = '123456'
        # 链接mysql
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        # 链接mongodb
        types = {
            'jingzhuibing': 10001,
            'kesou': 10002,
            'gaoxueya': 10003,
            'gaoxuezhi': 10004,
            'tangniaobing': 10005,
            'zhifanggan': 10006,
            'guanxinbing': 10007,
            'zhongfeng': 10008,
            'chidai': 10009,
            'ganmao': 10010,
            'yaotuiteng': 10011,
            'tongfeng': 10012,
            'yangxuzhi': 10013,
            'yinxuzhi': 10014,
            'qixuzhi': 10015,
            'shirezhi': 10016,
            'qiyuzhi': 10017,
            'tanshizhi': 10018,
            'tebingzhi': 10019,
            'xueyuzhi': 10020,
            'pinghezhi': 10021
        }
        connection = pymongo.MongoClient('mongodb://localhost:27017')
        db = connection['tizhi']
        self.collection = db['pinghezhi']
        self.typeId = types['pinghezhi']
        self.getMongodb()

    def getMongodb(self):
        resultsCount = self.collection.count()
        for skipNum in range(0, resultsCount, 200):
            results = self.collection.find().skip(skipNum).limit(200)
            print(skipNum)
            for result in results:
                self.saveMysql(result)

        # for skipNum in range(0, 100, 20):
        #     results = self.collection.find().skip(skipNum).limit(20)
        #     # print(skipNum)
        #     for result in results:
        #         # print(result)
        #         self.saveMysql(result)

    def saveMysql(self, item):
        try:
            cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute(
                """insert into question_desc(type_id,title,question_desc,url,create_time,update_time)
                  value (%s,%s,%s,%s,%s,%s)""",
                (self.typeId,
                 item['question']['askText'],
                 item['question']['askDesc'],
                 item['url'],
                 cur_time,
                 cur_time))
            q_id = self.cursor.lastrowid
            # print(self.cursor.lastrowid)

            if isinstance(item['answer'], str):
                self.cursor.execute(
                    """insert into answer_desc(question_id,answer_desc,url,create_time,update_time)
                      value (%s,%s,%s,%s,%s)""",
                    (q_id,
                     item['answer'],
                     item['url'],
                     cur_time,
                     cur_time))
            elif isinstance(item['answer'], list):
                for each in item['answer']:
                    self.cursor.execute(
                        """insert into answer_desc(question_id,answer_desc,url,create_time,update_time)
                          value (%s,%s,%s,%s,%s)""",
                        (q_id,
                         each,
                         item['url'],
                         cur_time,
                         cur_time))
            else:
                self.cursor.execute(
                    """insert into answer_desc(question_id,answer_desc,url,create_time,update_time)
                      value (%s,%s,%s,%s,%s)""",
                    (q_id,
                     '',
                     item['url'],
                     cur_time,
                     cur_time))

            # self.cursor.execute(
            #     """UPDATE answer_desc as a, question_desc as q SET a.question_id = q.question_id WHERE q.url=a.url""")
            self.connect.commit()
        except Exception as e:
            print('======保存myqsl出错=======')
            print(e)

if __name__ == '__main__':
    try:
        MongodbToMysql()
    except Exception as e:
        print(str(e))
