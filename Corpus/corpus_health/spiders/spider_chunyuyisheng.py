#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/19'

__QQ__ = '376205871'

"""

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import CorpusHealthItem
from scrapy_redis.spiders import RedisCrawlSpider
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)

class ChunYuYiShengSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'chunyuyisheng'
    allowed_domains = ['chunyuyisheng.com']
    # start_urls = [
    # 'https://www.chunyuyisheng.com/pc/qalist/clinicno_3/diseaseid_273242/?page=1' # 糖尿病
    # 'https://www.chunyuyisheng.com/pc/qalist/clinicno_3/diseaseid_273221/?page=1'  # 痛风
    # 'https://www.chunyuyisheng.com/pc/qalist/clinicno_3/diseaseid_273383/?page=1' # 高血压
    # 'https://www.chunyuyisheng.com/pc/qalist/clinicno_7/diseaseid_268796/?page=1' # 颈椎病
    # 'https://www.chunyuyisheng.com/pc/search/qalist/?query=%E6%84%9F%E5%86%92&page=1' # 感冒
    # 'https://www.chunyuyisheng.com/pc/search/qalist/?query=%E4%B8%AD%E9%A3%8E&page=1' # 中风
    # 'https://www.chunyuyisheng.com/pc/search/qalist/?query=%E5%86%A0%E5%BF%83%E7%97%85&page=1' # 冠心病
    # 'https://www.chunyuyisheng.com/pc/search/qalist/?query=%E8%80%81%E5%B9%B4%E7%97%B4%E5%91%86&page=1' # 老年痴呆
    #     ]
    redis_key = 'chunyuyisheng:start_urls'

    rules = (
        # Rule(LinkExtractor(allow=r"/pc/qalist/clinicno_3/diseaseid_268796/\?page=\d+#hotqa$"), follow=True),  #列表
        Rule(LinkExtractor(allow=r"/pc/search/qalist/\?query=%E5%86%A0%E5%BF%83%E7%97%85&page=\d+$"), follow=True),  #搜索

        Rule(LinkExtractor(allow=r"/pc/qa/[a-zA-Z0-9_\\-]+/$"), callback="parse_detail_mongo", follow=False),
    )

    def parse_detail_mongo(self, response):
        item = CorpusHealthItem()
        try:
            item['url'] = response.url
            question = response.xpath('//span[@class="title"]').extract()[0]
            # question = response.xpath('//h1').extract()[0]
            askText = self.filter_tags_blank(question)
            item['question'] = {'askText': askText, 'askDesc': ''}
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
