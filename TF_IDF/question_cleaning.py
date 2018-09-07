# -*- coding: utf-8 -*-
import question_tfidf as qt
import xlwt
import jieba

def get_tags(path, sheets_idx, start_line, col_idx, topK):
  return qt.wrapper(path, sheets_idx, start_line, col_idx, topK)

def read_file(path, sheets_idx):
  return qt.read_file(path, sheets_idx)

def tags_filter(table, tags, start_line_idx, col_idx):
  needed = []
  for i in range(start_line_idx, table.nrows):
    row = table.row_values(i)
    # print("row: {}".format(row))

    row_col_idx = row[col_idx]
    # print("row_col_idx: {}".format(row_col_idx))
    if row_col_idx[0:2] == "请问":
      row_col_idx = row_col_idx[2:]
      # print(row_col_idx)
    for tag in tags:
      if tag in row_col_idx:
        needed.append(row)
        # print("needed: {}".format(needed))
        # print(row)
        break
  return needed


def write_xls(needed, saving_path):
  f = xlwt.Workbook()
  sheet1 = f.add_sheet("sheet1", cell_overwrite_ok=True)
  # row0 = ["问题", "描述"]
  # for i in range(0, len(row0)):
  #   sheet1.write(0, i, row0[i])
  for i in range(0, len(needed)):
    for j in range(len(needed[0])):
      # print(len(needed[0]))
      # exit()
      sheet1.write(i, j, needed[i][j])
  f.save(saving_path)
  print(saving_path)


if __name__ == "__main__":
  path = r"E:\GMWork\AIRobot\8种体质\体质数据\体质数据\平和质问答.xls"
  tags = qt.wrapper(path, 0, 0, 0, 15)
  tags = set(tags)
  tags_set = set(["你好", "...", "最近", "哪个", "现在", "您好", "医生", "请问","可以","什么"])
  tags = tags - tags_set
  print(tags)
  # exit()
  table = read_file(path, 0)
  needed = tags_filter(table, tags, 0, 0)
  # print("needed: {}".format(needed[0]))
  print(len(needed))
  # exit()
  # print(needed[0:4])
  saving_path = r"E:\GMWork\AIRobot\8种体质\体质数据\体质数据\平和质问答_new.xls"
  write_xls(needed, saving_path)


