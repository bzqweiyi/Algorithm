# coding:utf-8
from lxml import etree
import requests
import xlwt

title = []


def get_film_name(url):
    html = requests.get(url).text  # 这里一般先打印一下 html 内容，看看是否有内容再继续。
    # print(html)
    s = etree.HTML(html)  # 将源码转化为能被 XPath 匹配的格式
    filename = s.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')  # 返回为一列表
    # print (filename)
    title.extend(filename)


def get_all_film_name():
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i)
        get_film_name(url)


if __name__ == '__main__':
    myxls = xlwt.Workbook()
    sheet1 = myxls.add_sheet(u'top250', cell_overwrite_ok=True)
    get_all_film_name()
    for i in range(0, len(title)):
        sheet1.write(i, 0, i + 1)
        sheet1.write(i, 1, title[i])
    myxls.save('top250.xls')
