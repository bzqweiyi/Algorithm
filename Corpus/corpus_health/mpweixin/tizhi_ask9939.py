#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/3'

__QQ__ = '376205871'

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import pymongo
from datetime import datetime

class getAsk():
    def __init__(self):
        self.url = 'http://zhannei.baidu.com/cse/search?q=%E6%B0%94%E8%99%9A%E8%B4%A8&p='  # qixuzhi  p65
        # self.url = 'http://zhannei.baidu.com/cse/search?q=%E6%B0%94%E9%83%81%E8%B4%A8&p='  # qiyuzhi  p2
        # self.url = 'http://zhannei.baidu.com/cse/search?q=%E6%B9%BF%E7%83%AD%E8%B4%A8&p='  # shirezhi  p73
        # self.url = 'http://zhannei.baidu.com/cse/search?q=%E7%97%B0%E6%B9%BF%E8%B4%A8&p='  # tanshizhi  p51
        # self.url = 'http://zhannei.baidu.com/cse/search?q=%E7%89%B9%E7%A6%80%E8%B4%A8&p='  # tebingzhi  p5
        # self.url = 'http://zhannei.baidu.com/cse/search?q=%E8%A1%80%E7%98%80%E8%B4%A8&p='  # xueyuzhi  p37
        # self.url = 'http://zhannei.baidu.com/cse/search?q=%E9%98%B3%E8%99%9A%E8%B4%A8&p='  # yangxuzhi  p40
        # self.url = 'http://zhannei.baidu.com/cse/search?q=%E9%98%B4%E8%99%9A%E8%B4%A8&p='  # yinxuzhi  p75
        connection = pymongo.MongoClient('mongodb://localhost:27017')
        db = connection['tizhi']
        self.collection = db['qixuzhi']
        for page in range(0, 1):
            url = self.url + str(page) + '&s=11390991775594799180&nsid=0&entry=1'
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
            list = soup.select('#results h3')
            # print(list)
            # print(len(list))
            # print('=============')
            for child in list:
                # print(child)
                alist = child.find_all('a', href=True)
                # print(alist[0]['href'])
                # if 'question' in alist[0]['href']:
                self.getDetail(alist[0]['href'])
        except Exception as e:
            print(e)
        # driver.quit()

    def getDetail(self, url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头参数
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml-xml')
        item = {}
        try:
            askTxt = soup.h1.string
            descTemp = soup.select('.user_ask')[0].find(class_='descip')
            descText = self.filter_tags_blank(str(descTemp))
            print(descText)
            # item['question'] = {'askText': askTxt, 'askDesc': descText}
            # item['answer'] = ''
            # item['url'] = url
            # print(item)
            # self.saveMongo(item)
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
