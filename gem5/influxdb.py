# This is a sample Python script.

from datetime import datetime
from email import message
from itertools import cycle
from pickle import FALSE, TRUE
from unittest import result

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time
import re
import fcntl
import threading
 # You can generate an API token from the "API Tokens Tab" in the UI
token = "iaVHealnZgJFz2OhCyNeWCSlwSvuA7XNBvfkxW4-ruPC2XclRG1zhVXcNtiNWaa-p7fLGRLbedym8yeYlVQdJw=="
ip = "http://10.240.192.131:8086"
org = "intel"
bucket = "demo"
measurement = "gem5template"
flag = True

SelectEvent = [
    "system.cpu.ipc",
    "system.cpu.commit.branchMispredicts",
    "system.cpu.fetch.insts",
    "system.cpu.commit.instsCommitted",
    "system.cpu.lsq0.loadToUse::mean",
    "system.cpu.dcache.ReadReq.hits::total",
    "system.cpu.dcache.ReadReq.misses::total",
    "system.cpu.icache.demandHits::total",
    "system.cpu.icache.demandMisses::total",
    "system.l2.demandAccesses::total",
    "system.l2.demandMissRate::total" 
] 
def print_hi(name):
    print(f'Hi, {name}') 

#删除一个指定的measurement
def Delete_Measurement(client):
    start = "1970-01-01T00:00:00Z"
    stop = "2200-01-01T00:00:00Z"
    delete_api = client.delete_api()
    delete_api.delete(start, stop, "_measurement=\"" + measurement +"\"", bucket, org)

def SplitStr(line):
    Result = []
    line = re.sub("\s|\t|\n","",line)
    Result = line.split(",")
    return Result

def SelectInfo(line):
    Result = []
    pos = line.find("#")
    line = line[0:pos]

    pos = line.find(" ")
    name = line[0:pos]        
    
    pos = line.find(" ")
    num = line[pos:]
    i = 0
    numlist = list(num)
    while i < len(numlist):
        if(numlist[i]!=' '):
            numlist[i-1]=','
            while numlist[i] != ' ':
                i = i + 1
            continue
        i = i + 1
    num = "".join(numlist)
    num = num.replace(" ","").replace("\n","").replace("\t","")
    
    line = name + num
    # print(line) 
    # print(line)
    #去掉字符串中的制表符和回车，然后空格分隔成list
    # line = re.sub("\t|\n|\r","",line)
    Result = line.split(",")
    if Result[1] == "nan":
        Result[1] = "0"
    # print(Result)

    return Result

#读取统计信息
def Read_Data():
    #读取txt文本信息,同时截取掉开头和结尾的打印信息
    FilePath = "data/tempstats.txt"
    lines = []
    while os.path.exists(FilePath) == False :
        print("",end="")
    time.sleep(0.5)
    with open(FilePath, "r") as f:
        lines = f.readlines()
        lines = lines[2:len(lines)-2]
    os.remove(FilePath)

    #选择出想要统计的信息
    AllResult = []
    for line in lines:
        Result = SelectInfo(line)
        AllResult.append(Result)
    return AllResult
    
def Write_Data(client):

    AllResult = Read_Data()
    
    if(len(AllResult)==0):
        print("NOT FIND STATS EVENT")
        exit(0)
    
    Index0 = 0
    # IntervalStats = {}
    # for i in range(0,len(AllIntervalResult)):
    #     IntervalStats[AllIntervalResult[i][1]] = 0
    # AllIntervalResultLength = len(AllIntervalResult)
    # AllLastResultlength = len(AllLastResult)
    # input = measurement
    for result in AllResult:
        input = measurement
        # print(result)
        # 按照"." 或者 "::"分割事件
        name = result[0]
        PartName = name.split(".")
        PartNameNums = len(PartName)

        for i in range(0,PartNameNums):
            input = input + ",Part" + str(i) + "=" + PartName[i]
        for i in range(PartNameNums,5):
            input = input + ",Part" + str(i) + "=0" 
        input = input + " "
        # 一个事件有多个统计信息，比如
        # system.cpu.statIssuedInstType_0::SimdAlu            0      0.00%
        # print(result)
        if len(result)>2 :
            continue
            for i in range(1,len(result)) :
                tempname = name + str(i)
                input = input + tempname + "=" + result[i] + ","
        else:
            input = input + name + "=" + result[1] + ","
        input = input[:-1]
        print(input)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, input)


    
    #传入influxdb2.3的语句：input = "cpu,id=cpu host=host1,list1=1,list2=2,list3=3"
    # input = measurement + ",id=cpu "
    # for key in allstats:
    #     print("key=",key,":",allstats[key])
    #     input = input  + key +"=" + allstats[key] + ","
    # input = input[:-1]
   
    # print(input)
    # # print("writing data")
    # write_api = client.write_api(write_options=SYNCHRONOUS)
    # write_api.write(bucket, org, input)

def Query_Data(clinet):
    query = "from(bucket: \""+ bucket +"\" ) |> range(start: -7d)"
    print(query)
    tables = client.query_api().query(query, org=org)
    for table in tables:
        for record in table.records:
            print(record)
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print_hi('influxdb2.3')

    # 初始化influxdb2.3 Client
    with InfluxDBClient(url=ip, token=token, org=org) as client:
        

        if flag is True :
            Delete_Measurement(client)
            print("Delete Measurement")
           
        # StatsFilePath = "data/emu.txt"
        # f = open(StatsFilePath,"r")
        # lines = f.readlines()
        # f.close()
        # Read_Data()
        while True:
            Write_Data(client)
        # Write Data
        # while(True):
        #     Write_Data(client)

        # Query Data
        # query = 'from(bucket: "demo") |> range(start: -1m)'
        
        

 
        # Execute a Flux query
        # query = "from(bucket: \"" + bucket + "\") |> range(start: -1h)"
        # tables = client.query_api().query(query, org=org)
        # for table in tables:
        #     for record in table.records:
        #         print(record)
 
    client.close()
    print("end")
