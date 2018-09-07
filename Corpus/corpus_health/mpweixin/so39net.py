#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/5'

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
from corpus_health import settings

class weChatContent():
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        self.weChat_login()

    def weChat_login(self):

        # service_args = []
        # service_args.append('--load-images=no')  ##关闭图片加载
        # service_args.append('--disk-cache=yes')  ##开启缓存
        # service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
        #
        # d = webdriver.PhantomJS("phantomjs", service_args=service_args)
        # d.get("http://so.39.net/bke?words=%E9%AB%98%E8%A1%80%E5%8E%8B%E9%A5%AE%E9%A3%9F")
        # print(d.page_source)

        path = "http://so.39.net/bke?words=%E9%AB%98%E8%A1%80%E5%8E%8B%E9%A5%AE%E9%A3%9F"
        USER_AGENTS = ['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                      'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
                      'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                      'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11']

        chrome_options = Options()
        chrome_options.add_argument('--headless') # 无头参数
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
        driver.get(path)
        soup = BeautifulSoup(driver.page_source, 'lxml-xml')
        # str = '<ol><li class="normal">高血压吃什么好</li><li class="normal">高血压饮食禁忌那些</li></ol>'
        # soup = BeautifulSoup(str, 'lxml-xml')
        # print(type(soup))
        print(soup.ol)
        print('=============')
        for child in soup.ol:
            print(child)
            print(child.string)
        # print(driver.page_source)
        # driver.quit()

    def save_mysql(self, item):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # 判断表是否存在，不存在则创建表(图片信息表)
            self.cursor.execute(
                """SELECT table_name FROM information_schema.TABLES WHERE table_name ='corpus_wechat';""")
            table_is_none = self.cursor.fetchone()
            if table_is_none is None:
                sql_create = """CREATE TABLE corpus_wechat (
                            id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                            url VARCHAR(1000) NOT NULL,
                            title VARCHAR(500),
                            content VARCHAR(20000),
                            create_time VARCHAR(20),
                            update_time VARCHAR(20))"""
                self.cursor.execute(sql_create)
            self.cursor.execute("""select * from corpus_wechat where url = %s""", item["url"])
            ret = self.cursor.fetchone()
            if ret:
                self.cursor.execute(
                    """update corpus_wechat set title = %s,content = %s,url = %s,update_time = %s
                        where url = %s""",
                    (item['title'],
                     item['content'],
                     item['url'],
                     cur_time,
                     item['url']))
            else:
                self.cursor.execute(
                    """insert into corpus_wechat(title,content,url,create_time,update_time)
                      value (%s,%s,%s,%s,%s)""",
                    (item['title'],
                     item['content'],
                     item['url'],
                     cur_time,
                     cur_time))
            self.connect.commit()
        except Exception as e:
            print("保存数据库出错。错误原因:")
            print(e)

if __name__ == '__main__':
    try:
        weChatContent()
    except Exception as e:
        print(str(e))
