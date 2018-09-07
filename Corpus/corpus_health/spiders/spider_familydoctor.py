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

class FamilyDoctorSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'familydoctor'
    allowed_domains = ['ask.familydoctor.com.cn']
    # start_urls = [
    # 'http://ask.familydoctor.com.cn/did/87/?page=1&amp;' # 糖尿病
    # 'http://ask.familydoctor.com.cn/did/3008/?page=1&amp;' # 腰腿痛
    # 'http://ask.familydoctor.com.cn/did/777/?page=1&amp;' # 高血脂
    # 'http://ask.familydoctor.com.cn/did/91/?page=1&amp;' # 痛风
    # 'http://ask.familydoctor.com.cn/did/686/?page=1&amp;' # 痴呆
    # 'http://ask.familydoctor.com.cn/did/2722/?page=1&amp;' # 中风
    # 'http://ask.familydoctor.com.cn/did/711/?page=1&amp;' # 脂肪肝
    # 'http://ask.familydoctor.com.cn/did/64/?page=1&amp;' # 冠心病
    # 'http://ask.familydoctor.com.cn/did/1479/?page=1&amp;' # 颈椎病
    # 'http://ask.familydoctor.com.cn/did/600/?page=1&amp;' # 感冒
    # 'http://ask.familydoctor.com.cn/did/63/?page=1&amp;' # 高血压
    # 'http://ask.familydoctor.com.cn/did/2562/?page=1&amp;' # 咳嗽
    #     ]
    redis_key = 'familydoctor:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"http://ask\.familydoctor\.com\.cn/did/3008/\?page=\d+\&$"), follow=True),
        Rule(LinkExtractor(allow=r"http://ask\.familydoctor\.com\.cn/q/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//h3[@class="quest-title"]').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//div[@class="illness-pics"]/p').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = []
                answers = response.xpath('//p[@class="answer-words"]')
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
