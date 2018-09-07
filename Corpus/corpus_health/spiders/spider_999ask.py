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

class Ask999Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'ask999'
    allowed_domains = ['999ask.com']
    # start_urls = [
    # 'http://www.999ask.com/list/gaoxuezhi/all/2.html' # 高血脂
    # 'http://www.999ask.com/list/zhifanggan/all/2.html' # 脂肪肝
    # 'http://www.999ask.com/list/ganmao/all/2.html' # 感冒
    # 'http://www.999ask.com/list/gaoxueya/all/2.html' # 高血压
    # 'http://www.999ask.com/list/kesou/all/2.html' # 咳嗽
    # 'http://www.999ask.com/list/tongfengbing/all/2.html' # 痛风
    # 'http://www.999ask.com/list/guanxinbing/all/2.html' # 冠心病
    # 'http://www.999ask.com/list/tangniaobing/all/2.html' # 糖尿病
    # 'http://www.999ask.com/list/jingzhuibing/all/2.html' # 颈椎病
    #     ]
    redis_key = 'ask999:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"/list/jingzhuibing/all/\d+\.html$"), follow=True),
        Rule(LinkExtractor(allow=r"/allask/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//p[@class="ask_article_title_p1"]').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//p[@class="ask_article_nr1_p2"]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = []
                answers = response.xpath('//div[@class="answer_content2_1"]')
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
