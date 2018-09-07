#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/5'

__QQ__ = '376205871'

"""

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import CorpusHealthItem
from scrapy_redis.spiders import RedisCrawlSpider
import urllib.parse
from math import floor
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)

class HaodfSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'haodf'
    allowed_domains = ['haodf.com']
    # start_urls = [
    # 'https://so.haodf.com/index/search?kw=%E8%A1%80%E7%98%80%E8%B4%A8&page=1'  # 血瘀质（搜索）页码1-100
    # 'https://so.haodf.com/index/search?kw=%E6%B0%94%E8%99%9A%E8%B4%A8&page='  # 气虚质
    # 'https://so.haodf.com/index/search?kw=%E7%89%B9%E7%A6%80%E8%B4%A8&page='  # 特禀质
    # 'https://so.haodf.com/index/search?kw=%E6%B9%BF%E7%83%AD%E8%B4%A8&page='  # 湿热质
    # 'https://so.haodf.com/index/search?kw=%E7%97%B0%E6%B9%BF%E8%B4%A8&page='  # 痰湿质
    # 'https://so.haodf.com/index/search?kw=%E6%B0%94%E9%83%81%E8%B4%A8&page='  # 气郁质
    # 'https://so.haodf.com/index/search?kw=%E9%98%B3%E8%99%9A%E8%B4%A8&page='  # 阳虚质
    # 'https://so.haodf.com/index/search?kw=%E9%98%B4%E8%99%9A&page='  # 阴虚质
    #     ]
    redis_key = 'haodf:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"//www\.haodf\.com/wenda/[a-zA-Z0-9_]+_g_\d+\.htm$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//h1[contains(@class, "fyahei")]').extract()[0]
            askTxt = self.filter_tags_blank(question)
            descText = ''
            # try:
            #     desc = response.xpath('//p[@class="pd_txt"]').extract()[0]
            #     descText = self.filter_tags_blank(desc)
            # except Exception as e:
            #     descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            # try:
            #     answer = response.xpath('//div[@class="an_cont"]/dl/dt').extract()[0]
            #     item['answer'] = self.filter_tags_blank(answer)
            # except Exception as e:
            #     item['answer'] = ''
            item['answer'] = ''
                # print(item)
            # print(item['answer'])
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
