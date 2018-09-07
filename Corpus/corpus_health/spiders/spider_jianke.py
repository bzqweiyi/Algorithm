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

class JiankeSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'jianke'
    allowed_domains = ['jianke.com']
    # start_urls = [
    # 'https://www.jianke.com/ask/browse/10401-1-1' #高血压 34000
    # 'https://www.jianke.com/ask/browse/10405-1-1' #冠心病 11000
    # 'https://www.jianke.com/ask/browse/10103-1-1' #感冒 116000
    # 'https://www.jianke.com/ask/browse/10603-1-1' #痛风 8000
    # 'https://www.jianke.com/ask/browse/10807-1-1' #糖尿病 34000
    # 'https://www.jianke.com/ask/browse/3020201-1-1' #劲椎病 12000
    # 'https://www.jianke.com/ask/browse/1050201-1-1' #脂肪肝 5600
    # 'https://www.jianke.com/ask/browse/10104-1-1' #咳嗽（肺炎）
    # 'https://www.jianke.com/ask/browse/30901-1-1' #痴呆
    # 'https://search.jianke.com/ask?wd=%E7%97%B4%E5%91%86'  #痴呆（搜索）
    # 'https://search.jianke.com/ask?wd=%E4%B8%AD%E9%A3%8E&pn=2' #中风（搜索）
    # 'https://search.jianke.com/ask?wd=%E8%85%B0%E8%85%BF%E7%96%BC&pn=2' #腰腿疼（搜索）
    # 'https://search.jianke.com/ask?wd=%E9%AB%98%E8%A1%80%E8%84%82&pn=2'  #高血脂（搜索）
    #     ]
    redis_key = 'jianke:start_urls'

    rules = (
        # Rule(LinkExtractor(allow=r"/ask/browse/10103\-1\-\d+$"), follow=True),
        # Rule(LinkExtractor(allow=r"/ask/question/\d+$"), callback="parse_detail_mongo", follow=False),
        Rule(LinkExtractor(allow=r"//search\.jianke\.com/ask\?wd=%E7%97%B4%E5%91%86\&pn=\d+$"), follow=True),
        Rule(LinkExtractor(allow=r"//www\.jianke\.com/ask/question/\d+$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
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


