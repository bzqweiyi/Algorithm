#-*- encoding=utf -8-*-
import json
from flask import Flask
from flask import request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from handle import Handle
app = Flask(__name__)
wxtoken = 'weixin'
@app.route('/')
def hello_world():
    return 'Hello This is ChatBot!'


@app.route('/user', methods=['GET', 'POST'])
def user():
    #判断请求方式为POST否则为GET
    if request.method == 'POST':
        res_input = request.form.get('res_input', 'default value')  #参数不存在时默认default value
        print('name:%s' % (res_input))
    else:
        res_input = request.args.get('res_input', r'哈哈')  #参数不存在时默认default value
        deviceId = request.args.get('deviceId', '77777')  # 参数不存在时默认default value
        result = chatbot.get_response(res_input)
        print('res_input:%s' % (res_input))
        print('result:%s' % (result))
    resp_obj = {'deviceId':deviceId, 'res_input': res_input, 'result': str(result)}
    resp = json.dumps(resp_obj,ensure_ascii=False)  ##解决编码问题
    return resp
    #return jsonify({'Success': "1",'deviceId':deviceId,'res_input': res_input,'result': str(result)})


if __name__ == '__main__':
    chatbot = ChatBot("myBot")
    chatbot.set_trainer(ChatterBotCorpusTrainer)
    chatbot.train("chatterbot.corpus.chinese")
    app.run(host='0.0.0.0', port=80)
