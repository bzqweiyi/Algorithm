#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/3'

__QQ__ = '376205871'

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time
import json
import requests
import re
import random
import urllib.request
import urllib.response
import pymysql
import pymongo
from datetime import datetime

class getAsk():
    def __init__(self):
        # self.url = 'http://so.120ask.com/?kw=%E6%B0%94%E8%99%9A&nsid=1&page='  # qixu  p76==
        self.url = 'http://so.120ask.com/?kw=%E6%B0%94%E8%99%9A%E8%B4%A8&nsid=1&page='  # qixuzhi  p76==
        # self.url = 'http://so.120ask.com/?kw=%E6%B0%94%E9%83%81&nsid=1&page='  # qiyu  p76==
        # self.url = 'http://so.120ask.com/?kw=%E6%B0%94%E9%83%81%E8%B4%A8&nsid=1&page='  # qiyuzhi  p53==
        # self.url = 'http://so.120ask.com/?kw=%E6%B9%BF%E7%83%AD%E8%B4%A8&nsid=1&page='  # shirezhi  p76==

        # self.url = 'http://so.120ask.com/?kw=%E7%97%B0%E6%B9%BF%E8%B4%A8&nsid=1&page='  # tanshizhi  p76==a
        # self.url = 'http://so.120ask.com/?kw=%E7%89%B9%E7%A6%80%E8%B4%A8&nsid=1&page='  # tebingzhi  p68==a
        # self.url = 'http://so.120ask.com/?kw=%E8%A1%80%E7%98%80%E8%B4%A8&nsid=1&page='  # xueyuzhi  p76==a
        # self.url = 'http://so.120ask.com/?kw=%E9%98%B3%E8%99%9A%E8%B4%A8&nsid=1&page='  # yangxuzhi  p76==a
        # self.url = 'http://so.120ask.com/?kw=%E9%98%B4%E8%99%9A%E8%B4%A8&nsid=1&page='  # yinxuzhi  p76==a
        # self.url = 'http://so.120ask.com/?kw=%E5%B9%B3%E5%92%8C%E8%B4%A8&nsid=1&page='  # pinghezhi  p64==a

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

        connection = pymongo.MongoClient('mongodb://localhost:27017')
        db = connection['tizhi']
        self.collection = db['qixuzhi']
        # 页码从1开始
        for page in range(1, 77):
            url = self.url + str(page)
            self.getList(url)

    def getList(self, url):
        print(url)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头参数
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml-xml')
        try:
            list = soup.select('#datalist li h3')
            for child in list:
                alist = child.find_all('a', href=True)
                if 'question' in alist[0]['href']:
                    self.getDetail(alist[0]['href'])
        except Exception as e:
            print(e)
        # driver.quit()

    def getDetail(self, url):
        try:
            ua = random.choice(self.user_agent_list)
            if ua:
                # 设置headers
                header = {
                    "User-Agent": ua
                }
            response = requests.get(url, headers=header)
            html = response.content
            html_doc = str(html, 'utf-8')
            soup = BeautifulSoup(html_doc, 'lxml-xml')
            item = {}
            askTxt = soup.find_all(id='d_askH1', limit=1)[0].string
            descTemp = soup.select('#d_msCon')[0].find(class_='crazy_new')
            descText = self.filter_tags_blank(str(descTemp))
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            item['url'] = url
            item['answer'] = ''
            try:
                list = soup.find_all('div', class_="b_answerbox t10")[0]
                lists = list.find_all('div', class_="b_answerli")
                itemList = []
                for child in lists:
                    answers = child.find_all('div', class_="b_anscont_cont")
                    for each in answers:
                        itemList.append(self.filter_tags_blank(str(each)))
                        item['answer'] = itemList
            except Exception as e:
                item['answer'] = ''
                print(e)
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
                    'question': item.get('question'),
                    'answer': item.get('answer'),
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
