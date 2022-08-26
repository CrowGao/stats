#-*- coding:utf-8 -*-
#!/usr/bin/python3
import json

def findEvent(allEvents,event):
    for e in allEvents:
        if e == event:
            return False
    return True

def generatePanel():
    # 读取监控事件
    allEvents = []
    eventFilePath = "event.txt"
    with open(eventFilePath,"r") as f:
        events = f.readlines()
        for event in events:
            event = event.replace("\n","")
            if findEvent(allEvents,event) == True:
                allEvents.append(event)

    # 读取模板panel数据
    f=open("paneltemplate.json", "r")
    dataDashboard = json.load(f)
    f.close()

    rawpanel = dataDashboard["panels"][0]
    h = 8
    w = 6
    x = 0
    y = 0
    xlimit = w * 4
    level = 0
    newpanels = []

    for id in range(0,len(allEvents)):
        if x >= xlimit:
            level = level + 1
            x = 0     
        y = level * h

        # panel 位置和大小
        gridPos = {}
        gridPos["h"] = h
        gridPos["w"] = w
        gridPos["x"] = x
        gridPos["y"] = y
        rawpanel["gridPos"] = gridPos

        # panel id
        rawpanel["id"] = id

        # grafana查询语句
        target = []
        method = {}
        method["datasource"] = {
            "type": "influxdb",
            "uid": "_5uOsGz4z"
        }
        bucket = "demo"
        measurement = "gem5template"
        method["query"] = "from(bucket: \"" + bucket + "\")\r\n\
                |> range(start: -2d)\r\n\
                |> filter(fn: (r) => r[\"_measurement\"] == \"" + measurement + "\")\r\n\
                |> filter(fn: (r) => r[\"_field\"] == \"" + allEvents[id] + "\")"
        method["refId"] = "A"
        target.append(method)
        rawpanel["targets"] = target

        # panel title
        title = allEvents[id]
        rawpanel["title"] = title
        
        newpanels.append(rawpanel.copy())
        x = x + w

    # print(len(newpanels))
    dataDashboard["panels"] = newpanels
    f = open('newdashboard.json', 'w')
    json.dump(dataDashboard, f)
    f.close()

if __name__ == '__main__':
    generatePanel()
    