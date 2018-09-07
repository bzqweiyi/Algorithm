#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/7'

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

class Ask9939Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'ask_9939'
    allowed_domains = ['ask.9939.com']
    # start_urls = [
    # 'http://ask.9939.com/disease/34' #高血压
    # 'http://ask.9939.com/disease/562' #原发性高血压
    # 'http://ask.9939.com/disease/36'  # 冠心病
    # 'http://ask.9939.com/disease/104'  # 劲椎病
    # 'http://ask.9939.com/disease/161'  # 脂肪肝
    # 'http://ask.9939.com/disease/177'  # 腰腿疼
    # 'http://ask.9939.com/disease/132'  # 中风
    # 'http://ask.9939.com/disease/45'  # 高血脂
    # 'http://ask.9939.com/disease/43'  # 糖尿病
    # 'http://ask.9939.com/disease/50'  # 痛风
    # 'http://ask.9939.com/disease/78'  # 感冒
    # 'http://ask.9939.com/disease/464'  # 咳嗽
    #     ]
    redis_key = 'ask_9939:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"/disease/34\-\d+/$"), follow=True),
        Rule(LinkExtractor(allow=r"http://ask\.9939\.com/id/\d+$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//h1').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//div[@class="descip"]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = response.xpath('//div[@class="dorawer"]/div[@class="descip paint1"]').extract()
                itemList = []
                for index, answerli in enumerate(answerList):
                    itemList.append(self.filter_tags_blank(answerli))
                item['answer'] = itemList
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
