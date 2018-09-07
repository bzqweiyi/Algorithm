# -*- coding: utf-8 -*-
# James
# 20180906
# This is baidu's nlp API

import urllib.request
import urllib
import requests
import json
import sys
from aip import AipNlp
# This aip sdk help file.
# http://ai.baidu.com/docs#/NLP-Python-SDK/d2e424bf


APP_ID = '11642155'
API_KEY = 'gt4ogN9A7ROF3GWBXYmDTrUu'
SECRET_KEY = '87uvAFMYAPC8KfBzI6GRgpLfQzZB2zA7'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
text = '百度是一家高科技公司'
client.lexer(text)

word1 = "老婆"; word2 = "老公"
client.wordSimEmbedding(word1, word2)  # 得到两个词的相似度

sen1 = "nana是我老婆"; sen2 = "我老公是nana"
client.simnet(sen1, sen2)

# confirm the access authority:
def get_access_token():
    # client_id 为官网获取的AK，
    # client_secret 为官网获取的SK
    ak = 'gt4ogN9A7ROF3GWBXYmDTrUu'
    sk = '87uvAFMYAPC8KfBzI6GRgpLfQzZB2zA7'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ ak +'&client_secret='+ sk+'&'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    content = json.loads(content)
    if (content):
        return content["access_token"]

# get json content
def get_content(text):
    access_token = get_access_token()
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag?access_token=" + access_token
    headers = {"Content-Type": "application/json"}
    data = {"text": text, "type": 2}
    try:
        data = json.dumps(data)
        r = requests.post(url, data=data, headers=headers)
        return r.text
    except Exception as e:
        print(str(e))
        return 0


if __name__ == "__main__":
    text = '服务态度好，但是房间比较小'
    contents = get_content(text)
    print(contents)
    contents = json.loads(contents)
    if contents['items']:
        for i in range(len(contents['items'])):
            print('评论观点:' + contents['items'][i]['prop'])
    else:
        pass