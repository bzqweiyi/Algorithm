#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/6'

__QQ__ = '376205871'

"""

import requests
import json
import pymongo
from corpus_health import settings
from datetime import datetime
import re

class spiderAskDxy(object):
    def __init__(self):
        self.url = 'https://ask.dxy.com/view/i/question/list/section'
        connection = pymongo.MongoClient(settings.MONGODB_URI)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]
        for item in range(617):
            self.payload = {'section_group_name': 'xinxueguannei', 'page_index': (item+1)}
            self.getContent()

    def getContent(self):
        r = requests.get(self.url, params=self.payload)
        rObj = json.loads(r.text)
        items = rObj['data']['items']
        for item in items:
            data = []
            for dialog in item['dialogs']:
                data_each = {}
                # print(dialog['id'], '\n')
                # print(dialog['question_id'], '\n')
                # print(self.filter_tags_blank(dialog['content']), '\n')
                data_each['id'] = dialog['id']
                data_each['question_id'] = dialog['question_id']
                data_each['content'] = self.filter_tags_blank(dialog['content'])
                if dialog['type']:
                    data_each['type'] = 'answer'
                else:
                    data_each['type'] = 'question'
                data.append(data_each)
            # print(data)
            self.saveMongo(data)

    def saveMongo(self, item):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.collection.update_one(
            {'question_id': item[0]['question_id']},
            {
                "$set": {
                    'dialogs': item,
                    'update_time': cur_time
                }
            },
            upsert=True
        )

    """
    去掉html标签和空格
    """
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())

if __name__ == '__main__':
    try:
        spiderAskDxy()
    except Exception as e:
        print(str(e))
