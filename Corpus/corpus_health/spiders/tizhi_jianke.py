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

class JiankeTizhiSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'jianke_tizhi'
    allowed_domains = ['jianke.com']
    # start_urls = [
    # ''  # 血瘀质（搜索）页码1-
    # 'https://search.jianke.com/ask?wd=%E6%B0%94%E8%99%9A&pn=2'  # 气虚 1-67
    # ''  # 特禀质
    # ''  # 湿热质
    # ''  # 痰湿质
    # ''  # 气郁质
    # ''  # 阳虚质
    # ''  # 阴虚质
    #     ]
    redis_key = 'jianke_tizhi:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"//search\.jianke\.com/ask\?wd=%E6%B0%94%E8%99%9A&pn=\d+$"), follow=True),
        Rule(LinkExtractor(allow=r"//www\.jianke\.com/ask/question/931531\d+$"), callback="parse_detail_mongo", follow=False)
    )

    def parse_detail_mongo(self, response):
        print('==============')
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//div[@class="why"]/h1').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//p[@class="pd_txt"]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answer = response.xpath('//div[@class="an_cont"]/dl/dt').extract()[0]
                item['answer'] = self.filter_tags_blank(answer)
            except Exception as e:
                item['answer'] = ''
            print(item)
            # yield item
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
