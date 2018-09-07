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

class AskQiuyiSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'askqiuyi'
    allowed_domains = ['ask.qiuyi.cn']
    # start_urls = [
    # 'http://ask.qiuyi.cn/departments/37_1/index.html' #糖尿病
    # 'http://ask.qiuyi.cn/departments/763_1/index.html' #高血压
    # 'http://ask.qiuyi.cn/departments/490_1/index.html' # 老年痴呆
    # 'http://ask.qiuyi.cn/departments/505_1/index.html' # 颈椎病
    # 'http://ask.qiuyi.cn/departments/771_1/index.html' # 感冒
    # 'http://ask.qiuyi.cn/departments/36_1/index.html' # 痛风 ID = 41
    # 'http://ask.qiuyi.cn/departments/57_1/index.html' # 冠心病
    # 'http://ask.qiuyi.cn/departments/815_1/index.html' # 高血脂
    # 'http://ask.qiuyi.cn/departments/92_1/index.html' # 脂肪肝
    # 'http://ask.qiuyi.cn/departments/1148_1/index.html' # 腰痛
    # 'http://ask.qiuyi.cn/departments/745_1/index.html' # 中风
    # 'http://ask.qiuyi.cn/departments/22_1/index.html' # 慢性咳嗽
    #     ]
    redis_key = 'askqiuyi:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"http://ask\.qiuyi\.cn/departments/22_\d+/index\.html$"), follow=True),
        Rule(LinkExtractor(allow=r"http://ask\.qiuyi\.cn/question/\d+\.htm$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//div[@class="ask_title"]/h1').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//div[@class="ask_title"]/following-sibling::div[@class="wd_cont_s"][1]/p[1]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = []
                answers = response.xpath('//div[@class="angle"]')
                for answer_each in answers:
                    answer = answer_each.xpath('.//following-sibling::p[1]').extract()[0]
                    answerList.append(self.filter_tags_blank(answer))
                item['answer'] = answerList
            except Exception as e:
                item['answer'] = []
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



