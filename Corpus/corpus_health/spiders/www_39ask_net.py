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

class Www39AskNetSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'www_39ask_net'
    allowed_domains = ['39ask.net']
    # start_urls = [
    # 'https://www.39ask.net/category/view/108/2/1.html' #高血压
    # 'https://www.39ask.net/category/view/112/2/1.html' # 冠心病
    # 'https://www.39ask.net/category/view/53/2/1.html' # 糖尿病
    # 'https://www.39ask.net/category/view/14/2/1.html' # 感冒
    # 'https://www.39ask.net/category/view/251/2/1.html' # 痛风
    # 'https://www.39ask.net/category/view/125/2/1.html' # 颈椎病
    #     ]
    redis_key = 'www_39ask_net:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"https://www\.39ask\.net/category/view/125/2/\d+\.html$"), follow=True),
        Rule(LinkExtractor(allow=r"https://www\.39ask\.net/question/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//h1[@class="four font-16 u_tit"]').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//p[@class="k_questiond"]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = response.xpath('//div[@class="k_answerlist"]/div[@class="k_answerli"]')
                itemList = []
                for index, answerli in enumerate(answerList):
                    answer_each = answerli.xpath('.//div[@class="crazy_new"]').extract()[0]
                    itemList.append(self.filter_tags_blank(answer_each))
                item['answer'] = itemList
            except Exception as e:
                item['answer'] = ''
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


