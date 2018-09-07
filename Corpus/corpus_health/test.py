#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/5'

__QQ__ = '376205871'

"""

import re
def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<![CDATA[[^>]*//]]>', re.I)  # 匹配CDATA
    re_script = re.compile('<s*script[^>]*>[^<]*<s*/s*scripts*>', re.I)  # Script
    re_style = re.compile('<s*style[^>]*>[^<]*<s*/s*styles*>', re.I)  # style
    re_br = re.compile('<brs*?/?>')  # 处理换行
    re_h = re.compile('</?w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('n+')
    s = blank_line.sub('n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s


"""
##替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
"""


def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr



if __name__ == '__main__':
    s = '<dd>\r\n                              主要用于缺血性<a href="/search/%E8%84%91%E8%A1%80%E7%AE%A1%E7%97%85/">脑血管病</a>如<a href="/search/%E8%84%91%E8%A1%80%E6%A0%93/">脑血栓</a>、<a href="/search/%E8%84%91%E6%A0%93%E5%A1%9E/">脑栓塞</a>、<a href="/search/%E7%9F%AD%E6%9A%82%E6%80%A7%E8%84%91%E7%BC%BA%E8%A1%80%E5%8F%91%E4%BD%9C/">短暂性脑缺血发作</a>及心血管<a href="/search/%E7%96%BE%E7%97%85/">疾病</a>如<a href="/search/%E9%AB%98%E8%A1%80%E5%8E%8B/">高血压</a>、<a href="/search/%E9%AB%98%E8%84%82%E8%9B%8B%E7%99%BD%E8%A1%80%E7%97%87/">高脂蛋白血症</a>、<a href="/search/%E5%86%A0%E5%BF%83%E7%97%85/">冠心病</a>、<a href="/search/%E5%BF%83%E7%BB%9E%E7%97%9B/">心绞痛</a>等<a href="/search/%E7%96%BE%E7%97%85/">疾病</a>的防治。也可用于治疗<a href="/search/%E5%BC%A5%E6%BC%AB%E6%80%A7%E8%A1%80%E7%AE%A1%E5%86%85%E5%87%9D%E8%A1%80/">弥漫性血管内凝血</a>、<a href="/search/%E6%85%A2%E6%80%A7%E8%82%BE%E5%B0%8F%E7%90%83%E8%82%BE%E7%82%8E/">慢性肾小球肾炎</a>及<a href="/search/%E5%87%BA%E8%A1%80%E7%83%AD/">出血热</a>等。\r\n                        </dd>'
    print(str)
    print('========')
    p = re.compile('<[^>]+>').sub("", s)
    print("".join(p.split()))
    print('=========')
