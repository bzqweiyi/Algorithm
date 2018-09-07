# coding:utf-8
import numpy as np
import pandas as pd
path = r"E:\GMWork\AIRobot\12种慢病\感冒.xlsx"
df = pd.read_excel(path, header=None)

def screen(x):
    screensentence = ["喉咙", "孩子", "哺乳期", "感冒药", "咳嗽", "嗓子疼", "晚上", "四肢", \
              "打喷嚏", "鼻子", "喉咙痛", "鼻涕", "流清", "发炎", "无力", "疼痛", \
              "低烧", "严重", "酸痛", "头痛", "扁桃体", "发热", "感冒", "嗓子", \
              "鼻塞", "流鼻涕", "咽喉", "难受", "头晕", "发烧", "干咳"]
    for i in screensentence:
        if i in x:
            return True
    else:
        return False

df["flag"] = df.loc[:,0].apply(screen)
df2 = df.loc[df.flag==True, :].drop_duplicates(subset=[0])
df2.to_excel(r"E:\GMWork\AIRobot\12种慢病\KeyWords\感冒数据.xlsx", index=False)

