#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/12'

__QQ__ = '376205871'

"""

import pymongo
import re
from datetime import datetime

class MongodbFilter(object):
    def __init__(self):
        # 本地mongodb
        connection = pymongo.MongoClient('mongodb://localhost:27017')
        self.collection = connection['article']['info_tnb39net']

        connection_notag = pymongo.MongoClient('mongodb://192.168.1.15:27017')
        self.collection_notag = connection_notag['article_notag']['info']
        self.getMongodb()


    # 过滤script标签及里面内容 iframe
    def filterTags(self, htmlstr):
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_script_s = re.compile('<(script).*?>[\s\S]*?<\/script>', re.I)   # Script标签里含有script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_iframe = re.compile('<\s*iframe[^>]*>[^<]*<\s*/\s*iframe\s*>', re.I)  # iframe
        re_br = re.compile('<br\s*?/?>')  # 处理换行
    #     re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        re_a = re.compile('</?a[^>]*>')   # a标签
        blank_line = re.compile('\n+')  # 多余空行

        # 过滤匹配内容
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_script_s.sub('', s)  # 去掉SCRIPT和里面的SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_iframe.sub('', s)  # 去掉iframe
        s = re_br.sub('\n', s)  # 将br转换为换行
    #     s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        s = re_a.sub('', s)     # 去掉a标签保留内容
        s = blank_line.sub('\n', s)  # 去掉多余的空行
        return s


    def getMongodb(self):
        # result = self.collection.find().skip(0).limit(1)
        # content = result[0]["content"]
        # print(content)
        # print('====================')
        # filterResult = self.filterTags(content)
        # print(filterResult)

        resultsCount = self.collection.count()
        for skipNum in range(0, resultsCount, 200):
            results = self.collection.find().skip(skipNum).limit(200)
            print(skipNum)
            for result in results:
                filterResult = self.filter_tags_blank(result['content'])
                result['content'] = filterResult
                self.saveMongodb(result)


    def saveMongodb(self, item):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.collection_notag.update_one(
                {'url': item['url']},
                {
                    "$set": {
                        'title': item.get('title'),
                        'content': item.get('content'),
                        'url': item.get('url'),
                        'category': item.get('category'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        except Exception as e:
            print("======保存出错=====")
            print(e)


    # 去掉html标签和空格
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())


if __name__ == '__main__':
    try:
        MongodbFilter()
    except Exception as e:
        print(str(e))
