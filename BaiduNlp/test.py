# coding=gbk
import jieba.analyse
# �ַ���ǰ���u��ʾʹ��unicode����
# content = u'�й���ɫ������������ǵ��쵼��ΰ����ҵ��ȫ���ƽ����Ľ����µ�ΰ�󹤳̣�����һΰ����ҵȡ��ʤ���Ĺؼ����ڡ�����ǿ��������ҵ��������������Ҳ��ܷ����ȶ�����������Ҹ�����������ʮ�˴����������ǵ���ֵ�Ҫ�ܵ��������ε������ľ�����ֱ�����ס�������а�����Ľ��迪���¾��棬�����������������ϰ��ƽ�����Χ�ƴ��Ϲܵ��ε����һϵ���µ���Ҫ˼�룬Ϊȫ���ƽ����Ľ����µ�ΰ�󹤳̽�һ��ָ���˷���'
# content = u'�й���ɫ������������ǵ��쵼��ΰ����ҵ��ȫ���ƽ����Ľ����µ�ΰ�󹤳̣�����һΰ����ҵȡ��ʤ���Ĺؼ����ڡ�����ǿ��������ҵ��������������Ҳ��ܷ����ȶ�����������Ҹ�����������ʮ�˴����������ǵ���ֵ�Ҫ�ܵ��������ε������ľ�����ֱ�����ס�������а�����Ľ��迪���¾��棬�����������������ϰ��ƽ�����Χ�ƴ��Ϲܵ��ε����һϵ���µ���Ҫ˼�룬Ϊȫ���ƽ����Ľ����µ�ΰ�󹤳̽�һ��ָ���˷���'
content = u'˹̹���������ڽ��ڿγ�'
# ��һ������������ȡ�ؼ��ʵ��ı�
# �ڶ������������عؼ��ʵ���������Ҫ�ԴӸߵ�������
# �������������Ƿ�ͬʱ����ÿ���ؼ��ʵ�Ȩ��
# ���ĸ����������Թ��ˣ�Ϊ�ձ�ʾ�����ˣ����ṩ������ط��ϴ���Ҫ��Ĺؼ���
keywords = jieba.analyse.extract_tags(content, topK=20, withWeight=True, allowPOS=())
for item in keywords:
    print(item[0], item[1])

# ͬ�����ĸ���������allowPOSĬ��Ϊ('ns', 'n', 'vn', 'v')
# ������ȡ���������ʡ������ʡ�����
import time
tic = time.clock()
keywords = jieba.analyse.textrank(content, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
print(time.clock() - tic)
# ������ȡ���
for item in keywords:
    # �ֱ�Ϊ�ؼ��ʺ���Ӧ��Ȩ��
    print(item[0],  item[1])
'''
# ����jieba.posseg��ȡ���������������
import jieba.posseg as pseg
words = pseg.cut("˹̹���������ڽ��ڿγ�")
for word, flag in words:
    # ��ʽ��ģ�沢�������
    print('%s, %s' % (word, flag))
'''

'''
import os
# �����ļ��ĺ���
def savefile(savepath, content):
    fp = open(savepath, 'w', encoding='utf-8',errors='ignore')
    fp.write(content)
    fp.close()

# ��ȡ�ļ��ĺ���
def readfile(path):
    fp = open(path, "r", encoding='utf-8', errors='ignore')
    content = fp.read()
    # fp.write(content)
    fp.close()
    return content

## ȥ��ͣ�ôʵ�2������dd
# ����ͣ�ô�list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readline()]
    return stopwords
# �Ծ���ȥ��ͣ�ô�
def movestopwords(sentence):
    stopwords = stopwordslist('����/hlt_stop_words.txt')
    outstr = ''
    for word in sentence:
        if word not in stopwords:
            if word != '\t' and '\n':
                outstr += word
    return outstr

corpus_path = "����/train/" # δ�ִʷ���Ԥ�Ͽ�·��
seg_path = "����/train_seg/"  # �ִʺ�������Ͽ�·��

catelist = os.listdir(corpus_path)  # ��ȡδ�ִ�Ŀ¼��������Ŀ¼
for mydir in catelist:
    class_path = corpus_path + mydir + "/"  # ƴ��������Ŀ¼��·��
    seg_dir = seg_path + mydir + "/"        # ƴ���ִʺ����Ϸ���Ŀ¼
    if not os.path.exists(seg_dir):         # �Ƿ���ڣ��������򴴽�
        os.makedirs(seg_dir)

    file_list = os.listdir(class_path)  # �оٵ�ǰĿ¼�����ļ�
    for file_path in file_list:
        fullname = class_path + file_path  # ·��+�ļ���
        print("��ǰ������ļ��ǣ� ", fullname)  # ����/train/pos/pos1.txt
            # ����/train/neg/neg1.txt
        content = readfile(fullname).strip()  # ��ȡ�ļ�����
        content = content.replace("\n", "").strip()  # ɾ�����кͶ���Ŀո�
        content_seg = jieba.cut(content)
        print("jieba�ִʺ� ", content_seg)
        listcontent = ''
        for i in content_seg:
            listcontent += i
            listcontent += " "
        print(listcontent[0:10])
        listcontent = movestopwords(listcontent)
        print("ȥ��ͣ�ôʺ�", listcontent[0:10])
        listcontent = listcontent.replace("   ", " ").replace("  ", " ")
        savefile(seg_dir + file_path, "".join(listcontent))  #����
'''












