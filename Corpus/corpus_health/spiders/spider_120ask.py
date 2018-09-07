#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/5/29'

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

class Ask120Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'ask120'
    allowed_domains = ['120ask.com']
    # start_urls = [
    #     'http://www.120ask.com/list/gaoxueya/',
    #     'http://www.120ask.com/list/gaoxueya/all/2/'
    # 'http://www.120ask.com/list/tangniaobing/'
    # 'http://www.120ask.com/list/guanxinbing/'
    # 'http://www.120ask.com/list/ganmao/'
    # 'http://www.120ask.com/list/jingzhuibing/'
    # 'https://www.120ask.com/list/zhifanggan/'
    # 'http://www.120ask.com/list/tongfeng/'
    # 'https://www.120ask.com/list/laonianchidai/'
    # 'https://www.120ask.com/list/yaozhuibing/'
    #     ]
    redis_key = 'ask120:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"//www.120ask.com/list/gaoxueya/all/\d+/$"), follow=True),
        Rule(LinkExtractor(allow=r"http://www.120ask.com/question/\d+\.htm$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            item['question'] = response.xpath('//p[@class="crazy_new"]/text()').extract()[1].strip()
            answerList = response.xpath('//div[@class="b_anscont_cont"][1]/div[@class="crazy_new"]/p/text()').extract()
            answer = "".join(answerList)
            item['answer'] = "".join(answer.split())
            yield item
        except Exception as e:
            print(e)
            logger.info("匹配信息出错。错误原因:")
            logger.info(e)

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//h1[@id="d_askH1"]').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//p[@class="crazy_new"][1]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = response.xpath('//div[@class="b_anscont_cont"]')
                itemList = []
                for index, answerli in enumerate(answerList):
                    answer_each = answerli.xpath('.//div[@class="crazy_new"]/p/text()').extract()
                    answer = "".join(answer_each)
                    itemList.append("".join(answer.split()))
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
