# -*- coding:utf-8 -*-
# read and cut repeat words
# james

def cutRepeat(read_file, save_file):
    file = open(read_file, 'r', encoding='utf-8')
    source = file.readlines()
    newsource = set(source)
    file.close()
    save = open(save_file, 'w', encoding='utf-8')
    for line in newsource:
        save.write(line)
    print('set finished.', len(newsource))

if __name__ == "__main__":
    read_file = "repeat.txt"
    save_file = "repeat_new.txt"
    cutRepeat(read_file, save_file)