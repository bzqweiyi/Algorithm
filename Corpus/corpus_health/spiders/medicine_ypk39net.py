#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/8'

__QQ__ = '376205871'

"""

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import MedicineItem
from scrapy_redis.spiders import RedisCrawlSpider
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)

class MedicineYpk39net(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'medicine_ypk39net'
    allowed_domains = ['ypk.39.net']
    # start_urls = [
    # 'http://ypk.39.net/549982/'
    # 'http://ypk.39.net/588197/'
    #     ]
    redis_key = 'medicine_ypk39net:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r"http://ypk\.39\.net/[a-z]+/$"), follow=True),   # 类别：中西药
        Rule(LinkExtractor(allow=r"http://ypk\.39\.net/[a-z]+/p\d+$"), follow=True),   # 分页
        Rule(LinkExtractor(allow=r"http://ypk\.39\.net/\d+/$"), callback="parse_gaishu", follow=False),    # 概述
        # Rule(LinkExtractor(allow=r"/\d+/manual$"), callback="parse_shuomingshu", follow=False)  # 说明书
    )

    # 爬取概述页面信息
    def parse_gaishu(self, response):
        print("===========概述============")
        item = MedicineItem()
        item["Url"] = response.url
        item["ImgUrl"] = ""
        item["DosageForm"] = ""
        item["Specifications"] = ""
        item["PrescribedDrug"] = ""
        # item["ApprovalNumber"] = ""
        item["ApprovalDate"] = ""
        item["DrugProperties"] = ""
        item["DrugCategory"] = ""
        item["MedicalInsurance"] = ""
        try:
            subs_a = response.xpath('//div[@class="subs"]/p/a')
            subProp = subs_a[1].xpath('.//text()').extract()[0]
            item["DrugProperties"] = self.filter_tags_blank(subProp)
            if len(subs_a) == 3:
                item["DrugCategory"] = subs_a[2].xpath('.//text()').extract()[0]
        except Exception as e:
            print("=======yaopinshuxing=====")
            print(e)
            logger.info(response.url)
            logger.info("=======yaopinshuxing=====")
            logger.info(e)
        try:
            xxsLis = response.xpath('//ul[@class="xxs"]/li')
            for xxsli in xxsLis:
                xxsCite = xxsli.xpath('.//cite/text()').extract()[0]
                # if xxsCite == "批准文号：":
                #     xxsTemp = xxsli.extract()
                #     item["ApprovalNumber"] = self.filter_tags_blank(xxsTemp).split("批准文号：")[1]
                if xxsCite == "批准日期：":
                    xxsTemp = xxsli.extract()
                    item["ApprovalDate"] = self.filter_tags_blank(xxsTemp).split("批准日期：")[1]
        except Exception as e:
            print("=======pizhunriqi=====")
            print(e)
            logger.info(response.url)
            logger.info("=======pizhunriqi=====")
            logger.info(e)
        try:
            item["ImgUrl"] = response.xpath('//div[@class="imgbox"]/img/@src').extract()[0]
        except Exception as e:
            print("========tupian======")
            print(e)
            logger.info(response.url)
            logger.info("=======tupian=====")
            logger.info(e)
        try:
            showLis = response.xpath('//ul[@class="showlis"]/li')
            for eachLi in showLis:
                propsTitle = eachLi.xpath('.//cite/text()').extract()[0]
                if "剂型：" in propsTitle:
                    item["DosageForm"] = self.filter_tags_blank(eachLi.extract()).split("剂型：")[1]
                elif "规格：" in propsTitle:
                    item["Specifications"] = self.filter_tags_blank(eachLi.extract()).split("规格：")[1]
        except Exception as e:
            print("=======guige======")
            print(e)
            logger.info(response.url)
            logger.info("=======guige=====")
            logger.info(e)
        try:
            cites = response.xpath('//div[@class="yps_top"]/div[@class="t1"]/cite')
            for cite in cites:
                iClass = cite.xpath('.//i/@class').extract()[0]
                if "icon1" in iClass or "icon2" in iClass:
                    # 非处方药
                    item["PrescribedDrug"] = cite.xpath('.//span/text()').extract()[0]
                elif "icon5" in iClass or "icon12" in iClass:
                    # 医保用药
                    item["MedicalInsurance"] = cite.xpath('.//span/text()').extract()[0]
                    # icon9 外用药，icon4 国家基本药物目录（2012）
        except Exception as e:
            print("============chufangyao|yibao======")
            print(e)
            logger.info(response.url)
            logger.info("=======chufangyao|yibao=====")
            logger.info(e)
        # print(item)
        url = item["Url"] + "manual"
        yield scrapy.Request(url, meta=item, callback=self.parse_shuomingshu)

    # 爬取说明书信息
    def parse_shuomingshu(self, response):
        print("========说明书========")
        item = MedicineItem()
        # 24
        # 概述数据
        item["Url"] = response.meta["Url"]
        item["ImgUrl"] = response.meta["ImgUrl"]
        item["DosageForm"] = response.meta["DosageForm"]
        item["Specifications"] = response.meta["Specifications"]
        item["PrescribedDrug"] = response.meta["PrescribedDrug"]
        # item["ApprovalNumber"] = response.meta["ApprovalNumber"]
        item["ApprovalDate"] = response.meta["ApprovalDate"]
        item["DrugCategory"] = response.meta["DrugCategory"]
        item["DrugProperties"] = response.meta["DrugProperties"]
        item["MedicalInsurance"] = response.meta["MedicalInsurance"]
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
        item["DosageAndAdministration"] = ""
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
        try:
            tabBox = response.xpath('//div[@class="tab_box"]/div/dl')
            for dl in tabBox:
                propsTitle = dl.xpath('.//dt/text()').extract()[0]
                if "药品名称" in propsTitle:
                    try:
                        namesHtml = dl.xpath('.//dd/p').extract()[0].split("<br>")
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
                elif "用法用量" in propsTitle:
                    try:
                        DosageAndAdministration = dl.xpath('.//dd').extract()[0]
                        item["DosageAndAdministration"] = self.filter_tags_blank(DosageAndAdministration)
                    except Exception as e:
                        print("========yongfayongliang=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======yongfayongliang=====")
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
                        productionsDd = dl.xpath('.//dd')
                        for each_dd in productionsDd:
                            ddText = each_dd.xpath('.//text()').extract()[0]
                            if "企业名称：" in ddText:
                                item["ManufacturingEnterprise"]["EnterpriseName"] = self.filter_tags_blank(ddText).split("企业名称：")[1]
                            elif "企业简称：" in ddText:
                                item["ManufacturingEnterprise"]["EnterpriseAbbreviation"] = self.filter_tags_blank(ddText).split("企业简称：")[1]
                            elif "生产地址：" in ddText:
                                item["ManufacturingEnterprise"]["ProductionAddress"] = self.filter_tags_blank(ddText).split("生产地址：")[1]
                            elif "联系电话：" in ddText:
                                item["ManufacturingEnterprise"]["ContactNumber"] = \
                                self.filter_tags_blank(ddText).split("联系电话：")[1].split("如有问题")[0]
                    except Exception as e:
                        print("=======shengchanqiye=======")
                        print(e)
                        logger.info(response.url)
                        logger.info("=======shengchanqiye=====")
                        logger.info(e)

            print(item["Url"])
            yield item
        except Exception as e:
            logger.info(response.url)
            logger.info("说明书匹配出错，错误原因:")
            logger.info(e)


    """
    去掉html标签和空格
    """
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())
