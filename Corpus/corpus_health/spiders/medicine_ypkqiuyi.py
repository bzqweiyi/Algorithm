#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/10'

__QQ__ = '376205871'

"""

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import MedicineItem
from scrapy_redis.spiders import RedisCrawlSpider
import urllib.parse
from math import floor
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)

class MedicineYpkQiuyi(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'medicine_ypkqiuyi'
    allowed_domains = ['ypk.qiuyi.cn']
    # start_urls = [
    # 'http://ypk.qiuyi.cn/index.html'
    # 'http://ypk.qiuyi.cn/detail/31510.html'
    # 'http://ypk.qiuyi.cn/explain/31510.html'
    #     ]
    redis_key = 'medicine_ypkqiuyi:start_urls'

    rules = (
        # Rule(LinkExtractor(allow=r"http://ypk\.qiuyi\.cn/list/\d+\.html$"), follow=True),   # 类别
        # Rule(LinkExtractor(allow=r"http://ypk\.qiuyi\.cn/list/\d+_0_0_0_0_0_0_0_\d+\.html$"), follow=True),   # 分页
        Rule(LinkExtractor(allow=r"http://ypk\.qiuyi\.cn/detail/\d+\.html$"), callback="parse_gaishu", follow=False),    # 概述
        # Rule(LinkExtractor(allow=r"http://ypk\.qiuyi\.cn/explain/\d+\.html$"), callback="parse_shuomingshu", follow=False)  # 说明书
    )

    # 爬取概述页面信息
    def parse_gaishu(self, response):
        print("===========概述============")
        item = MedicineItem()
        item["Url"] = response.url
        item["ImgUrl"] = ""
        item["Specifications"] = ""
        item["PrescribedDrug"] = ""
        item["ApprovalDate"] = ""
        item["DrugProperties"] = ""
        item["DrugCategory"] = ""
        item["MedicalInsurance"] = ""
        item["DosageAndAdministration"] = ""
        try:
            gaishuBox = response.xpath('//div[@class="yp_d1"]/p')
            for divp in gaishuBox:
                strongText = divp.xpath('.//strong/text()').extract()[0]
                if "用法用量" in strongText:
                    try:
                        shouqiText = divp.xpath('.//span[@class="shouqi"]/text()').extract()[0]
                        item["DosageAndAdministration"] = self.filter_tags_blank(shouqiText)
                    except Exception as e:
                        print("=======yongfayongliang=====")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======yongfayongliang=====")
                        logger.info(e)
                elif "医保类型" in strongText:
                    try:
                        yibaoText = divp.extract()
                        item["MedicalInsurance"] = self.filter_tags_blank(yibaoText).split("医保类型")[1]
                    except Exception as e:
                        print("=======yibao=====")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======yibao=====")
                        logger.info(e)
                elif "药品属性" in strongText:
                    try:
                        shuxingText = divp.extract()
                        item["DrugProperties"] = self.filter_tags_blank(shuxingText).split("药品属性")[1]
                    except Exception as e:
                        print("=======yaopinshuxing=====")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======yaopinshuxing=====")
                        logger.info(e)
            try:
                ypLis = response.xpath('//div[@class="yp_d2"]/ul/li')
                for ypli in ypLis:
                    ypliText = ypli.xpath('.//strong/text()').extract()[0]
                    if "规格：" in ypliText:
                        temptpli = ypli.extract()
                        item["Specifications"] = self.filter_tags_blank(temptpli).split("规格：")[1]
            except Exception as e:
                print("=======guige=====")
                print(e)
                logger.info(response.url)
                logger.info("=======guige=====")
                logger.info(e)
            try:
                subs_a = response.xpath('//div[@class="path"]/a')
                item["DrugCategory"] = subs_a[1].xpath('.//text()').extract()[0]
            except Exception as e:
                print("=======yaopinleibie=====")
                print(e)
                logger.info(response.url)
                logger.info("=======yaopinleibie=====")
                logger.info(e)
            # try:
            #     xxsLis = response.xpath('//ul[@class="xxs"]/li')
            #     for xxsli in xxsLis:
            #         xxsCite = xxsli.xpath('.//cite/text()').extract()[0]
            #         if xxsCite == "批准日期：":
            #             xxsTemp = xxsli.extract()
            #             item["ApprovalDate"] = self.filter_tags_blank(xxsTemp).split("批准日期：")[1]
            # except Exception as e:
            #     print("=======pizhunriqi=====")
            #     print(e)
            #     logger.info("=======pizhunriqi=====")
            #     logger.info(e)
            try:
                item["ImgUrl"] = response.xpath('//a[@class="img_4"]/img/@src').extract()[0]
            except Exception as e:
                print("========tupian======")
                print(e)
                logger.info(response.url)
                logger.info("=======tupian=====")
                logger.info(e)
            try:
                item["PrescribedDrug"] = response.xpath('//ul[@class="one ul_h"]/li[@class="o1"]/text()').extract()[0]
            except Exception as e:
                try:
                    item["PrescribedDrug"] = response.xpath('//ul[@class="one ul_h"]/li[@class="o2"]/text()').extract()[
                        0]
                except Exception as e:
                    print("========chufangyao======")
                    print(e)
                    logger.info(response.url)
                    logger.info("=======chufangyao=====")
                    logger.info(e)
            try:
                urlId = item["Url"].split("detail/")[1].split(".")[0]
                url = 'http://ypk.qiuyi.cn/explain/' + urlId + '.html'
                yield scrapy.Request(url, meta=item, callback=self.parse_shuomingshu)
            except Exception as e:
                print("==========explain url error========")
                print(e)
                logger.info(response.url)
                logger.info("=======explain url error=====")
                logger.info(e)
            # print(item)
        except Exception as e:
            print("=======概述信息出错=====")
            print(e)
            logger.info(response.url)
            logger.info("=======概述信息出错=====")
            logger.info(e)

    # 爬取说明书信息
    def parse_shuomingshu(self, response):
        print("========说明书========")
        item = MedicineItem()
        # 24
        # 概述数据
        item["Url"] = response.meta["Url"]
        item["ImgUrl"] = response.meta["ImgUrl"]
        item["Specifications"] = response.meta["Specifications"]
        item["PrescribedDrug"] = response.meta["PrescribedDrug"]
        item["ApprovalDate"] = response.meta["ApprovalDate"]
        item["DrugCategory"] = response.meta["DrugCategory"]
        item["DrugProperties"] = response.meta["DrugProperties"]
        item["MedicalInsurance"] = response.meta["MedicalInsurance"]
        item["DosageAndAdministration"] = response.meta["DosageAndAdministration"]
        # 说明书数据
        item["DrugNames"] = {
            "BrandName": "",
            "TradeName": "",
            "GenericName": "",
            "ChemicalName": "",
            "EnglishName": ""
        }
        item["Composition"] = ""
        item["Indications"] = ""
        item["AdverseReactions"] = ""
        item["Contraindications"] = ""
        item["Precautions"] = ""
        item["SpecialDrugUse"] = ""
        item["Interactions"] = ""
        item["PharmacologicalActions"] = ""
        item["Storage"] = ""
        item["Validity"] = ""
        item["ApprovalNumber"] = ""
        item["RevisionDate"] = ""
        item["ManufacturingEnterprise"] = {
            "EnterpriseName": "",
            "EnterpriseAbbreviation": "",
            "ProductionAddress": "",
            "ContactNumber": ""
        }
        item["DosageForm"] = ""
        try:
            tabBox = response.xpath('//div[@class="dzzy"]/div[@class="bd"]/div[@class="tab_c"]/dl')
            for dl in tabBox:
                propsTitle = dl.xpath('.//dt/text()').extract()[0]
                if "药品名称" in propsTitle:
                    try:
                        namesHtml = dl.xpath('.//dd').extract()[0].split("<br>")
                        for eachName in namesHtml:
                            strName = self.filter_tags_blank(eachName)
                            if strName:
                                if "商品名称：" in eachName:
                                    item["DrugNames"]["TradeName"] = strName.split("商品名称：")[1]
                                elif "通用名称：" in eachName:
                                    item["DrugNames"]["GenericName"] = strName.split("通用名称：")[1]
                                elif "英文名称：" in eachName:
                                    item["DrugNames"]["EnglishName"] = strName.split("英文名称：")[1]
                                elif "化学名称：" in eachName:
                                    item["DrugNames"]["ChemicalName"] = strName.split("化学名称：")[1]
                    except Exception as e:
                        print("========yaopinmingcheng=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======yaopinmingcheng=====")
                        logger.info(e)
                elif "成份" in propsTitle:
                    try:
                        Composition = dl.xpath('.//dd').extract()[0]
                        item["Composition"] = self.filter_tags_blank(Composition)
                    except Exception as e:
                        print("========chengfen=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======chengfen=====")
                        logger.info(e)
                elif "剂型" in propsTitle:
                    try:
                        Composition = dl.xpath('.//dd').extract()[0]
                        item["DosageForm"] = self.filter_tags_blank(Composition)
                    except Exception as e:
                        print("========jixing=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======jixing=====")
                        logger.info(e)
                elif "适应症" in propsTitle or "功能主治" in propsTitle:
                    try:
                        Indications = dl.xpath('.//dd').extract()[0]
                        item["Indications"] = self.filter_tags_blank(Indications)
                    except Exception as e:
                        print("========shiyingzheng=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======shiyingzheng=====")
                        logger.info(e)
                elif "不良反应" in propsTitle:
                    try:
                        AdverseReactions = dl.xpath('.//dd').extract()[0]
                        item["AdverseReactions"] = self.filter_tags_blank(AdverseReactions)
                    except Exception as e:
                        print("========buliangfanying=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======buliangfanying=====")
                        logger.info(e)
                elif "禁忌" in propsTitle:
                    try:
                        Contraindications = dl.xpath('.//dd').extract()[0]
                        item["Contraindications"] = self.filter_tags_blank(Contraindications)
                    except Exception as e:
                        print("========jinji=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======jinji=====")
                        logger.info(e)
                elif "注意事项" in propsTitle:
                    try:
                        Precautions = dl.xpath('.//dd').extract()[0]
                        item["Precautions"] = self.filter_tags_blank(Precautions)
                    except Exception as e:
                        print("========zhuyishixiang=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======zhuyishixiang=====")
                        logger.info(e)
                elif "特殊人群用药" in propsTitle:
                    try:
                        SpecialDrugUse = dl.xpath('.//dd').extract()[0]
                        item["SpecialDrugUse"] = self.filter_tags_blank(SpecialDrugUse)
                    except Exception as e:
                        print("========teshurenqunyongyao=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======teshurenqunyongyao=====")
                        logger.info(e)
                elif "药物相互作用" in propsTitle:
                    try:
                        Interactions = dl.xpath('.//dd').extract()[0]
                        item["Interactions"] = self.filter_tags_blank(Interactions)
                    except Exception as e:
                        print("========yaowuxianghuzuoyong=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======yaowuxianghuzuoyong=====")
                        logger.info(e)
                elif "药理作用" in propsTitle:
                    try:
                        PharmacologicalActions = dl.xpath('.//dd').extract()[0]
                        item["PharmacologicalActions"] = self.filter_tags_blank(PharmacologicalActions)
                    except Exception as e:
                        print("========yaolizuoyong=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======yaolizuoyong=====")
                        logger.info(e)
                elif "贮藏" in propsTitle:
                    try:
                        Storage = dl.xpath('.//dd').extract()[0]
                        item["Storage"] = self.filter_tags_blank(Storage)
                    except Exception as e:
                        print("========zhucang=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======zhucang=====")
                        logger.info(e)
                elif "有效期" in propsTitle:
                    try:
                        Validity = dl.xpath('.//dd').extract()[0]
                        item["Validity"] = self.filter_tags_blank(Validity)
                    except Exception as e:
                        print("========youxiaoqi=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======youxiaoqi=====")
                        logger.info(e)
                elif "批准文号" in propsTitle:
                    try:
                        ApprovalNumber = dl.xpath('.//dd').extract()[0]
                        item["ApprovalNumber"] = self.filter_tags_blank(ApprovalNumber)
                    except Exception as e:
                        print("========pizhunwenhao=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======pizhunwenhao=====")
                        logger.info(e)
                elif "说明书修订日期" in propsTitle:
                    try:
                        RevisionDate = dl.xpath('.//dd').extract()[0]
                        item["RevisionDate"] = self.filter_tags_blank(RevisionDate)
                    except Exception as e:
                        print("========xiudingriqi=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======xiudingriqi=====")
                        logger.info(e)
                elif "生产企业" in propsTitle:
                    try:
                        productionsDd = dl.xpath('.//dd').extract()[0].split("\r")
                        for ddText in productionsDd:
                            if "企业名称：" in ddText:
                                item["ManufacturingEnterprise"]["EnterpriseName"] = self.filter_tags_blank(ddText).split("企业名称：")[1]
                            elif "企业简称：" in ddText:
                                item["ManufacturingEnterprise"]["EnterpriseAbbreviation"] = self.filter_tags_blank(ddText).split("企业简称：")[1]
                            elif "生产地址：" in ddText:
                                item["ManufacturingEnterprise"]["ProductionAddress"] = self.filter_tags_blank(ddText).split("生产地址：")[1]
                            elif "联系电话：" in ddText:
                                item["ManufacturingEnterprise"]["ContactNumber"] = \
                                self.filter_tags_blank(ddText).split("联系电话：")[1]
                    except Exception as e:
                        print("=======shengchanqiye=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======shengchanqiye=====")
                        logger.info(e)
            # print(item)
            yield item
        except Exception as e:
            print("========说明书匹配出错========")
            logger.info(response.url)
            logger.info("说明书匹配出错，错误原因:")
            logger.info(e)


    """
    去掉html标签和空格
    """
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())
