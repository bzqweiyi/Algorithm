# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 16:02:30 2018

Author: Hsiaofei Tsien

Email: Hsiaofei.Tsien@foxmail.com
"""
#%%
import numpy as np
import pandas as pd
import jieba

import pickle
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle


#%%

path_5k = r"D:\GMWork\高血压_clean汇总(2).xlsx"
df = pd.read_excel(path_5k,header=None)
df = df.loc[df[2].notnull() & df[1].notnull()]
# df.fillna("",inplace=True)
# df.reset_index(inplace=True,drop=True)
df = shuffle(df)

#%%
path_word2vec = r"D:\Downloads\Compressed\wiki.zh\wiki.zh.vec"
with open(path_word2vec,encoding="utf8") as file:
    print(file.readline())
    Vdata = [x.split() for x in file.readlines()]


dict_word2vec = {v[0]:np.array([*map(float,v[1:-1])]) for v in Vdata}

def get_sent_vec(li):
    data = [dict_word2vec.get(i,np.array([np.nan]*300)) for i in li]
    res = np.nanmean(data,axis=0)
    if np.isnan(res[0]):
        return np.array([0]*300)
    return res
#%%
label2id = {k:v for v,k in enumerate(df[1].value_counts().index)}
id2label = {v:k for k,v in label2id.items()}
df["label"] = df[1].map(label2id)
# df["text"] = df.iloc[:,3] + df.iloc[:,4]
df["text"] = df.iloc[:,2]

df["split_text"] = df.text.apply(jieba.lcut)

df["set_vec"] = df.split_text.apply(get_sent_vec)


#%%
data = np.array([list(i) for i in df["set_vec"]])
y = df.label
model = RandomForestClassifier(class_weight="balanced",
                               max_depth=20)

# X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.33)
# model.fit(X_train, y_train)
model.fit(data[:3500], y[:3500])
#%%
#pred = model.predict(X_test)
#print(np.mean(y_test==pred))

pred = model.predict(data[3500:])
print(np.mean(y[3500:]==pred))

Counter(pred)
#%%
df.loc[[False]*3500 + list(pred == 2),[1,2]]

# {0: '疾病诊疗', 1: '症状', 2: '疾病介绍', 3: '预防', 4: '病因', 5: '检查'}


get_pred("什么是高血压")
get_pred("早上血压140/90")


#%%
def get_pred(text):
    text_split = jieba.lcut(text)
    text_vec = get_sent_vec(text_split).reshape(1,300)

    return id2label[model.predict(text_vec)[0]]


