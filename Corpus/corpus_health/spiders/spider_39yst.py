#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/22'

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
    name = '39yst'
    allowed_domains = ['39yst.com']
    # start_urls = [
    # 'http://www.39yst.com/ask/search/?q=%E5%92%B3%E5%97%BD' # 咳嗽
    # 'http://www.39yst.com/ask/search/?q=%E9%AB%98%E8%A1%80%E5%8E%8B' # 高血压
    # 'http://www.39yst.com/ask/search/?q=%E5%86%A0%E5%BF%83%E7%97%85&page=2' # 冠心病
    # 'http://www.39yst.com/ask/search/?q=%E7%97%B4%E5%91%86' # 痴呆
    # 'http://www.39yst.com/ask/search/?q=%E4%B8%AD%E9%A3%8E' # 中风
    # 'http://www.39yst.com/ask/search/?q=%E7%B3%96%E5%B0%BF%E7%97%85' # 糖尿病
    # 'http://www.39yst.com/ask/search/?q=%E9%AB%98%E8%A1%80%E8%84%82' # 高血脂
    # 'http://www.39yst.com/ask/search/?q=%E7%97%9B%E9%A3%8E' # 痛风
    # 'http://www.39yst.com/ask/search/?q=%E6%84%9F%E5%86%92' # 感冒
    # 'http://www.39yst.com/ask/search/?q=%E9%A2%88%E6%A4%8E%E7%97%85' # 颈椎病
    # 'http://www.39yst.com/ask/search/?q=%E8%84%82%E8%82%AA%E8%82%9D' # 脂肪肝
    # 'http://www.39yst.com/ask/search/?q=%E8%85%B0%E7%96%BC' # 腰腿疼（腰疼）
    # 'http://www.39yst.com/ask/search/?q=%E8%85%BF%E7%96%BC' # 腰腿疼（腿疼）
    #     ]
    redis_key = '39yst:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"/ask/search/\?q=腰疼\&page=\d+$"), follow=True),
        Rule(LinkExtractor(allow=r"/ask/\d+\.shtml$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//h1').extract()[0].replace('<span>问</span>', '')
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//div[@class="wenti_dec"]/p').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
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
