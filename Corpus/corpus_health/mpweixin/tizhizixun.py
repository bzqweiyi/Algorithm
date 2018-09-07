#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/3'

__QQ__ = '376205871'

"""

from selenium import webdriver
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
        #微信公众号账号
        self.user = ""
        #公众号密码
        self.password = ""
        #设置要爬取的公众号列表
        self.gzlist = ['体质资讯平台', '炎黄东方']
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        self.weChat_login()
        # 登录之后，通过微信公众号后台提供的微信公众号文章接口爬取文章
        for query in self.gzlist:
            # 爬取微信公众号文章，并存在本地文本中
            print("开始爬取公众号：" + query)
            self.get_content(query)
            print("爬取完成")

    #登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中
    def weChat_login(self):
        #定义一个空的字典，存放cookies内容
        post = {}

        #用webdriver启动谷歌浏览器
        print("启动浏览器，打开微信公众号登录界面")
        driver = webdriver.Chrome(executable_path='./chromedriver')
        #打开微信公众号登录页面
        driver.get('https://mp.weixin.qq.com/')
        #等待5秒钟
        time.sleep(5)
        print("正在输入微信公众号登录账号和密码......")
        #清空账号框中的内容
        driver.find_element_by_xpath("./*//input[@name='account']").clear()
        #自动填入登录用户名
        driver.find_element_by_xpath("./*//input[@name='account']").send_keys(self.user)
        #清空密码框中的内容
        driver.find_element_by_xpath("./*//input[@name='password']").clear()
        #自动填入登录密码
        driver.find_element_by_xpath("./*//input[@name='password']").send_keys(self.password)

        # 在自动输完密码之后需要手动点一下记住我
        print("请在登录界面点击:记住账号")
        time.sleep(10)
        #自动点击登录按钮进行登录
        driver.find_element_by_xpath("./*//a[@class='btn_login']").click()
        # 拿手机扫二维码！
        print("请拿手机扫码二维码登录公众号")
        time.sleep(20)
        print("登录成功")
        #重新载入公众号登录页，登录之后会显示公众号后台首页，从这个返回内容中获取cookies信息
        driver.get('https://mp.weixin.qq.com/')
        #获取cookies
        cookie_items = driver.get_cookies()

        #获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
        for cookie_item in cookie_items:
            post[cookie_item['name']] = cookie_item['value']
        cookie_str = json.dumps(post)
        with open('cookie.txt', 'w+', encoding='utf-8') as f:
            f.write(cookie_str)
        print("cookies信息已保存到本地")

    # 请求url
    def open_url(self, url):
        req = urllib.request.Request(url)
        user_agent = ['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                      'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
                      'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                      'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11']
        userAgent = random.choice(user_agent)
        req.add_header('User-Agent', userAgent)
        response = urllib.request.urlopen(url)
        html = response.read()
        return html

    #爬取微信公众号文章，并存在本地文本中
    def get_content(self, query):
        #query为要爬取的公众号名称
        #公众号主页
        url = 'https://mp.weixin.qq.com'
        #设置headers
        header = {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
            }

        #读取上一步获取到的cookies
        with open('cookie.txt', 'r', encoding='utf-8') as f:
            cookie = f.read()
        cookies = json.loads(cookie)

        #登录之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1849751598，从这里获取token信息
        response = requests.get(url=url, cookies=cookies)
        token = re.findall(r'token=(\d+)', str(response.url))[0]

        #搜索微信公众号的接口地址
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        #搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
        query_id = {
            'action': 'search_biz',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5'
            }
        #打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
        search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
        #取搜索结果中的第一个公众号
        lists = search_response.json().get('list')[0]
        #获取这个公众号的fakeid，后面爬取公众号文章需要此字段
        fakeid = lists.get('fakeid')

        #微信公众号文章接口地址
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        #搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '0',#不同页，此参数变化，变化规则为每页加5
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
            }
        #打开搜索的微信公众号文章列表页
        appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        #获取文章总数
        max_num = appmsg_response.json().get('app_msg_cnt')
        #每页至少有5条，获取文章总的页数，爬取时需要分页爬
        num = int(int(max_num) / 5)
        #起始页begin参数，往后每页加5
        begin = 0
        while num + 1 > 0:
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '{}'.format(str(begin)),
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
                }
            print('正在翻页：--------------',begin)

            #获取每一页文章的标题和链接地址，并写入本地文本中
            query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            fakeid_list = query_fakeid_response.json().get('app_msg_list')
            for item in fakeid_list:
                content_link = item.get('link')
                html = self.open_url(content_link).decode('utf-8')
                # 爬取内容信息
                ul_a = html.find('</h2>')
                ul_b = html.find('<script', ul_a)
                content_html = html[ul_a:ul_b]
                # 清除所有标签，正则匹配所有标签。
                reg = re.compile('<[^>]*>')
                content = reg.sub('', content_html).replace('\n', '').replace(' ', '')
                content_title = item.get('title')
                mysqlData = {'url': content_link, 'content': content, 'title': content_title}
                self.save_mysql(mysqlData)
                # fileName = query+'.txt'
                # with open(fileName, 'a', encoding='utf-8') as fh:
                #     fh.write(content_title+":\n"+content_link+"\n")
                # with open('content/' + content_title + '.txt', 'a', encoding='utf-8') as fc:
                #     fc.write(content)
            num -= 1
            begin = int(begin)
            begin += 5
            time.sleep(2)
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
        #登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中
        # getWeChatText.weChat_login()
        # #登录之后，通过微信公众号后台提供的微信公众号文章接口爬取文章
        # for query in gzlist:
        #     #爬取微信公众号文章，并存在本地文本中
        #     print("开始爬取公众号："+query)
        #     get_content(query)
        #     print("爬取完成")
    except Exception as e:
        print(str(e))
