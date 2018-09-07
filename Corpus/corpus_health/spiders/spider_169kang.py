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

class Kang169Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'kang169'
    allowed_domains = ['169kang.com']
    # start_urls = [
    # 'https://www.169kang.com/ask-gaoxueya/2' # 高血压
    # 'https://www.169kang.com/ask-guanxinbing' # 冠心病
    # 'https://www.169kang.com/ask-tongfeng' # 痛风
    # 'https://www.169kang.com/ask-ganmao' # 感冒
    # 'https://www.169kang.com/ask-tangniaobing' # 糖尿病
    # 'https://www.169kang.com/ask-zhongfeng' # 中风
    # 'https://www.169kang.com/ask-jingzhuibing' # 颈椎病
    #     ]
    redis_key = 'kang169:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"/ask\-gaoxueya/\d+$"), follow=True),
        Rule(LinkExtractor(allow=r"/question/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//h1[@class="four font-16 u_tit bold"]').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//p[@class="k_questiond"]/b').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = []
                answers = response.xpath('//div[@class="crazy_new"]')
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


