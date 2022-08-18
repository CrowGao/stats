#!/usr/bin/python3
import json
 
# 读取数据
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

for id in range(0,8):
    if x >= xlimit:
        level = level + 1
        x = 0     
    y = level * h

    gridPos = {}
    gridPos["h"] = h
    gridPos["w"] = w
    gridPos["x"] = x
    gridPos["y"] = y
    rawpanel["gridPos"] = gridPos

    rawpanel["id"] = id

    newpanels.append(rawpanel.copy())
    x = x + w

# print(len(newpanels))
dataDashboard["panels"] = newpanels
f = open('newdashboard.json', 'w')
json.dump(dataDashboard, f)
f.close()
    