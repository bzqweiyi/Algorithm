#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/4'

__QQ__ = '376205871'

字段说明：
    # name            食物名称
    # foodPic         食物图片
    # alias           别名
    # category        分类
    # message         信息（评价建议信息）
    # nutritionTags   营养信息标签（标签[tag]，每100单位含量[content]）
    # nutritionUnit   营养信息单位（每100单位: 克，毫升）
    # widgetUnit      度量单位（度量单位[widget]，热量[energy]）
    # material        材料
    # practice        做法

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
        self.url = 'http://www.boohee.com/food/view_menu?page=1'
        connection = pymongo.MongoClient('mongodb://localhost:27017')
        db = connection['food']
        self.collection = db['info']
        self.collectionUrl = db['food_url']
        self.collectionSearch = db['food_search']
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

        # 列表数据
        # for cate in range(1, 11):
        #     for page_a in range(1, 11):
        #         url_a = 'http://www.boohee.com/food/group/' + str(cate) + '?page=' + str(page_a)
        #         # print(url_a)
        #         self.getList(url_a)
        # for page_b in range(1, 11):
        #     url_b = 'http://www.boohee.com/food/view_menu?page=' + str(page_b)
        #     # print(url_b)
        #     self.getList(url_b)


        # 搜索数据
        resultsCount = self.collection.count()
        for skipNum in range(2660, resultsCount, 100):
            results = self.collection.find().skip(skipNum).limit(100)
            print(skipNum)
            # results = self.collection.find().skip(1300).limit(200)
            for result in results:
                for page_c in range(1, 11):
                    searchUrl = 'http://www.boohee.com/food/search?keyword=' + result['name'] + '&page=' + str(page_c)
                    # print(searchUrl)
                    resultSearch = self.collectionSearch.find_one({'searchUrl': searchUrl})
                    if resultSearch == None:
                        self.getList(searchUrl, result['name'])

        # 原料数据(通过存储原料的url到food_url集合，然后爬去url里的内容)
        # resultsCount = self.collectionUrl.count()
        # for skipNum in range(0, resultsCount, 200):
        #     results = self.collectionUrl.find().skip(skipNum).limit(200)
        #     print(skipNum)
        #     for result in results:
        #         resultUrl = self.collection.find_one({'url': result['url']})
        #         if resultUrl == None:
        #             self.getDetail(result['url'])


        # self.getList(self.url_b)
        # self.getDetail('http://www.boohee.com/shiwu/shaoqiezi')
        # self.getDetail('http://www.boohee.com/shiwu/chaoqingcai')
        # self.getDetail('http://www.boohee.com/shiwu/mantou_junzhi')

    def getList(self, url, foodName):
        print(url)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头参数
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml-xml')
        try:
            lists = soup.find_all('ul', class_="food-list")[0]
            list = lists.find_all('li')
            cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.collectionSearch.update_one(
                {'searchUrl': url},
                {
                    "$set": {
                        'searchUrl': url,
                        'name': foodName,
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
            for child in list:
                alist = child.find_all('a', href=True)
                detailUrl = 'http://www.boohee.com' + alist[0]['href']
                # print(detailUrl)
                resultUrl = self.collection.find_one({'url': detailUrl})
                if resultUrl == None:
                    self.getDetail(detailUrl)
        except Exception as e:
            print(e)
            # driver.quit()

    def getDetail(self, url):
        print(url)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头参数
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml-xml')
        # print(soup)
        item = {
            'url': url,
            'name': '',
            'foodPic': '',
            'alias': '',
            'category': '',
            'message': {
                'title': '',
                'info': ''
            },
            'nutritionTags': [],
            'nutritionUnit': '',
            'widgetUnit': [],
            'material': [],
            'practice': ''
        }
        # 名称、分类
        try:
            headTemp = soup.find_all('ul', class_="basic-infor ")[0]
            nameTemp = soup.find_all('h2', class_="crumb")[0]
            item['name'] = self.filter_tags_blank(str(nameTemp)).split('/')[-1]
            item['foodPic'] = soup.find_all('div', class_="food-pic pull-left")[0].find_all('a', href=True)[0]['href']
            for eachLi in headTemp.find_all('li'):
                if '别名：' in eachLi.select("b")[0].string:
                    item['alias'] = self.filter_tags_blank(str(eachLi)).replace('别名：', '')
                if '分类：' in eachLi.select("b")[0].string:
                    item['category'] = self.filter_tags_blank(str(eachLi)).replace('分类：', '')
        except Exception as e:
            print('=====mingcheng======')
            print(e)

        # 备注信息
        try:
            mTemp = soup.find_all("div", class_="widget-food-detail pull-left")[0]
            msgContent = mTemp.find_all("div", class_="content", recursive=False)[0]
            messageHtml = msgContent.find_all("p", recursive=False)[0]
            item['message']['title'] = messageHtml.find_all("b", recursive=False)[0].string.split('：')[0]
            item['message']['info'] = self.filter_tags_blank(str(messageHtml).split('</b>')[1])
            # print(item)
        except Exception as e:
            print('====beizhu=====')
            print(e)

        # 营养信息
        try:
            nutr = soup.find_all('div', class_="nutr-tag margin10")[0]
            nutrContent = nutr.find_all('div', class_="content")[0]
            list = nutrContent.find_all('dl')
            # print(list)
            nutrTags = []
            for index, ddList in enumerate(list):
                if index:
                    for each in ddList.find_all('dd'):
                        nutrTag = {}
                        tag = each.find_all('span', class_="dt")[0]
                        nutrTag['tag'] = self.filter_tags_blank(str(tag))
                        content = each.find_all('span', class_="dd")[0]
                        nutrTag['content'] = self.filter_tags_blank(str(content))
                        nutrTags.append(nutrTag)
                else:
                    nutrUnit = ddList.find_all('span', class_="dd", limit=1)[0].string
            item['nutritionTags'] = nutrTags
            item['nutritionUnit'] = nutrUnit.split('(')[1].split(')')[0]
            # print(item)
        except Exception as e:
            print('=======yingyang======')
            print(e)

        # 度量单位
        try:
            widget = soup.find_all('div', class_="widget-unit")[0]
            tbody = widget.find_all('tbody')[0]
            tr = tbody.find_all('tr')
            unitEnergy = []
            for index, trList in enumerate(tr):
                unit = {}
                widgetUnit = trList.find_all('td')[0]
                unit['widget'] = self.filter_tags_blank(str(widgetUnit))
                energy = trList.find_all('td')[1]
                unit['energy'] = self.filter_tags_blank(str(energy))
                unitEnergy.append(unit)
            item['widgetUnit'] = unitEnergy
            # print(item)
        except Exception as e:
            print('=========duliang=======')
            print(e)

        # 原料（如果有）、做法
        try:
            widgetMore = soup.find_all('div', class_="widget-more")[0]
            ulContent = widgetMore.find_all('ul')
            content = widgetMore.find_all('div', class_="content")
            material = []
            for eachUl in ulContent:
                liMore = eachUl.find_all('li')
                for moreLi in liMore:
                    # print(moreLi)
                    tempLi = {}
                    tempUrl = 'http://www.boohee.com' + moreLi.find_all('a', href=True)[0]['href']
                    # print(tempUrl)
                    cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.collectionUrl.update_one(
                        {'url': tempUrl},
                        {
                            "$set": {
                                'url': tempUrl,
                                'update_time': cur_time
                            }
                        },
                        upsert=True
                    )
                    tempLi['name'] = moreLi.find_all('a')[0].string
                    tempLi['weight'] = self.filter_tags_blank(str(moreLi).split('</a>')[1])
                    material.append(tempLi)
            item['material'] = material
            for contentLi in content:
                pHtml = contentLi.find_all('p')
                if len(pHtml):
                    item['practice'] = self.filter_tags_blank(str(pHtml[0]))
        except Exception as e:
            print('=======yuanliao======')
            print(e)
        # print(item)
        self.saveMongo(item)

    def saveMongo(self, item):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.collection.update_one(
            {'url': item['url']},
            {
                "$set": {
                    'name': item.get('name'),
                    'foodPic': item.get('foodPic'),
                    'alias': item.get('alias'),
                    'category': item.get('category'),
                    'message': item.get('message'),
                    'nutritionTags': item.get('nutritionTags'),
                    'nutritionUnit': item.get('nutritionUnit'),
                    'widgetUnit': item.get('widgetUnit'),
                    'material': item.get('material'),
                    'practice': item.get('practice'),
                    'url': item.get('url'),
                    'update_time': cur_time
                }
            },
            upsert=True
        )
        self.collectionUrl.update_one(
            {'url': item['url']},
            {
                "$set": {
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
