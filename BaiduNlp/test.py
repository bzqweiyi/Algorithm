# coding=gbk
import jieba.analyse
# 字符串前面加u表示使用unicode编码
# content = u'中国特色社会主义是我们党领导的伟大事业，全面推进党的建设新的伟大工程，是这一伟大事业取得胜利的关键所在。党坚强有力，事业才能兴旺发达，国家才能繁荣稳定，人民才能幸福安康。党的十八大以来，我们党坚持党要管党、从严治党，凝心聚力、直击积弊、扶正祛邪，党的建设开创新局面，党风政风呈现新气象。习近平总书记围绕从严管党治党提出一系列新的重要思想，为全面推进党的建设新的伟大工程进一步指明了方向。'
# content = u'中国特色社会主义是我们党领导的伟大事业，全面推进党的建设新的伟大工程，是这一伟大事业取得胜利的关键所在。党坚强有力，事业才能兴旺发达，国家才能繁荣稳定，人民才能幸福安康。党的十八大以来，我们党坚持党要管党、从严治党，凝心聚力、直击积弊、扶正祛邪，党的建设开创新局面，党风政风呈现新气象。习近平总书记围绕从严管党治党提出一系列新的重要思想，为全面推进党的建设新的伟大工程进一步指明了方向。'
content = u'斯坦福教授正在教授课程'
# 第一个参数：待提取关键词的文本
# 第二个参数：返回关键词的数量，重要性从高到低排序
# 第三个参数：是否同时返回每个关键词的权重
# 第四个参数：词性过滤，为空表示不过滤，若提供则仅返回符合词性要求的关键词
keywords = jieba.analyse.extract_tags(content, topK=20, withWeight=True, allowPOS=())
for item in keywords:
    print(item[0], item[1])

# 同样是四个参数，但allowPOS默认为('ns', 'n', 'vn', 'v')
# 即仅提取地名、名词、动名词、动词
import time
tic = time.clock()
keywords = jieba.analyse.textrank(content, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
print(time.clock() - tic)
# 访问提取结果
for item in keywords:
    # 分别为关键词和相应的权重
    print(item[0],  item[1])
'''
# 加载jieba.posseg并取个别名，方便调用
import jieba.posseg as pseg
words = pseg.cut("斯坦福教授正在教授课程")
for word, flag in words:
    # 格式化模版并传入参数
    print('%s, %s' % (word, flag))
'''

'''
import os
# 保存文件的函数
def savefile(savepath, content):
    fp = open(savepath, 'w', encoding='utf-8',errors='ignore')
    fp.write(content)
    fp.close()

# 读取文件的函数
def readfile(path):
    fp = open(path, "r", encoding='utf-8', errors='ignore')
    content = fp.read()
    # fp.write(content)
    fp.close()
    return content

## 去除停用词的2个函数dd
# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readline()]
    return stopwords
# 对句子去除停用词
def movestopwords(sentence):
    stopwords = stopwordslist('语料/hlt_stop_words.txt')
    outstr = ''
    for word in sentence:
        if word not in stopwords:
            if word != '\t' and '\n':
                outstr += word
    return outstr

corpus_path = "语料/train/" # 未分词分类预料库路径
seg_path = "语料/train_seg/"  # 分词后分类语料库路径

catelist = os.listdir(corpus_path)  # 获取未分词目录下所有子目录
for mydir in catelist:
    class_path = corpus_path + mydir + "/"  # 拼出分类子目录的路径
    seg_dir = seg_path + mydir + "/"        # 拼出分词后语料分类目录
    if not os.path.exists(seg_dir):         # 是否存在，不存在则创建
        os.makedirs(seg_dir)

    file_list = os.listdir(class_path)  # 列举当前目录所有文件
    for file_path in file_list:
        fullname = class_path + file_path  # 路径+文件名
        print("当前处理的文件是： ", fullname)  # 语料/train/pos/pos1.txt
            # 语料/train/neg/neg1.txt
        content = readfile(fullname).strip()  # 读取文件内容
        content = content.replace("\n", "").strip()  # 删除换行和多余的空格
        content_seg = jieba.cut(content)
        print("jieba分词后： ", content_seg)
        listcontent = ''
        for i in content_seg:
            listcontent += i
            listcontent += " "
        print(listcontent[0:10])
        listcontent = movestopwords(listcontent)
        print("去除停用词后：", listcontent[0:10])
        listcontent = listcontent.replace("   ", " ").replace("  ", " ")
        savefile(seg_dir + file_path, "".join(listcontent))  #保存
'''












