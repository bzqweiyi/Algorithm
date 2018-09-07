# -*- coding: utf-8 -*-
import jieba
import jieba.analyse

from functools import reduce
import xlrd

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

if __name__ == "__main__":
  path = r"C:\Users\USER\Documents\WeChat Files\mad_Lax\Files\过滤后的语料\过滤后的语料\糖尿病问答（已标签）8.29.xlsx"
  tags = wrapper(path, 0, 1, 1, 30)
  print(tags)
