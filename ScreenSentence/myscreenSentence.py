# coding: utf-8
# James
# 20180905
import numpy as np
import pandas as pd

def screenManbingSentence(values):
    gm = []
    for keyWord in gm:
        if keyWord in values:
            return True
    else:
        return False

def screenTizhiSentence(values):
    phz= []
    qxz = ["脾胃", "早泄", "气虚", "脾气", "治疗", "月经", "厌食", "咳嗽"]
    qyx = []
    srz = []
    tsz = []
    tbz = []
    xyz = []
    yangxz = ["早泄", "女性", "中成药", "调理", "怕冷", "中医", "阳虚", "肾阴虚", "寒性",\
              "症状", "脾虚", "肾阳虚", "手淫", "手脚冰凉", "治疗", "阳痿", "肾虚"]
    yinxz = ["阴虚内", "出汗", "耳鸣", "发热", "上火", "调理", "盗汗", "肾阴虚", "阴虚", \
             "湿热", "症状", "怎么回事", "火旺", "失眠", "体质", "阴虚阳", "治疗", "身体"]
    for keyWord in yangxz:
        if keyWord in values:
            return True
    else:
        return False

def randomExcelandSave(path, finalpath):
    df = pd.read_excel(path, header=None)
    df = df.sample(frac=1)
    df.to_excel(finalpath, header=None)

if __name__ == "__main__":
    try:
        gen_path = r"E:\GMWork\AIRobot\KeyWords"
        com_path = r"E:\GMWork\AIRobot"
        man_path = r"E:\GMWork\02 AIRobot\12种慢病"
        man_final_path = r"E:\GMWork\02 AIRobot\12种慢病\乱序12种慢病"
        tizhi_paths = [r"\平和质问答.xls", r"\气虚质问答.xls", r"\气郁质问答.xls",
                     r"\湿热质问答.xls", r"\痰湿质问答.xls", r"\特禀质问答.xls",
                     r"\血瘀质问答.xls", r"\阳虚质问答.xls", r"\阴虚质问答.xls"]
        manbing_paths = [r"\痴呆.xls", r"\感冒.xlsx", r"\高血压.xlsx",
                         r"\高血脂.xls", r"\冠心病.xls", r"\颈椎病.xls",
                         r"\咳嗽.xlsx", r"\糖尿病.xlsx", r"\痛风.xls",
                         r"\腰腿疼.xls", r"\脂肪肝.xls", r"\中风.xls"]
        firstpath = [r"\痴呆.xls", r"\感冒.xlsx", r"\高血压.xlsx",
                         r"\高血脂.xls", r"\冠心病.xls", r"\颈椎病.xls",
                         r"\咳嗽.xlsx", r"\糖尿病.xlsx", r"\痛风.xls",
                         r"\腰腿疼.xls", r"\脂肪肝.xls", r"\中风.xls"]
        for i in range(0, len(firstpath)):
            randomExcelandSave(man_path + manbing_paths[i], man_final_path + manbing_paths[i])
    except Exception as ex:
        print(ex)
"""
        manbing_path = r"\12种慢病" + manbing_paths[1]
        tizhi_path = r"\8种体质" + tizhi_paths[7]
        path = com_path + tizhi_path
        df = pd.read_excel(path, header=None)
        # generate tizhi report
        df["flag"] = df.loc[:, 0].apply(screenTizhiSentence)
        # gene manbing report. when you need it.
        # df["flag"] = df.loc[:, 0].apply(screenManbingSentence)
        df2 = df.loc[df.flag == True, :].drop_duplicates(subset=[0])
        df2.to_excel(gen_path + r"\阳虚_20180906.xlsx", index=False)
    except Exception as ex:
        print(ex)
"""
# df为需要筛选的数据框，col为选择非空依赖的列
# df[(df[:, 0].notnull)==True & (df[:, 0] != "")]
# df["flag"] = df.loc[:, 0].apply(screenSentence)
# df.dropna(axis=1, how='any', inplace=True)
# df["flag"] = df[(True - df.loc[:, 0])].isin("").apply(screenSentence)
# df.dropna(axis=0, how='any', inplace=True)
# temp = df.loc[:, 0].notnull()
# df[df.loc[0]]
# df.loc[:, 0] = df.loc[:, 0].fillna('9999')
# df[(df[:, 0] == '9999')].index.tolist()
# df.fillna(value=19900921)













