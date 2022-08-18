import re
from readline import write_history_file
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
    print(type(lines))
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
            f = open(writefilepath,"w")
            f.write(data)
            f.close()
            time.sleep(10)
        else:
            data = data + line


