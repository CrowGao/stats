import re
from readline import write_history_file
import fcntl
import threading
import time

def split_list_by_n(list_collection, n):
    """
    将集合均分 每份n个元素
    :param list_collection:
    :param n:
    :return:返回的结果为评分后的每份可迭代对象
    """
    allstats = []
    for i in range(0, len(list_collection), n):
        allstats.append(list_collection[i: i + n])
        # print(list_collection[i: i + n])
        # yield list_collection[i: i + n]
    return allstats

def process():
    readfilepath = "stats.txt"
    writefilepath = "tempstats.txt"
    f = open(readfilepath,"r")
    lines = f.readlines()
    # oneStatsLength = 1192
    # allstats = split_list_by_n(lines,oneStatsLength)
    f.close()
    data = ""
    for line in lines:
        if line == "---------- Begin Simulation Statistics ----------\n" :
            data = "\n"
            data = data + line
        elif line == "---------- End Simulation Statistics   ----------\n" :
            data = data + line
            with open(writefilepath, "w") as f:
                # fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # 加锁
                f = open(writefilepath,"w")
                f.write(data)  
            time.sleep(1)
        else:
            data = data + line

def main():
    process()
    print("print over")

if __name__=="__main__":
    main()
