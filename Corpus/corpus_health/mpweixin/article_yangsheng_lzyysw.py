#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/3'

__QQ__ = '376205871'

"""

from bs4 import BeautifulSoup
import re
import pymongo
from datetime import datetime
import requests
import random

class getAsk():
    def __init__(self):
        self.url = 'http://www.lzyysw.com/zhongyi/list/0/'
        connection = pymongo.MongoClient('mongodb://localhost:27017')
        db = connection['tizhi']
        self.collection = db['article']
        self.user_agent_list = [ \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]
        for page in range(1, 242):
            url = self.url + str(page)
            self.getList(url)

    def getList(self, url):
        print(url)
        try:
            ua = random.choice(self.user_agent_list)
            if ua:
                # print(ua)
                # 设置headers
                header = {
                    "User-Agent": ua
                }
            response = requests.get(url, headers=header)
            html = response.content
            html_doc = str(html, 'utf-8')
            soup = BeautifulSoup(html_doc, 'lxml-xml')
            # print(soup)
            try:
                list = soup.select('ol li')
                # print(list)
                # print(len(list))
                for child in list:
                    alist = child.find_all('a', href=True)
                    detailUrl = 'http://www.lzyysw.com' + alist[0]['href']
                    self.getDetail(detailUrl)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
        # driver.quit()

    def getDetail(self, url):
        try:
            ua = random.choice(self.user_agent_list)
            if ua:
                # print(ua)
                # 设置headers
                header = {
                    "User-Agent": ua
                }
            response = requests.get(url, headers=header)
            html = response.content
            html_doc = str(html, 'utf-8')
            soup = BeautifulSoup(html_doc, 'lxml-xml')
            # print(soup)
            titleTemp = soup.select('#archivesTitle')[0]
            titleTxt = self.filter_tags_blank(str(titleTemp))
            contentTemp = soup.select('#archivesContent')[0]
            contentText = self.filter_tags_blank(str(contentTemp))
            # print(askTxt)
            # print(descText)
            item = {}
            item['title'] = titleTxt
            item['content'] = contentText
            item['url'] = url
            # print(item)
            self.saveMongo(item)
        except Exception as e:
            print(e)

    def saveMongo(self, item):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.collection.update_one(
            {'url': item['url']},
            {
                "$set": {
                    'title': item.get('title'),
                    'content': item.get('content'),
                    'url': item.get('url'),
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
        getAsk()
    except Exception as e:
        print(str(e))
