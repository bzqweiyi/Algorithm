#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/13'

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

class Xhs100Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'fh21'
    allowed_domains = ['iask.fh21.com.cn']
    # start_urls = [
    # 'https://iask.fh21.com.cn/question/list-32.html' # 高血压
    # 'https://iask.fh21.com.cn/question/list-35.html' # 冠心病
    # 'https://iask.fh21.com.cn/question/list-402.html' # 感冒
    # 'https://iask.fh21.com.cn/question/list-44.html' # 糖尿病
    # 'https://iask.fh21.com.cn/question/list-136.html' # 痴呆
    # 'https://iask.fh21.com.cn/question/list-74.html' # 痛风
    # 'https://iask.fh21.com.cn/question/list-78.html' # 颈椎病
    # 'https://iask.fh21.com.cn/question/list-97.html' # 脂肪肝
    # 'https://iask.fh21.com.cn/question/list-217.html' # 咳嗽
    # 'https://iask.fh21.com.cn/question/list-347.html' # 中风
    #     ]
    redis_key = 'fh21:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"/question/list-347-1-0-\d+\.html$"), follow=True),
        Rule(LinkExtractor(allow=r"/question/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//div[@class="iask_detail01a"]//ul').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//div[@class="iask_detail01b1"]/dl[2]/dd').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = []
                answers = response.xpath('//div[@class="iask_answer02a"]')
                for item_each in answers:
                    answerLi = item_each.xpath('.//dd').extract()[0]
                    answerList.append(self.filter_tags_blank(answerLi))
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

