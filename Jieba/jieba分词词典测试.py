# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 09:15:51 2018

@author: Hsiaofei Tsien
"""

#%%
import jieba
import os
import pandas as pd

jieba.set_dictionary(r"D:\GMWork\分词与词向量\分词词典库\jieba.dict.txt.big")

#%% 挂载额外的词库

dict_path = r"D:\GMWork\分词与词向量\分词词典库/外挂词典/"
files = os.listdir(dict_path)
for file in files:
    jieba.load_userdict(dict_path+file)
jieba.initialize()
#%%
path = r"D:\GMWork\分词与词向量\体质数据\气郁质问答.xls"
path = r"D:\GMWork\分词与词向量\体质数据\湿热质问答.xls"
path = r"D:\GMWork\高血压(1).xlsx"
df = pd.read_excel(path,header=None)
#%%
df[2] = df[0].map(str) + df[1].map(str)
df["2_split"] = df[2].apply(jieba.lcut)


#%%
while True:
    for i in range(len(df))[:]:
        print(i)
        print(df.iloc[i,2])
        print()
        print(df.iloc[i,3])
        out = input()
        if out == "0":
            break
    break


#%%
from functools import reduce
res = set([*reduce(lambda x,y:x+y,df["2_split"])])
len(res)
res
#%%
import os
files = os.listdir(r"D:\Downloads\医疗词库")

#%%
all_data = set()
for file in files:
    with open(r"D:\Downloads\医疗词库/" + file,encoding="utf8") as fo:
        data = set(fo.read().split())
        all_data.update(data)
len(all_data)
with open(r"D:\Downloads\医疗.txt","w",encoding="utf8") as file:
    for i in all_data:
        file.write(i+"\n")
