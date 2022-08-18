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

 # You can generate an API token from the "API Tokens Tab" in the UI
token = "iaVHealnZgJFz2OhCyNeWCSlwSvuA7XNBvfkxW4-ruPC2XclRG1zhVXcNtiNWaa-p7fLGRLbedym8yeYlVQdJw=="
ip = "http://10.240.192.131:8086"
org = "intel"
bucket = "demo"
measurement = "CPU"
flag = True


SelectIntervalEvent = [
    "TOP.SimTop.l_soc.core_with_l2.core.frontend.ftq: entry",                       
    "TOP.SimTop.l_soc.core_with_l2.core.frontend.ibuffer: utilization",
    "TOP.SimTop.l_soc.core_with_l2.core.ctrlBlock.rob: utilization",
    "TOP.SimTop.l_soc.core_with_l2.core.memBlock.lsq.loadQueue: utilization",
    "TOP.SimTop.l_soc.core_with_l2.core.memBlock.lsq.storeQueue: utilization"
    ]

SelectLastEvent = [
    "TOP.SimTop.l_soc.core_with_l2.core.memBlock.dcache.dcache.ldu_0: load_req",
    "TOP.SimTop.l_soc.core_with_l2.core.memBlock.dcache.dcache.ldu_0: load_miss",
    "TOP.SimTop.l_soc.core_with_l2.core.memBlock.dcache.dcache.ldu_1: load_req",
    "TOP.SimTop.l_soc.core_with_l2.core.memBlock.dcache.dcache.ldu_1: load_miss"
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

def SelectInfo(line,Events):
    Result = []
    for event in Events:
        # 为了防止以下统计信息
        # total guest instructions = 382113
        # instrCnt = 382113, cycleCnt = 209260, IPC = 1.826020
        # n_issue_entries_13_14,                    0
        if line.find(event) != -1 :
            #去掉字符串中的空格、制表符和回车，然后“，”分隔成list
            line = re.sub("\s|\t|\n","",line)
            Result = line.split(",")

            e = re.sub("\s|\t|\n","",event)
            if e is Result[1]:
                return Result
    return Result

#读取统计信息
def Read_Data():
    #读取txt文本信息
    FilePath = "data/emu.txt"
    f = open(FilePath,"r")
    lines = f.readlines()
    f.close()

    #选择出想要统计的信息
    AllIntervalResult = []
    AllLastResult = []
    for line in lines:
        Result = SelectInfo(line,SelectIntervalEvent)
        if len(Result) > 0:
            AllIntervalResult.append(Result)
            continue
        Result = SelectInfo(line,SelectLastEvent)
        if len(Result) > 0:
            AllLastResult.append(Result)
            continue 

    return AllIntervalResult,AllLastResult
    
def Write_Data(client):

    AllIntervalResult, AllLastResult = Read_Data()
    
    if(len(AllIntervalResult)==0 or len(AllLastResult)==0):
        print("NOT FIND STATS EVENT")
        exit(0)
    
    Index1 = 0
    Index2 = 0
    IntervalStats = {}
    for i in range(0,len(AllIntervalResult)):
        IntervalStats[AllIntervalResult[i][1]] = 0
    AllIntervalResultLength = len(AllIntervalResult)
    AllLastResultlength = len(AllLastResult)
    
    while Index1 < AllIntervalResultLength and Index2  < AllLastResultlength:
        input = measurement + ",id=cpu "
        Cycle = AllIntervalResult[Index1][0]
        input = input + "Cycle=" + Cycle + ","
        while Index1 < AllIntervalResultLength and Cycle == AllIntervalResult[Index1][0]:
            IntervalStats[AllIntervalResult[Index1][1]] = int(AllIntervalResult[Index1][2])/10000
            input = input + AllIntervalResult[Index1][1] + "=" + str(IntervalStats[AllIntervalResult[Index1][1]]) + ","
            Index1 = Index1 + 1
        while Index2 < AllLastResultlength and Cycle == AllLastResult[Index2][0]:
            input = input + AllLastResult[Index2][1] + "=" + AllLastResult[Index2][2] + ","
            Index2 = Index2 + 1
        input = input[:-1]
        # print(input)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, input)
        time.sleep(5)

    
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
        

        if flag is False :
            Delete_Measurement(client)
            # Create_Measurement(bucket_parameter,client)

        # StatsFilePath = "data/emu.txt"
        # f = open(StatsFilePath,"r")
        # lines = f.readlines()
        # f.close()
        # Read_Data()
        Write_Data(client)
        # Write Data
        # while(True):
        #     Write_Data(client)

        # Query Data
        # query = 'from(bucket: "demo") |> range(start: -1m)'
        
        

 
        # Execute a Flux query
        # query = 'from(bucket: "test") |> range(start: -1h)'
        # tables = client.query_api().query(query, org=org)
        # for table in tables:
        #     for record in table.records:
        #         print(record)
 
    client.close()
