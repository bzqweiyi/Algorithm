#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/19'

__QQ__ = '376205871'

字段说明：
    # Url                           网址
    # Name                          疾病名称
    # Summary                       概述
    # Intro                         介绍
    # MedicalInsurance              是否属于医保
    # Alias                         别名
    # Lesions                       发病部位
    # Contagion                     传染性
    # RouteOfTransmission           传播途径
    # Incubation                    潜伏期
    # LatentPeriodSymptom           潜伏期表现
    # MultiplePopulation            多发人群
    # CommonlyUsedDrugs             常用药品
    
    # Symptom                       症状
    # EarlySymptom                  早期症状
    # AdvancedSymptom               晚期症状
    # RelatedSymptoms               相关症状
    # TypicalSymptoms               典型症状
    # SymptomDescription            症状描述
    # SymptomDescriptionTag         症状描述（含html标签）
    
    # Cause                         发病原因
    # CauseOfDisease                病因
    # CauseOfDiseaseTag             病因（含html标签）
    
    # Prevention                    预防
    # DiseasePrevention             疾病预防
    # DiseasePreventionTag          疾病预防（含html标签）
    
    # Identify                      鉴别
    # IdentifyDisease               疾病鉴别
    # IdentifyDiseaseTag            疾病鉴别（含html标签）
    
    # Treatment                     治疗
    # ClinicDepartment              就诊科室
    # TreatmentExpense              治疗费用
    # CureRate                      治愈率
    # TreatmentCycle                治疗周期
    # TherapeuticMethod             治疗方法
    # TreatmentBox                  治疗描述
    # TreatmentBoxTag               治疗描述（含html标签）
    
    # DiseaseCare                   疾病护理
    # Nursing                       护理
    # NursingTag                    护理（含html标签）
    
    # DietaryHealth                 饮食保健
    # EatFood                       宜吃
    # DietTaboo                     禁忌
    # Guideline                     饮食原则
    # WhatToEat                     吃什么好
    # Dietotherapy                  食疗偏方
    # GuidelineBoxTag               饮食原则（含html标签）
    
    # Complication                  并发症
    # ConcurrentDisease             并发疾病
    # ComplicationBox               并发症介绍
    # ComplicationBoxTag            并发症介绍（含html标签）
    
    
    未录入数据：
        1、就诊指南  /jzzn/
        2、临床检查  /jcjb/

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import random
import re
import pymongo
from datetime import datetime
# from ..Util.LogHandler import LogHandler
# logger = LogHandler(__name__, stream=True)

# 日志操作
import os
import logging
from logging.handlers import TimedRotatingFileHandler

# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')


