#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/7/12'

__QQ__ = '376205871'

"""

import pymongo
from datetime import datetime

class MongodbToPC(object):
    def __init__(self):
        # 本地mongodb
        connection = pymongo.MongoClient('mongodb://localhost:27017')
        db = connection['tizhi']
        self.collection = db['xueyuzhi']

        # pc端mongodb
        remote_connection = pymongo.MongoClient('mongodb://192.168.1.15:27017')
        remote_db = remote_connection['tizhi']
        self.remote_collection = remote_db['xueyuzhi']
        self.getMongodb()

    def getMongodb(self):
        resultsCount = self.collection.count()
        for skipNum in range(0, resultsCount, 200):
            results = self.collection.find().skip(skipNum).limit(200)
            print(skipNum)
            for result in results:
                self.saveRemoteMongodb(result)

    def saveRemoteMongodb(self, item):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 食品库
        # try:
        #     self.remote_collection.update_one(
        #         {'url': item['url']},
        #         {
        #             "$set": {
        #                 'name': item.get('name'),
        #                 'foodPic': item.get('foodPic'),
        #                 'alias': item.get('alias'),
        #                 'category': item.get('category'),
        #                 'message': item.get('message'),
        #                 'nutritionTags': item.get('nutritionTags'),
        #                 'nutritionUnit': item.get('nutritionUnit'),
        #                 'widgetUnit': item.get('widgetUnit'),
        #                 'material': item.get('material'),
        #                 'practice': item.get('practice'),
        #                 'url': item.get('url'),
        #                 'update_time': cur_time
        #             }
        #         },
        #         upsert=True
        #     )
        # except Exception as e:
        #     print("======保存pc出错=====")
        #     print(e)

        # 资讯文章
        # try:
        #     self.remote_collection.update_one(
        #         {'url': item['url']},
        #         {
        #             "$set": {
        #                 'title': item.get('title'),
        #                 'content': item.get('content'),
        #                 'url': item.get('url'),
        #                 'category': item.get('category'),
        #                 'update_time': cur_time
        #             }
        #         },
        #         upsert=True
        #     )
        # except Exception as e:
        #     print("======保存pc出错=====")
        #     print(e)

        # 问答
        try:
            self.remote_collection.update_one(
                {'url': item['url']},
                {
                    "$set": {
                        'question': item.get('question'),
                        'answer': item.get('answer'),
                        'url': item.get('url'),
                        'update_time': cur_time
                    }
                },
                upsert=True
            )
        except Exception as e:
            print("======保存pc出错=====")
            print(e)

        # 药品库
        # try:
        #     self.remote_collection.update_one(
        #         {'ApprovalNumber': item['ApprovalNumber']},
        #         {
        #             "$set": {
        #                 'Url': item.get('Url'),
        #                 'ImgUrl': item.get('ImgUrl'),
        #                 'DosageForm': item.get('DosageForm'),
        #                 'Specifications': item.get('Specifications'),
        #                 'PrescribedDrug': item.get('PrescribedDrug'),
        #                 'ApprovalNumber': item.get('ApprovalNumber'),
        #                 'ApprovalDate': item.get('ApprovalDate'),
        #                 'DrugNames': item.get('DrugNames'),
        #                 'Composition': item.get('Composition'),
        #                 'Indications': item.get('Indications'),
        #                 'DosageAndAdministration': item.get('DosageAndAdministration'),
        #                 'AdverseReactions': item.get('AdverseReactions'),
        #                 'Contraindications': item.get('Contraindications'),
        #                 'Precautions': item.get('Precautions'),
        #                 'SpecialDrugUse': item.get('SpecialDrugUse'),
        #                 'Interactions': item.get('Interactions'),
        #                 'PharmacologicalActions': item.get('PharmacologicalActions'),
        #                 'Storage': item.get('Storage'),
        #                 'Validity': item.get('Validity'),
        #                 'RevisionDate': item.get('RevisionDate'),
        #                 'ManufacturingEnterprise': item.get('ManufacturingEnterprise'),
        #                 "DrugCategory": item.get("DrugCategory"),
        #                 "DrugProperties": item.get("DrugProperties"),
        #                 "MedicalInsurance": item.get("MedicalInsurance"),
        #                 'update_time': cur_time
        #             }
        #         },
        #         upsert=True
        #     )
        # except Exception as e:
        #     print("======保存pc出错=====")
        #     print(e)


if __name__ == '__main__':
    try:
        MongodbToPC()
    except Exception as e:
        print(str(e))
