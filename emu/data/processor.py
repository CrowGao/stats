import re
import time
readfilepath = "emu.txt"
writefilepath = "stats.txt"

readf = open(readfilepath,"r")
lines = readf.readlines()
print(type(lines))
readf.close()


a = r'PERF(.*?)TOP'
i = 0
for i in range(0,len(lines)):
    writef = open(writefilepath,"w")
    data = ""
    print(type(lines[i]),lines[i])
    cycle  = re.findall(a,lines[i])[0]
    print(type(cycle),cycle)
    j = i
    while(j < len(lines) and lines[j].find(cycle) != -1):
        data = data + lines[j]
        j = j + 1
        # 
    i = j
    print(i)
    writef.write(data)
    writef.write("done")
    writef.close()
    time.sleep(8)
