# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import xlrd
import xlwt
import random

def read_file(path, sheets_idx):
  data = xlrd.open_workbook(path)
  table = data.sheets()[sheets_idx]
  return table

def gen(table, start_line, col_idx):
  for i in range(1, table.nrows):
    # yield reduce(lambda x,y  : x+y, table.row_values(i))
    yield table.row_values(i)[col_idx]

def build_content(table, start_line, col_idx):
  content = ""
  temp = gen(table, start_line, col_idx)
  for i in temp:
    content += i
  return content

def find_tags(content, topK):
  return jieba.analyse.extract_tags(content, topK=topK)

def wrapper(path, sheets_idx, start_line, col_idx, topK):
  table = read_file(path, sheets_idx)
  content = build_content(table, start_line, col_idx)
  tags = find_tags(content, topK)
  return tags

myExcel = xlwt.Workbook()
def savefile(filepath, tags, name):
  sheet1 = myExcel.add_sheet(name, cell_overwrite_ok=True)
  for i in range(0, len(tags)):
    sheet1.write(i, 0, tags[i])
  myExcel.save(filepath)

def genratorHealthReport(finalpath, new_path, health_data):
  tags = wrapper(finalpath, 0, 1, 0, topK=100)
  tags = set(tags)
  tags_set = set(["你好", "...", "..", "最近", "哪个", "现在", \
                  "您好", "怎么", "怎么办", "医生", "请问","可以",\
                  "什么", "如何", "怎么回事"])
  tags = tags - tags_set
  new_tags = list(tags)
  random.shuffle(new_tags)
  savefile(new_path, new_tags, health_data)


if __name__ == "__main__":
  # This is for tizhi
  tizhi = ["平和质", "气虚质", "气郁质", "湿热质", "痰湿质", "特禀质", "血瘀质", "阳虚质", "阴虚质"]
  tz_path = r"E:\GMWork\AIRobot\8种体质\体质数据\体质数据"
  tizhi_path = [r"\平和质问答.xls", r"\气虚质问答.xls", r"\气郁质问答.xls", \
               r"\湿热质问答.xls", r"\痰湿质问答.xls", r"\特禀质问答.xls", \
               r"\血瘀质问答.xls", r"\阳虚质问答.xls", r"\阴虚质问答.xls"]
  new_tizhi_path = r"E:\GMWork\AIRobot\8种体质\体质数据\体质数据\KeyWords\体质数据.xls"
  # This is for manbing
  mb_path = r"E:\GMWork\AIRobot\12种慢病"
  manbing = ["痴呆", "感冒", "高血压", "高血脂", "冠心病", "颈椎病", "咳嗽", "糖尿病", "痛风", "腰腿疼", "脂肪肝", "中风"]
  manbing_path = [r"\痴呆.xls", r"\感冒.xlsx", r"\高血压.xlsx", r"\高血脂.xls", \
                  r"\冠心病.xls", r"\颈椎病.xls", r"\咳嗽.xlsx", r"\糖尿病.xlsx", \
                  r"\痛风.xls", r"\腰腿疼.xls", r"\脂肪肝.xls", r"\中风.xls"]
  new_manbing_path = r"E:\GMWork\AIRobot\12种慢病\KeyWords\慢病数据.xls"
  for i in range(0, len(manbing)):
    finalpath = mb_path + manbing_path[i]
    try:
      genratorHealthReport(finalpath, new_manbing_path, manbing[i])
    except Exception as ex:
      print(ex)

