#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/19'

__QQ__ = '376205871'

"""

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import CorpusHealthItem
from scrapy_redis.spiders import RedisCrawlSpider
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)

class CnkangSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'cnkang'
    allowed_domains = ['cnkang.com']
    # start_urls = [
    # 'http://www.cnkang.com/ask/question/list_13_0_1.html' # 心血管内科
    # 'http://www.cnkang.com/ask/question/list_20_0_1.html' # 感染内科
    #     ]
    redis_key = 'cnkang:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"/ask/question/list_20_0_\d+\.html$"), callback="parse_detail", follow=True),
        # Rule(LinkExtractor(allow=r"/question/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail(self, response):
        detailUrls = response.xpath('//div[@class="iask12_con"]/dl')
        for each_url in detailUrls:
            url = each_url.xpath('.//dt/a/@href').extract()[0]
            request_url = 'http://www.cnkang.com' + url
            yield scrapy.Request(request_url, callback=self.parse_detail_mongo)

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//dl[@class="iask13_title"]/dt').extract()[0]
            askTxt = self.filter_tags_blank(question)
            try:
                desc = response.xpath('//div[@class="iask13 iask13_q"]/ul[@class="iask13_con"]').extract()[0]
                descText = self.filter_tags_blank(desc)
            except Exception as e:
                descText = ''
            item['question'] = {'askText': askTxt, 'askDesc': descText}
            try:
                answerList = []
                answers = response.xpath('//div[@class="iask13 iask13_a"]')
                for item_each in answers:
                    ulList = item_each.xpath('.//ul[@class="iask13_con"]')
                    tempAnswer = ''
                    for item_ul in ulList:
                        tempAnswer = tempAnswer + self.filter_tags_blank(item_ul.extract())
                    answerList.append(tempAnswer)
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

