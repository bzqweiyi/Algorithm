# coding:utf-8
# james
# 20180904
import jieba
import jieba.analyse
import xlwt
import xlrd

def readFile(path):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    return table

def generator(table):
    for i in range(1, table.nrows):
        yield table.row_values(i)[0]

def screenSentence(table, screensentence):
    total = 0
    out = []
    temp = generator(table)
    for i in temp:
        count = 0
        seg = jieba.cut(i, cut_all=False)
        for j in seg:
            for k in screensentence:
                if j == k:
                    if count == 0:
                        out.append(i)
                        # print(i)
                        total += 1
                    count += 1
    # print(out)
    print("count:", total)
    return out

def sumAllcolums(out, table):
    temp = 0
    nrows = table.nrows  # get rows
    final_out = []
    tempdata = []
    for i in range(0, len(out)):
        tempdata = out[i]
        count = 0
        for j in range(0, nrows):
            # print(table.row_values(1)[1])
            if out[i] == table.row_values(j)[0]:
                # if count == 0:
                # if temp == 0:
                    data = table.row_values(j)
                    final_out.append(data)
                    # print(i)
                    temp += 1
                # count += 1
                # print(data)
    print("temp", temp)
    print("len(final_out)", len(final_out))
    saveFile(final_out)


# def screenSentence(content):
#     seg_list = jieba.cut(content, cut_all=False)
#     # print("/".join(seg_list))

def saveFile(datas):
    path = r"E:\GMWork\AIRobot\8种体质\体质数据\体质数据\KeyWords"
    temp_path = r"\气虚质筛选结果.xls"
    filepath = path + temp_path
    myExcel = xlwt.Workbook()
    sheet1 = myExcel.add_sheet("气虚", cell_overwrite_ok=True)
    # 将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        for j in range(len(data)):
            sheet1.write(i, j, data[j])
        i += 1
    # for i in range(0, len(value)):
    #     for j in range(len(value[0])):
    #         sheet1.write(i, 0, value[i][j])
    myExcel.save(filepath)


if __name__ == "__main__":
    screensentence = ["脾胃", "早泄", "气虚", "脾气", "治疗", "月经", "厌食", "咳嗽"]
    path = r"E:\GMWork\AIRobot\8种体质\体质数据\体质数据"
    temp_path = r"\气虚质问答.xls"
    filepath = path + temp_path
    try:
        table = readFile(filepath)
        out = screenSentence(table, screensentence)
        # out = screenSentence(content)
        # out = screenSentence(content)
        sumAllcolums(out, table)
    except Exception as ex:
        print(ex)
    '''
    temp_path = [r"\平和质问答.xls", r"\气虚质问答.xls", r"\气郁质问答.xls", \
                 r"\湿热质问答.xls", r"\痰湿质问答.xls", r"\特禀质问答.xls", \
                 r"\血瘀质问答.xls", r"\阳虚质问答.xls", r"\阴虚质问答.xls"]
    '''




