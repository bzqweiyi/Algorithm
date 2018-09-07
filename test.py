# This is for pandas common using method.
# James
# 20180905
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

path = r"E:\GMWork\AIRobot\8种体质\体质数据\体质数据\KeyWords"
df = pd.read_excel(path + r"\tt.xlsx")
# 1、维度查看：
df.shape
# 2、数据表基本信息（维度、列名称、数据格式、所占空间等）：
df.info()
# 3、每一列数据的格式：
df.dtypes
# 4、某一列格式： ??
df['D'].dtype
# 5、空值
df.isnull
# 6、查看某一列空值：
df.isnull()
# 7、查看某一列的唯一值：
df['B'].unique()
# 8、查看数据表的值：
df.values
# 9、查看列名称：
df.columns
# 10、查看前10行数据、后10行数据：
df.head(1000) #默认前10行数据
df.tail(10)    #默认后10 行数据
# This function like random.shuffle
df = df.sample(frac=1)
df = df.fillna(value=0)
df[:3].to_excel(path + r"\ttnew.xlsx", index=False)
# 三、数据表清洗
df['city'] = df['city'].map(str.strip)

df['city'].str.lower()
df['price'].astype('int')
df.rename(columns={'apple': 'appple-pie'})
df['city'].drop_duplicates(keep='last')
df['city'].replace('上海', 'SH')
df['city']

df['price'] = np.where(df['price']>3, 'high', 'low')

df.set_index('price')
df.sort_values(by=['price'])
print('-----------------')
df.loc[3]
df.fillna(value=1)
df.to_excel(path + r"\tt.xlsx",index= False)

'''
print("hello")

# -*- coding: utf-8 -*-
import hashlib
import web

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "gmjk"   #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr.format('utf-8')
            else:
                return ""
        except Exception as Argument:
            return Argument

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
'''