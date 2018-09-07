#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/5'

__QQ__ = '376205871'

"""
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import MedicineItem
from scrapy_redis.spiders import RedisCrawlSpider
import urllib.parse
from math import floor
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)

class Ypk39net(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'ypk39net'
    allowed_domains = ['ypk.39.net']
    # start_urls = [
    #     'http://ypk.39.net/search/%E9%AB%98%E8%A1%80%E5%8E%8B-c2-p1/',
    #     'http://ypk.39.net/search/%E9%AB%98%E8%84%82%E8%A1%80%E7%97%87-c2-p1/'
    #     'http://ypk.39.net/search/%E7%B3%96%E5%B0%BF%E7%97%85-c2-p1/'
    # 'http://ypk.39.net/search/%E8%84%82%E8%82%AA%E8%82%9D-c2-p1/'
    # 'http://ypk.39.net/search/%E5%86%A0%E5%BF%83%E7%97%85-c2-p1/'
    # 'http://ypk.39.net/search/%E4%B8%AD%E9%A3%8E-c2-p1/'
    # 'http://ypk.39.net/search/%E7%97%B4%E5%91%86-c2-p1/'
    # 'http://ypk.39.net/search/%E6%98%93%E6%82%A3%E6%84%9F%E5%86%92-c2-p1/'
    # 'http://ypk.39.net/search/%E6%85%A2%E6%80%A7%E5%92%B3%E5%97%BD-c2-p1/'
    # 'http://ypk.39.net/search/%E9%A2%88%E6%A4%8E%E7%97%85-c2-p1/'
    # 'http://ypk.39.net/search/%E8%85%B0%E8%85%BF%E7%96%BC-c2-p1/'
    # 'http://ypk.39.net/search/%E7%97%9B%E9%A3%8E-c2-p1/'
    #     ]
    redis_key = 'ypk39net:start_urls'

    rules = (
        # Rule(LinkExtractor(allow=r"/search/高血压\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/高脂血症\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/糖尿病\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/脂肪肝\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/冠心病\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/中风\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/痴呆\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/易患感冒\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/慢性咳嗽\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/颈椎病\-c2\-p\d+/$"), follow=True),
        # Rule(LinkExtractor(allow=r"/search/腰腿疼\-c2\-p\d+/$"), follow=True),
        Rule(LinkExtractor(allow=r"/search/痛风\-c2\-p\d+/$"), follow=True),
        Rule(LinkExtractor(allow=r"/\d+/$"), callback="parse_help_mongo", follow=False),
        # Rule(LinkExtractor(allow=r"/\d+/manual$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail(self, response):
        pass

    def parse_help_mongo(self, response):
        item = MedicineItem()
        try:
            cureDiseaseArr = []
            item['url'] = response.url + 'manual'
            itemList = response.xpath('//ul[contains(@class, "whatsthis")]/li')
            for itemLi in itemList:
                cureDiseaseArr.append(itemLi.xpath('.//text()').extract()[0])
            # item['cureDisease'] = cureDiseaseArr
            # yield item
            yield scrapy.Request(item['url'], meta={'cureDisease': cureDiseaseArr}, callback=self.parse_detail_mongo)
        except Exception as e:
            print(e)
            logger.info("匹配信息出错。错误原因:")
            logger.info(e)

    def parse_detail_mongo(self, response):
        item = MedicineItem()
        # name = Field()  # 名称
        # ChemicalComposition = Field()  # 化学成分
        # Indication = Field()  # 适应症
        # Usage = Field()  # 用法用量
        # Contraindication = Field()  # 禁忌
        # SpecialDrugUse = Field()  # 特殊人群用药
        # PeriodOfValidity = Field()  # 有效期
        # Pharmacology = Field()  # 药物相互作用,药理
        try:
            item['url'] = response.url
            item['name'] = response.xpath('//h1/a[@target="_self"]/text()').extract()[0]
            chemicalComposition = response.xpath('//div[@class="tab_box"]/div/dl[2]/dd').extract()[0]
            item['chemicalComposition'] = self.filter_tags_blank(chemicalComposition)
            indicationArr = response.xpath('//div[@class="tab_box"]/div/dl[3]/dd').extract()[0]
            item['indication'] = self.filter_tags_blank(indicationArr)
            usage = response.xpath('//div[@class="tab_box"]/div/dl[4]/dd').extract()[0]
            item['usage'] = self.filter_tags_blank(usage)
            contraindication = response.xpath('//div[@class="tab_box"]/div/dl[6]/dd').extract()[0]
            item['contraindication'] = self.filter_tags_blank(contraindication)
            specialDrugUseArr = response.xpath('//div[@class="tab_box"]/div/dl[8]/dd').extract()[0]
            item['specialDrugUse'] = self.filter_tags_blank(specialDrugUseArr)
            periodOfValidityArr = response.xpath('//div[@class="tab_box"]/div/dl[12]/dd').extract()[0]
            item['periodOfValidity'] = self.filter_tags_blank(periodOfValidityArr)
            pharmacologyArr = response.xpath('//div[@class="tab_box"]/div/dl[10]/dd').extract()[0]
            item['pharmacology'] = self.filter_tags_blank(pharmacologyArr)
            item['cureDisease'] = response.meta['cureDisease']
            yield item
        except Exception as e:
            print(e)
            logger.info("匹配信息出错。错误原因:")
            logger.info(e)


    """
    去掉html标签和空格
    """
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())

