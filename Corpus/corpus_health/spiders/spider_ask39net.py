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
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)

class Ask39NetSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'ask39net'
    allowed_domains = ['ask.39.net']
    # start_urls = [

    # 'http://ask.39.net/news/17-2.html' # 高血压 142000

    # 'http://ask.39.net/browse/17-1-8.html' # 高血压 106000  == 14700
    # 'http://ask.39.net/browse/22-1-8.html' # 冠心病 23000  == 3100
    # 'http://ask.39.net/browse/466-1-8.html' # 老年痴呆 3000==
    # 'http://ask.39.net/browse/455-1-8.html' # 中风 9000  == 3000
    # 'http://ask.39.net/browse/20-1-8.html' # 糖尿病 177000  == 2800
    # 'http://ask.39.net/browse/1046-1-8.html' # 高血脂 8000  == 2900
    # 'http://ask.39.net/browse/2062-1-8.html' # 痛风 34000  == 3000
    # 'http://ask.39.net/browse/705-1-8.html' # 感冒 275000 == 10800
    # 'http://ask.39.net/browse/625-1-8.html' # 颈椎病 26000  == 1600
    # 'http://ask.39.net/browse/2685-1-8.html' # 咳嗽 308000 == 6300
    # 'http://ask.39.net/browse/6165-1-8.html' # 脂肪肝 15000 == 1400
    # 'http://ask.39.net/browse/756-1-8.html' # 腰腿疼 1000  腰疼-319469631 53000  == 4200
    #     ]
    redis_key = 'ask39net:start_urls'

    rules = (
        # Rule(LinkExtractor(allow=r"/browse/17\-1\-\d+\.html$"), follow=True),
        Rule(LinkExtractor(allow=r"/news/2685\-\d+\.html$"), follow=True),
        Rule(LinkExtractor(allow=r"/question/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//p[@class="ask_tit"]').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//p[@class="txt_ms"]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = []
                answers = response.xpath('//p[@class="sele_txt"]')
                for item_each in answers:
                    answerList.append(self.filter_tags_blank(item_each.extract()))
                item['answer'] = answerList
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

