#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/14'

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

class Ask999120Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'ask999120'
    allowed_domains = ['ask.999120.net']
    # start_urls = [
    # 'http://ask.999120.net/list_830_all/index_50.html' # 高血压
    # 'http://ask.999120.net/list_829_all/index.html' # 冠心病
    # 'http://ask.999120.net/list_831_all/index.html' # 糖尿病
    # 'http://ask.999120.net/list_869_all/index.html' # 脂肪肝
    # 'http://ask.999120.net/list_871_all/index.html' # 高血脂
    # 'http://ask.999120.net/list_766_all/index.html' # 老年痴呆
    # 'http://ask.999120.net/list_883_all/index.html' # 咳嗽
    # 'http://ask.999120.net/list_787_all/index.html' # 痛风
    # 'http://ask.999120.net/list_791_all/index.html' # 颈椎病
    #     ]
    redis_key = 'ask999120:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"http://ask\.999120\.net/list_791_all/index_\d+\.html$"), follow=True),
        Rule(LinkExtractor(allow=r"http://ask\.999120\.net/list_791/\d+/\d+/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//div[@class="title"]/h1').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//div[@class="q_con clear"]/p[@class="txt"]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            # try:
            #     answerList = []
            #     answers = response.xpath('//div[@class="iask_answer02a"]')
            #     for item_each in answers:
            #         answerLi = item_each.xpath('.//dd').extract()[0]
            #         answerList.append(self.filter_tags_blank(answerLi))
            #     item['answer'] = answerList
            # except Exception as e:
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