class LogHandler(logging.Logger):
    """
    LogHandler
    """

    def __init__(self, name, level=DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='midnight', interval=1, backupCount=15)
        file_handler.suffix = '%Y-%m-%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        # if not len(self.handlers):
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def resetName(self, name):
        """
        reset name
        :param name:
        :return:
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()

logger = LogHandler("disease_jbk39net_v2", stream=True)

class getJbk():
    def __init__(self):
        self.user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        # self.url = 'http://jbk.39.net/map/'
        self.url = 'http://jbk.39.net/map_p792/'
        # self.url = 'http://jbk.39.net/map/G_p31/'

        # propUrl = 'http://jbk.39.net/xqjy/jb/'
        # endPath = propUrl.split("/")[-2]
        # Url = propUrl.split('/'+endPath+'/')[0] + '/'
        # print(Url)

        connection = pymongo.MongoClient('mongodb://localhost:27017')
        db = connection['disease_v2']
        self.collection = db['info']
        # self.getList(self.url)

        # resultsCount = self.collection.count()
        # for skipNum in range(0, resultsCount, 20):
        #     results = self.collection.find().skip(skipNum).limit(20)
        #     for result in results:
        #         jbzsUrl = result['Url'] + 'jbzs/'
        #         self.getDetail(jbzsUrl)

        # 测试
        # self.getDetail('http://jbk.39.net/gxy/jbzs/')
        # self.getDetail('http://jbk.39.net/gxy/zztz/')
        # self.getDetail('http://jbk.39.net/gxy/blby/')
        # self.getDetail('http://jbk.39.net/gxy/yfhl/')
        # self.getDetail('http://jbk.39.net/gxy/jb/')
        # self.getDetail('http://jbk.39.net/xtxzgjrh/yyzl/')
        # self.getDetail('http://jbk.39.net/gxy/hl/')
        # self.getDetail('http://jbk.39.net/gxy/ysbj/')
        # self.getDetail('http://jbk.39.net/gxy/bfbz/')

        diseaseUrls = ['http://jbk.39.net/brk/']
        categories = ['jbzs/', 'zztz/', 'blby/', 'yfhl/', 'jb/', 'yyzl/', 'hl/', 'ysbj/', 'bfbz/']
        for diseaseUrl in diseaseUrls:
            for category in categories:
                tempUrl = diseaseUrl + category
                self.getDetail(tempUrl)

    def getList(self, url):
        print('分页========' + url)
        logger.info('current page:' + url)
        ua = random.choice(self.user_agent_list)
        if ua:
            # 设置headers
            header = {
                "User-Agent": ua
            }
        response = requests.get(url, headers=header)
        html = response.content
        html_doc = str(html, 'gbk')
        soup = BeautifulSoup(html_doc, 'lxml')

        # 匹配详情页url
        try:
            siteUl = soup.find('ul', class_='site-list')
            urls = siteUl.find_all('li')
            for liUrl in urls:
                propUrl = liUrl.find('a', href=True)['href']
                if '/jbzs/' in propUrl:
                    # print('疾病简介：%s' % propUrl)
                    self.getDetail(propUrl)
                elif '/zztz/' in propUrl:
                    # print('典型症状：%s' % propUrl)
                    self.getDetail(propUrl)
                elif '/blby/' in propUrl:
                    # print('发病原因：%s' % propUrl)
                    self.getDetail(propUrl)
                elif '/yfhl/' in propUrl:
                    # print('预防：%s' % propUrl)
                    self.getDetail(propUrl)
                # elif '/jcjb/' in propUrl:
                    # print('临床检查：%s' % propUrl)
                    # self.getDetail(propUrl)
                elif '/jb/' in propUrl:
                    # print('鉴别：%s' % propUrl)
                    self.getDetail(propUrl)
                elif '/yyzl/' in propUrl:
                    # print('治疗方法：%s' % propUrl)
                    self.getDetail(propUrl)
                elif '/hl/' in propUrl:
                    # print('护理：%s' % propUrl)
                    self.getDetail(propUrl)
                elif '/ysbj/' in propUrl:
                    # print('饮食保健：%s' % propUrl)
                    self.getDetail(propUrl)
                elif '/bfbz/' in propUrl:
                    # print('并发症：%s' % propUrl)
                    self.getDetail(propUrl)
        except Exception as e:
            logger.info(url)
            logger.info("=======匹配详情页url======")
            logger.info(e)


        # 下一页列表
        try:
            PageUrls = soup.find_all('a', class_='sp-a', href=True)
            for pageurl in PageUrls:
                if "下页" in pageurl.text:
                    nextPageUrl = pageurl['href']
            # print('http://jbk.39.net' + nextPageUrl)
            # driver.quit()
            self.getList('http://jbk.39.net' + nextPageUrl)
        except Exception as e:
            logger.info(url)
            logger.info("=======匹配下一页url======")
            logger.info(e)
        # driver.quit()


    # 提取各疾病属性的数据
    def getDetail(self, propUrl):
        # 介绍：Intro
        # 是否属于医保：MedicalInsurance
        # 别名：Alias
        # 发病部位：Lesions
        # 传染性：Contagion
        # 多发人群：MultiplePopulation
        # 相关症状：RelatedSymptoms
        # 并发疾病：ConcurrentDisease
        # 就诊科室：ClinicDepartment
        # 治疗费用：TreatmentExpense
        # 治愈率：CureRate
        # 治疗周期：TreatmentCycle
        # 治疗方法：TherapeuticMethod
        # 相关检查：CorrelationExamination
        # 常用药品：CommonlyUsedDrugs
        # 传播途径：RouteOfTransmission
        # 潜伏期：Incubation
        # 潜伏期表现：LatentPeriodSymptom

        # 最佳就诊时间：BestVisitTime
        # 就诊时长：LengthOfVisit
        # 复诊频率 / 诊疗周期：FrequencyOfRevisit
        # 就诊前准备：PreMedicalPreparation

        print(propUrl)
        ua = random.choice(self.user_agent_list)
        if ua:
            # 设置headers
            header = {
                "User-Agent": ua
            }
        response = requests.get(propUrl, headers=header)
        html = response.content
        html_doc = str(html, 'gbk')
        soup = BeautifulSoup(html_doc, 'lxml')

        # 分割URL
        endPath = propUrl.split("/")[-2]
        Url = propUrl.split('/' + endPath + '/')[0] + '/'

        if '/jbzs/' in propUrl:
            # 疾病简介
            item = {
                'Url': Url,
                'Name': '',
                'Summary': {
                    'Intro': '',
                    'MedicalInsurance': '',
                    'Alias': [],
                    'Lesions': [],
                    'Contagion': '',
                    'RouteOfTransmission': '',
                    'Incubation': '',
                    'LatentPeriodSymptom': '',
                    'MultiplePopulation': '',
                    'CommonlyUsedDrugs': []
                }
            }

            try:
                item["Name"] = soup.find('h1').string
                intro = soup.find('dl', class_='intro').find('dd').string
                item["Summary"]["Intro"] = self.filter_tags_blank(intro)
            except Exception as e:
                logger.info(propUrl)
                logger.info('=========简介=======')
                logger.info(e)
            try:
                infos = soup.find('div', class_='chi-know').find_all('dl', class_='info')
                for info in infos:
                    dds = info.find_all('dd')
                    for dd in dds:
                        ddi = dd.find('i')
                        if ddi is not None:
                            propName = dd.find('i').string
                            if "是否属于医保：" in propName:
                                item["Summary"]["MedicalInsurance"] = self.filter_tags_blank(str(dd)).split("是否属于医保：")[1]
                            elif "别名：" in propName:
                                aliasList = self.filter_tags_blank(str(dd)).split("别名：")[1].split("，")
                                for alias in aliasList:
                                    item["Summary"]["Alias"].append(alias)
                            elif "发病部位：" in propName:
                                lesions_label = dd.find_all('a')
                                for lesions_a in lesions_label:
                                    item["Summary"]["Lesions"].append(lesions_a.string)
                            elif "传染性：" in propName:
                                item["Summary"]["Contagion"] = self.filter_tags_blank(str(dd)).split("传染性：")[1]
                            elif "传播途径：" in propName:
                                item["Summary"]["RouteOfTransmission"] = self.filter_tags_blank(str(dd)).split("传播途径：")[1]
                            elif "潜伏期：" in propName:
                                item["Summary"]["Incubation"] = self.filter_tags_blank(str(dd)).split("潜伏期：")[1]
                            elif "潜伏期表现：" in propName:
                                item["Summary"]["LatentPeriodSymptom"] = self.filter_tags_blank(str(dd)).split("潜伏期表现：")[1]
                            elif "多发人群：" in propName:
                                item["Summary"]["MultiplePopulation"] = self.filter_tags_blank(str(dd)).split("多发人群：")[1]
                            # elif "就诊科室：" in propName:
                            #     clinic_label = dd.find_all('a')
                            #     for clinic_a in clinic_label:
                            #         item["Summary"]["ClinicDepartment"].append(clinic_a.string)
                            # elif "治疗费用：" in propName:
                            #     item["Summary"]["TreatmentExpense"] = self.filter_tags_blank(str(dd)).split("治疗费用：")[1]
                            # elif "治愈率：" in propName:
                            #     item["Summary"]["CureRate"] = self.filter_tags_blank(str(dd)).split("治愈率：")[1]
                            # elif "治疗周期：" in propName:
                            #     item["Summary"]["TreatmentCycle"] = self.filter_tags_blank(str(dd)).split("治疗周期：")[1]
                            # elif "治疗方法：" in propName:
                            #     method_label = self.filter_tags_blank(str(dd.find('a'))).split('、')
                            #     for method_a in method_label:
                            #         item["Summary"]["TherapeuticMethod"].append(method_a)
                            # elif "相关检查：" in propName:
                            #     exam_label = dd.find_all('a')
                            #     for exam_a in exam_label:
                            #         if exam_a.string.find("详细") < 0:
                            #             item["Summary"]["CorrelationExamination"].append(exam_a.string)
                            elif "常用药品：" in propName:
                                drug_label = dd.find_all('a', href=True)
                                for drug_a in drug_label:
                                    if drug_a.string.find("详细") < 0:
                                        item["Summary"]["CommonlyUsedDrugs"].append(drug_a['href'])
                                        # item["Summary"]["CommonlyUsedDrugs"].append(drug_a.string)

                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info('========基本信息======')
                logger.info(e)
        elif '/zztz/' in propUrl:
            # 典型症状
            item = {
                'Url': Url,
                'Symptom': {
                    'EarlySymptom': '',
                    'AdvancedSymptom': '',
                    'RelatedSymptoms': [],
                    'TypicalSymptoms': '',
                    'SymptomDescription': '',
                    'SymptomDescriptionTag': ''
                }
            }
            try:
                symptoms = soup.find('dl', class_="links").find_all('dd')
                for symp_dd in symptoms:
                    symp_name = symp_dd.find('i').string
                    if "早期症状：" in symp_name:
                        item["Symptom"]["EarlySymptom"] = self.filter_tags_blank(str(symp_dd)).split("早期症状：")[1]
                    elif "晚期症状：" in symp_name:
                        item["Symptom"]["AdvancedSymptom"] = self.filter_tags_blank(str(symp_dd)).split("晚期症状：")[1]
                    elif "相关症状：" in symp_name:
                        related_symps = symp_dd.find_all('a')
                        for each_related in related_symps:
                            item["Symptom"]["RelatedSymptoms"].append(each_related.string)
                    elif "典型症状：" in symp_name:
                        item["Symptom"]["TypicalSymptoms"] = self.filter_tags_blank(str(symp_dd)).split("典型症状：")[1]
                SymptomDescription = soup.find('div', class_="art-box")
                item["Symptom"]["SymptomDescriptionTag"] = str(SymptomDescription)
                item["Symptom"]["SymptomDescription"] = self.filter_tags_blank(str(SymptomDescription))
                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======典型症状======")
                logger.info(e)
        elif '/blby/' in propUrl:
            # 发病原因
            item = {
                'Url': Url,
                'Cause': {
                    'CauseOfDisease': '',
                    'CauseOfDiseaseTag': ''
                }
            }
            try:
                CauseOfDisease = soup.find('div', class_="art-box")
                item["Cause"]["CauseOfDiseaseTag"] = str(CauseOfDisease)
                item["Cause"]["CauseOfDisease"] = self.filter_tags_blank(str(CauseOfDisease))
                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======发病原因======")
                logger.info(e)
        elif '/yfhl/' in propUrl:
            # 预防
            item = {
                'Url': Url,
                'Prevention': {
                    'DiseasePrevention': '',
                    'DiseasePreventionTag': ''
                }
            }
            try:
                DiseasePrevention = soup.find('div', class_="art-box")
                item["Prevention"]["DiseasePreventionTag"] = str(DiseasePrevention)
                item["Prevention"]["DiseasePrevention"] = self.filter_tags_blank(str(DiseasePrevention))
                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======预防======")
                logger.info(e)
        elif '/jcjb/' in propUrl:
            print('临床检查：%s' % propUrl)
        elif '/jb/' in propUrl:
            # 鉴别
            item = {
                'Url': Url,
                'Identify': {
                    'IdentifyDisease': '',
                    'IdentifyDiseaseTag': ''
                }
            }
            try:
                Identify = soup.find('div', class_="art-box")
                item["Identify"]["IdentifyDiseaseTag"] = str(Identify)
                item["Identify"]["IdentifyDisease"] = self.filter_tags_blank(str(Identify))
                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======鉴别======")
                logger.info(e)
        elif '/yyzl/' in propUrl:
            # 治疗方法
            # 就诊科室：ClinicDepartment
            # 治疗费用：TreatmentExpense
            # 治愈率：CureRate
            # 治疗周期：TreatmentCycle
            # 治疗方法：TherapeuticMethod
            item = {
                'Url': Url,
                'Treatment': {
                    'ClinicDepartment': [],
                    'TreatmentExpense': '',
                    'CureRate': '',
                    'TreatmentCycle': '',
                    'TherapeuticMethod': [],
                    'TreatmentBox': '',
                    'TreatmentBoxTag': ''
                }
            }
            try:
                info_dds = soup.find('dl', class_="info").find_all('dd')
                for info_dd in info_dds:
                    info_label = info_dd.find('i').string
                    if "就诊科室：" in info_label:
                        try:
                            dep_a = info_dd.find_all('a')
                            for each_dep in dep_a:
                                item['Treatment']['ClinicDepartment'].append(self.filter_tags_blank(each_dep.string))
                        except Exception as e:
                            logger.info(propUrl)
                            logger.info("======就诊科室=====")
                            logger.info(e)
                    elif "治疗费用：" in info_label:
                        try:
                            item['Treatment']['TreatmentExpense'] = self.filter_tags_blank(str(info_dd)).split("治疗费用：")[1]
                        except Exception as e:
                            logger.info(propUrl)
                            logger.info("======治疗费用=====")
                            logger.info(e)
                    elif "治愈率：" in info_label:
                        try:
                            item['Treatment']['CureRate'] = self.filter_tags_blank(str(info_dd)).split("治愈率：")[1]
                        except Exception as e:
                            logger.info(propUrl)
                            logger.info("======治愈率=====")
                            logger.info(e)
                    elif "治疗周期：" in info_label:
                        try:
                            item['Treatment']['TreatmentCycle'] = self.filter_tags_blank(str(info_dd)).split("治疗周期：")[1]
                        except Exception as e:
                            logger.info(propUrl)
                            logger.info("======治疗周期=====")
                            logger.info(e)
                    elif "治疗方法：" in info_label:
                        try:
                            method_a = self.filter_tags_blank(str(info_dd)).split("治疗方法：")[1]
                            methods = method_a.split("、")
                            for each_method in methods:
                                item['Treatment']['TherapeuticMethod'].append(each_method)
                        except Exception as e:
                            logger.info(propUrl)
                            logger.info("======治疗方法=====")
                            logger.info(e)
                try:
                    TreatmentBox = soup.find('div', class_="art-box")
                    item['Treatment']['TreatmentBoxTag'] = str(TreatmentBox)
                    item['Treatment']['TreatmentBox'] = self.filter_tags_blank(str(TreatmentBox))
                except Exception as e:
                    logger.info(propUrl)
                    logger.info("======治疗介绍=====")
                    logger.info(e)
                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======治疗======")
                logger.info(e)
        elif '/hl/' in propUrl:
            # 护理
            item = {
                'Url': Url,
                'DiseaseCare': {
                    'Nursing': '',
                    'NursingTag': ''
                }
            }
            try:
                Nursing = soup.find('div', class_="art-box")
                item['DiseaseCare']['NursingTag'] = str(Nursing)
                item['DiseaseCare']['Nursing'] = self.filter_tags_blank(str(Nursing))
                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======护理======")
                logger.info(e)
        elif '/ysbj/' in propUrl:
            # 饮食保健
            # 适宜：EatFood
            # 禁忌：DietTaboo
            # 饮食原则：Guideline
            # 吃什么好：WhatToEat
            # 食疗偏方：Dietotherapy
            item = {
                'Url': Url,
                'DietaryHealth': {
                    'EatFood': {
                        'Description': '',
                        'Foods': []
                    },
                    'DietTaboo': {
                        'Description': '',
                        'Foods': []
                    },
                    'GuidelineBoxTag': '',
                    'Guideline': '',
                    'WhatToEat': '',
                    'Dietotherapy': ''
                }
            }
            # 饮食宜忌
            try:
                yinshi_table = soup.find('div', class_="yinshi_table")
                yinshi_title = yinshi_table.find_all('div', class_="yinshi_title")
                for each_title in yinshi_title:
                    if "饮食适宜：" in each_title.string:
                        item['DietaryHealth']['EatFood']['Description'] = self.filter_tags_blank(each_title.string)
                        shiyi_trs = yinshi_table.find_all('table')[0].find('tbody').find_all('tr')
                        for index,shiyi_tr in enumerate(shiyi_trs):
                            if index > 0:
                                temp_shiyi = {}
                                cur_tds = shiyi_tr.find_all('td')
                                temp_shiyi['Name'] = self.filter_tags_blank(str(cur_tds[0]))
                                temp_shiyi['Reason'] = self.filter_tags_blank(str(cur_tds[1]))
                                temp_shiyi['Suggestion'] = self.filter_tags_blank(str(cur_tds[2]))
                                item['DietaryHealth']['EatFood']['Foods'].append(temp_shiyi)
                    elif "饮食禁忌：" in each_title.string:
                        item['DietaryHealth']['DietTaboo']['Description'] = self.filter_tags_blank(each_title.string)
                        jinji_trs = yinshi_table.find_all('table')[1].find('tbody').find_all('tr')
                        for index, jinji_tr in enumerate(jinji_trs):
                            if index > 0:
                                temp_jinji = {}
                                curr_tds = jinji_tr.find_all('td')
                                temp_jinji['Name'] = self.filter_tags_blank(str(curr_tds[0]))
                                temp_jinji['Reason'] = self.filter_tags_blank(str(curr_tds[1]))
                                temp_jinji['Suggestion'] = self.filter_tags_blank(str(curr_tds[2]))
                                item['DietaryHealth']['DietTaboo']['Foods'].append(temp_jinji)
                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======饮食宜忌======")
                logger.info(e)

            # 饮食原则
            try:
                try:
                    guidelineBox = soup.find_all('div', class_="art-box")[1]
                except Exception as e:
                    try:
                        guidelineBox = soup.find_all('div', class_="art-box")[0]
                    except Exception as e:
                        logger.info(propUrl)
                        logger.info('=====饮食原则介绍====')
                        logger.info(e)
                item['DietaryHealth']['GuidelineBoxTag'] = str(guidelineBox)
                try:
                    Guideline = []
                    for eatline in guidelineBox:
                        if 'links' in str(eatline) and '饮食原则' in str(eatline):
                            StrGuideline = ''.join(Guideline)
                            if '饮食原则' in StrGuideline:
                                item['DietaryHealth']['Guideline'] = self.filter_tags_blank(StrGuideline)
                            elif '吃什么好' in StrGuideline:
                                item['DietaryHealth']['WhatToEat'] = self.filter_tags_blank(StrGuideline)
                            elif '食疗偏方' in StrGuideline:
                                item['DietaryHealth']['Dietotherapy'] = self.filter_tags_blank(StrGuideline)
                            Guideline.clear()
                            Guideline.append(str(eatline))
                        elif 'links' in str(eatline) and '吃什么好' in str(eatline):
                            StrGuideline = ''.join(Guideline)
                            if '饮食原则' in StrGuideline:
                                item['DietaryHealth']['Guideline'] = self.filter_tags_blank(StrGuideline)
                            elif '吃什么好' in StrGuideline:
                                item['DietaryHealth']['WhatToEat'] = self.filter_tags_blank(StrGuideline)
                            elif '食疗偏方' in StrGuideline:
                                item['DietaryHealth']['Dietotherapy'] = self.filter_tags_blank(StrGuideline)
                            Guideline.clear()
                            Guideline.append(str(eatline))
                        elif 'links' in str(eatline) and '食疗偏方' in str(eatline):
                            StrGuideline = ''.join(Guideline)
                            if '饮食原则' in StrGuideline:
                                item['DietaryHealth']['Guideline'] = self.filter_tags_blank(StrGuideline)
                            elif '吃什么好' in StrGuideline:
                                item['DietaryHealth']['WhatToEat'] = self.filter_tags_blank(StrGuideline)
                            elif '食疗偏方' in StrGuideline:
                                item['DietaryHealth']['Dietotherapy'] = self.filter_tags_blank(StrGuideline)
                            Guideline.clear()
                            Guideline.append(str(eatline))
                        else:
                            Guideline.append(str(eatline))
                    StrGuideline = ''.join(Guideline)
                    if '饮食原则' in StrGuideline:
                        item['DietaryHealth']['Guideline'] = self.filter_tags_blank(StrGuideline)
                    elif '吃什么好' in StrGuideline:
                        item['DietaryHealth']['WhatToEat'] = self.filter_tags_blank(StrGuideline)
                    elif '食疗偏方' in StrGuideline:
                        item['DietaryHealth']['Dietotherapy'] = self.filter_tags_blank(StrGuideline)
                    # print(item['DietaryHealth']['Guideline'])
                    # print(item['DietaryHealth']['WhatToEat'])
                    # print(item['DietaryHealth']['Dietotherapy'])
                    # print(item)
                except Exception as e:
                    logger.info(propUrl)
                    logger.info('=======yuanze======')
                    logger.info(e)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======饮食原则======")
                logger.info(e)
        elif '/bfbz/' in propUrl:
            # 并发症
            # 并发疾病：ConcurrentDisease
            # 并发症：ComplicationBox
            item = {
                'Url': Url,
                'Complication': {
                    'ConcurrentDisease': [],
                    'ComplicationBox': '',
                    'ComplicationBoxTag': ''
                }
            }
            try:
                concurrents = soup.find('dl', class_="links").find('dd').find_all('a')
                for each_cur in concurrents:
                    item['Complication']['ConcurrentDisease'].append(each_cur.string)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======并发症======")
                logger.info(e)
            try:
                ComplicationBox = soup.find('div', class_="art-box")
                item['Complication']['ComplicationBoxTag'] = str(ComplicationBox)
                item['Complication']['ComplicationBox'] = self.filter_tags_blank(str(ComplicationBox))
                # print(item)
            except Exception as e:
                logger.info(propUrl)
                logger.info("=======并发症描述======")
                logger.info(e)
        self.saveMongo(item, propUrl)


    def saveMongo(self, item, propUrl):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if '/jbzs/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'Name': item.get('Name'),
                        'Summary': item.get('Summary'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        elif '/zztz/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'Symptom': item.get('Symptom'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        elif '/blby/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'Cause': item.get('Cause'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        elif '/yfhl/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'Prevention': item.get('Prevention'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        elif '/jcjb/' in propUrl:
            print("======检查待定=====")
        elif '/jb/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'Identify': item.get('Identify'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        elif '/yyzl/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'Treatment': item.get('Treatment'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        elif '/hl/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'DiseaseCare': item.get('DiseaseCare'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        elif '/ysbj/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'DietaryHealth': item.get('DietaryHealth'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        elif '/bfbz/' in propUrl:
            self.collection.update_one(
                {'Url': item['Url']},
                {
                    "$set": {
                        'Complication': item.get('Complication'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )


    # 去掉html标签和空格
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())


if __name__ == '__main__':
    try:
        getJbk()
    except Exception as e:
        print(str(e))
