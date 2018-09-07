# -*- coding:utf-8 -*-
import shutil
readDir = "repeat"
writeDir = "repeat"
#txtDir = "/home/fuxueping/Desktop/１"
lines_seen = set()
outfile=open(writeDir,"w")
f = open(readDir, "r")
for line in f:
    if line not in lines_seen:
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
print("success")
def distinct_file(f_path, s_path):
    with open(f_path, "r", encoding="utf-8") as f:
        with open(s_path, "w", encoding="utf-8") as s:
            distinct_set = set()
            fcount = 0
            scount = 0
            for line in f.readlines():
                fcount +=1
                try:
                    print(line)
                    distinct_set.add(line)
                    scount +=1
                except UnicodeDecodeError:
                    continue
            for element in distinct_set:
                s.write(element)
    print("fcount".format(fcount))
    print("scount".format(scount))
    print("distinct_set".format(len(distinct_set)))


if __name__ == "__main__":
    f_path = r"C:\Users\User\Desktop\中医相关\中医穴位2\temp.txt"
    s_path = r"C:\Users\User\Desktop\中医相关 - 副本\中医穴位\中医穴位_1.0.txt"
    distinct_file(f_path, s_path)
