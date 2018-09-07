#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/12'

__QQ__ = '376205871'

"""

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import NewsItem
from scrapy_redis.spiders import RedisCrawlSpider
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)

class Care39NetSpider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    # start_urls = [
    # 'http://care.39.net/'
    # 'http://care.39.net/a/171012/5756083.html'
    #     ]

    # 保健
    # name = 'care39net'
    # allowed_domains = ['care.39.net']
    # redis_key = 'care39net:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r"http://care\.39\.net/[\w/]+$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://care\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://care\.39\.net/a/\d+/\d+\.html$"), callback="parse_detail_mongo", follow=False),
    # )

    # 饮食
    # name = 'food39net'
    # allowed_domains = ['food.39.net']
    # redis_key = 'food39net:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r"http://food\.39\.net/[\w/]+$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://food\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://food\.39\.net/a/\d+/\d+\.html$"), callback="parse_detail_mongo",
    #          follow=False),
    # )

    # 健身
    # name = 'sports39net'
    # allowed_domains = ['sports.39.net']
    # redis_key = 'sports39net:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r"http://sports\.39\.net/[\w/]+$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://sports\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://sports\.39\.net/a/\d+/\d+\.html$"), callback="parse_detail_mongo",
    #          follow=False),
    # )

    # 中医
    # name = 'cm39net'
    # allowed_domains = ['cm.39.net']
    # redis_key = 'cm39net:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r"http://cm\.39\.net/[\w/]+$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://cm\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://cm\.39\.net/a/\d+/\d+\.html$"), callback="parse_detail_mongo",
    #          follow=False),
    # )

    # 药品频道
    # name = 'drug39net'
    # allowed_domains = ['drug.39.net']
    # redis_key = 'drug39net:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r"http://drug\.39\.net/[\w/]+index\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://drug\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://drug\.39\.net/a/\d+/\d+\.html$"), callback="parse_detail_mongo",
    #          follow=False),
    # )

    # 心血管疾病
    # name = 'heart39net'
    # allowed_domains = ['heart.39.net']
    # redis_key = 'heart39net:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r"http://heart\.39\.net/[\w/]+(index\.html){0,1}$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://heart\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://heart\.39\.net/a/\d+/\d+\.html$"), callback="parse_detail_mongo",
    #          follow=False),
    # )

    # 减肥
    # name = 'fitness39net'
    # allowed_domains = ['fitness.39.net']
    # redis_key = 'fitness39net:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r"http://fitness\.39\.net/[\w/]+$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://fitness\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://fitness\.39\.net/a/\d+/\d+\.html$"), callback="parse_detail_mongo",
    #          follow=False),
    # )

    # 糖尿病
    name = 'tnb39net'
    allowed_domains = ['tnb.39.net']
    redis_key = 'tnb39net:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r"http://tnb\.39\.net/[\w/]+(index\.html){0,1}$"), follow=True),
        Rule(LinkExtractor(allow=r"http://tnb\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
        Rule(LinkExtractor(allow=r"http://tnb\.39\.net/a/\d+/\d+\.html$"), callback="parse_detail_mongo",
             follow=False),
    )

    # 资讯
    # name = 'news39net'
    # allowed_domains = ['news.39.net']
    # redis_key = 'news39net:start_urls'
    # rules = (
    #     Rule(LinkExtractor(allow=r"http://news\.39\.net/[\w/]+$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://news\.39\.net/[\w/]+index_\d+\.html$"), follow=True),
    #     Rule(LinkExtractor(allow=r"http://news\.39\.net/(jbyw|yltx|medicine|ysbj/ys|kyfx|shwx|"
    #                              r"qwfb|jjyg|hyfh|hxw|hsp|mxrd|qwqs|icu|xinzhi|tsxw|jkyys|pp/pp_04|"
    #                              r"interview|xwzt/xwgc|tpzx|sjsh|39dc|a)/\d+/\d+\.html$"), callback="parse_detail_mongo",
    #          follow=False),
    # )

    def parse_detail_mongo(self, response):
        item = NewsItem()
        try:
            item['url'] = response.url
            title = response.xpath('//h1').extract()[0]
            item['title'] = self.filter_tags_blank(title)
            category = response.xpath('//span[@class="art_location"]').extract()[0]
            item['category'] = self.filter_tags_blank(category)
            content = response.xpath('//div[@id="contentText"]').extract()[0]
            item['content'] = self.filterTags(str(content))
            # print(item)
            yield item
        except Exception as e:
            print(e)
            logger.info(response.url)
            logger.info("匹配信息出错。错误原因:")
            logger.info(e)


    # 去掉html标签和空格
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())


    # 过滤script标签及里面内容
    def filterTags(self, htmlstr):
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_script_s = re.compile('<(script).*?>[\s\S]*?<\/script>', re.I)   # Script标签里含有script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_iframe = re.compile('<\s*iframe[^>]*>[^<]*<\s*/\s*iframe\s*>', re.I)  # iframe
        re_br = re.compile('<br\s*?/?>')  # 处理换行
    #     re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        re_a = re.compile('</?a[^>]*>')   # a标签
        blank_line = re.compile('\n+')  # 多余空行

        # 过滤匹配内容
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_script_s.sub('', s)  # 去掉SCRIPT和里面的SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_iframe.sub('', s)  # 去掉iframe
        s = re_br.sub('\n', s)  # 将br转换为换行
    #     s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        s = re_a.sub('', s)     # 去掉a标签保留内容
        s = blank_line.sub('\n', s)  # 去掉多余的空行
        return s

