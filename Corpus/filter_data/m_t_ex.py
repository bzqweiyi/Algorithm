#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/23'

__QQ__ = '376205871'

"""

import pymongo
import xlwt


class MongodbToExcel(object):
    def __init__(self):
        # 本地mongodb
        connection = pymongo.MongoClient('mongodb://192.168.1.31')
        db = connection['corpus_distinct']
        self.collection = db['gaoxueya']
        self.total = 0
        self.row = 0
        self.col = 0
        self.rb = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.rb.add_sheet(u'高血压', cell_overwrite_ok=True)
        self.path = r"E:/GMWork/01 Project/corpus-spider/corpus/filter_data/new高血压_60000_MAX.xls"
        self.getMongodb()

    def getMongodb(self):
        resultsCount = self.collection.count()
        # calc = resultsCount - 65537
        # print('total counts: ', calc)
        # newNum = 53481
        for skipNum in range(60000, resultsCount, 20):
            # for skipNum in range(0, 1):

            results = self.collection.find().skip(skipNum).limit(20)
            # print('current num: ', skipNum)
            for result in results:
                # if result['answer'] != '' and len(result['answer']) != 0:
                # if len(result['question']['askText']) > 5 and len(result['question']['askText']) < 11:
                #     if len(result['answer'][0]) < 25:
                self.saveExcel(result)
                print('current steps: ', skipNum)
                print('ramain steps: ', resultsCount - skipNum)

    def saveExcel(self, item):
        self.sheet.write(self.row, 0, item['question']['askText'])
        self.sheet.write(self.row, 1, item['question']['askDesc'])
        # self.sheet.write(self.row, 0, item['question']['askText'])
        self.sheet.write(self.row, 2, item['answer'])
        # self.sheet.write(self.row, 2, item['askDesc'])
        self.rb.save(self.path)
        self.row += 1
        self.total += 1
        print(self.total)


if __name__ == '__main__':
    try:
        MongodbToExcel()
    except Exception as e:
        print(str(e))
