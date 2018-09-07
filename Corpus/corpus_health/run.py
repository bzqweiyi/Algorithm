#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/5/30'

启动爬虫

"""

import sys
import codecs
from multiprocessing import Process
from scrapy import cmdline

import logging
from scrapy.utils.log import configure_logging
import time

# 手动配置日志，一天保存一个日志文件
date_format = time.strftime('%Y-%m-%d', time.localtime())
configure_logging(install_root_handler=False)

# logging.basicConfig(
#     filename='logging/'+date_format+'.log',
#     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#     filemode='w',
#     datefmt='%Y-%m-%d %H:%M:%S',
#     level=logging.INFO
# )


class Ask120Run:
    def __init__(self):
        cmdline.execute("scrapy crawl ask120".split())

class Ypk39net:
    def __init__(self):
        cmdline.execute("scrapy crawl ypk39net".split())

class Ask39Net:
    def __init__(self):
        cmdline.execute("scrapy crawl ask39net".split())

def run():
    p_list = list()
    # p1 = Process(target=Ask120Run, name='Ask120Run')
    # p_list.append(p1)
    # p2 = Process(target=Ypk39net, name='Ypk39net')
    # p_list.append(p2)
    p3 = Process(target=Ask39Net, name='Ask39Net')
    p_list.append(p3)

    for p in p_list:
        p.daemon = True
        p.start()
    for p in p_list:
        p.join()

if __name__ == '__main__':
   run()

