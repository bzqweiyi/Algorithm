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
import requests
import random

class getAsk():
    def __init__(self):
        # self.url = 'http://search.999ask.com/cse/search?q=%E6%B0%94%E8%99%9A&p='  # qixu  p75==a
        # self.url = 'http://search.999ask.com/cse/search?q=%E6%B0%94%E8%99%9A%E8%B4%A8&p='  # qixuzhi  p29==a
        # self.url = 'http://search.999ask.com/cse/search?q=%E6%B0%94%E9%83%81%E8%B4%A8&p='  # qiyuzhi  p2==a
        # self.url = 'http://search.999ask.com/cse/search?q=%E6%B9%BF%E7%83%AD%E8%B4%A8&p='  # shirezhi  p41==a
        # self.url = 'http://search.999ask.com/cse/search?q=%E7%97%B0%E6%B9%BF%E8%B4%A8&p='  # tanshizhi  p4==a
        self.url = 'http://search.999ask.com/cse/search?q=%E8%A1%80%E7%98%80%E8%B4%A8&p='  # xueyuzhi  p14==a
        # self.url = 'http://search.999ask.com/cse/search?q=%E9%98%B3%E8%99%9A%E8%B4%A8&p='  # yangxuzhi  p40==a
        # self.url = 'http://search.999ask.com/cse/search?q=%E9%98%B4%E8%99%9A%E8%B4%A8&p='  # yinxuzhi  p54==a
        # self.url = 'http://search.999ask.com/cse/search?q=%E5%B9%B3%E5%92%8C%E8%B4%A8&p='  # pinghezhi  p11==a

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
        self.collection = db['xueyuzhi']
        # 页码从0开始
        for page in range(0, 15):
            url = self.url + str(page) + '&s=8139610519760641621&nsid=2&entry=1'
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
            for child in list:
                alist = child.find_all('a', href=True)
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
            askTemp = soup.find_all(class_='ask_article_title_p1', limit=1)[0]
            askTxt = self.filter_tags_blank(str(askTemp))
            descTemp = soup.find_all(class_='ask_article_nr1_p2', limit=1)[0]
            descText = self.filter_tags_blank(str(descTemp))
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            item['url'] = url
            item['answer'] = ''
            try:
                list = soup.find_all('div', class_="main_l")[0]
                lists = list.find_all('div', class_="ask_answer_border1 ask_answer_content")
                itemList = []
                for child in lists:
                    answers = child.find_all('div', class_="answer_content2")
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


        # chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 无头参数
        # chrome_options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver.get(url)
        # soup = BeautifulSoup(driver.page_source, 'lxml-xml')
        # item = {}
        # try:
        #     askTemp = soup.find_all(class_='ask_article_title_p1', limit=1)[0]
        #     askTxt = self.filter_tags_blank(str(askTemp))
        #     descTemp = soup.find_all(class_='ask_article_nr1_p2', limit=1)[0]
        #     descText = self.filter_tags_blank(str(descTemp))
        #     item['question'] = {'askText': askTxt, 'askDesc': descText}
        #     item['answer'] = ''
        #     item['url'] = url
        #     print(item)
        #     self.saveMongo(item)
        # except Exception as e:
        #     print(e)

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
