#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/12'

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

class ClubXywySpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'clubxywy'
    allowed_domains = ['club.xywy.com']
    # start_urls = [
    # 'http://club.xywy.com/list_647_all_2.htm' # 中风
    # 'http://club.xywy.com/list_286_all_2.htm' # 痛风
    # 'http://club.xywy.com/list_284_all_2.htm' # 高血压
    # 'http://club.xywy.com/list_740_all_2.htm' # 颈椎病
    # 'http://club.xywy.com/list_275_all_2.htm' # 糖尿病
    #     ]
    redis_key = 'clubxywy:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"/list_275_all_\d+\.htm$"), follow=True),
        Rule(LinkExtractor(allow=r"http://club\.xywy\.com/question/\d+/\d+\.htm$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//p[@class="fl dib fb"]').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//div[@id="qdetailc"]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answer = response.xpath('//div[@class="pt15 f14 graydeep  pl20 pr20"]').extract()[0]
                item['answer'] = self.filter_tags_blank(answer)
            except Exception as e:
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

