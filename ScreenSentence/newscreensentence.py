import numpy as np
import pandas as pd


path = r"E:\GMWork\AIRobot\8种体质\体质数据\体质数据"
temp_path = r"\气虚质问答.xls"
filepath = path + temp_path

df = pd.read_excel(filepath, header=None)
df.head()
df.tail()


def screen(x):
    screensentence = ["脾胃", "早泄", "气虚", "脾气", "治疗", "月经", "厌食", "咳嗽"]
    for i in screensentence:
        if i in x:
            return True
    else:
        return False


df["flag"] = df.loc[:,0].apply(screen)
df2 = df.loc[df.flag==True, :].drop_duplicates(subset=[0])
df2.to_excel(path+"/test11.xlsx", index=False)
len(df2.loc[:,0].value_counts())
print(df2.shape)

