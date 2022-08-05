# This is a sample Python script.
 
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
from email import message
from pickle import FALSE

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time
import re

 # You can generate an API token from the "API Tokens Tab" in the UI
token = "iaVHealnZgJFz2OhCyNeWCSlwSvuA7XNBvfkxW4-ruPC2XclRG1zhVXcNtiNWaa-p7fLGRLbedym8yeYlVQdJw=="
org = "intel"
bucket = "demo"
measurement = "CPU"
flag = False

SelectEvent = [
    "TOP.SimTop.l_soc.core_with_l2.core.memBlock.stdExeUnits_1.std: in_valid",\
    "TOP.SimTop.l_soc.core_with_l2.core.exuBlocks.fuBlock.exeUnits_0.alu: in_valid",\
    "TOP.SimTop.l_soc.core_with_l2.core.exuBlocks.fuBlock.exeUnits_3.alu: out_valid,"
    ]

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
 
def Delete_Measurement(client):
    start = "1970-01-01T00:00:00Z"
    stop = "2200-01-01T00:00:00Z"
    delete_api = client.delete_api()
    delete_api.delete(start, stop, "_measurement=\"" + measurement +"\"", bucket, org)

def Write_Data(client):
    allstats = {}
    filepath = "data/stats.txt"

    while(os.path.exists(filepath) is False):
        time.sleep(0.5)

    f = open(filepath,"r")
    lines = f.readlines()
    while(lines[len(lines)-1].find("done") == -1):
        lines = f.readlines()
    f.close()
    os.remove(filepath)
    
    EventNum = 0
    for line in lines:
        if EventNum == len(SelectEvent):
            break

        for event in SelectEvent:
            # print("event=",event)
            if EventNum == len(SelectEvent):
                break

            if line.find(event) != -1 :
                EventNum =EventNum + 1

                filter = r'TOP\.(.*?),'
                EventName = re.findall(filter,line)[0]
                EventName = EventName.replace(" ","")
                # print("eventname=",EventName)
                EventResult  = line.split(",")[1]
                # print("eventresult=",EventResult)
                allstats[EventName] = EventResult.strip()
    
    # input = "cpu,host=host1 used_percent=23.43234543"
    input = measurement + ",id=cpu "
    for key in allstats:
        print("key=",key,":",allstats[key])
        input = input  + key +"=" + allstats[key] + ","
    input = input[:-1]
   
    print(input)
    # print("writing data")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, input)

# def Create_Measurement(bucket_parameter,client):
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print_hi('influxdb2.3')

    # Initialize the Client
    with InfluxDBClient(url="http://10.240.192.131:8086", token=token, org=org) as client:
        
        if flag is True :
            Delete_Measurement(client)
            # Create_Measurement(bucket_parameter,client)

        # Write Data
        while(True):
            Write_Data(client)

        # Query Data
        # query = 'from(bucket: "demo") |> range(start: -1m)'
        query = "from(bucket: \""+ bucket +"\" ) |> range(start: -1m)"
        print(query)
        tables = client.query_api().query(query, org=org)
        for table in tables:
            for record in table.records:
                print(record)


 
        # Execute a Flux query
        # query = 'from(bucket: "test") |> range(start: -1h)'
        # tables = client.query_api().query(query, org=org)
        # for table in tables:
        #     for record in table.records:
        #         print(record)
 
    client.close()
