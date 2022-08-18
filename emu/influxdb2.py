from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "iaVHealnZgJFz2OhCyNeWCSlwSvuA7XNBvfkxW4-ruPC2XclRG1zhVXcNtiNWaa-p7fLGRLbedym8yeYlVQdJw=="
org = "intel"
bucket = "demo"

with InfluxDBClient(url="http://10.240.192.131:8086", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    # 写入方法1 
    # data = "mem,host=host1 used_percent=23.43234543"
    # write_api.write(bucket, org, data)

    # 写入方法2 （推荐这种）
    point = Point("mem") \
    .tag("host", "host1") \
    .field("used_percent", 24.43234543) \
    .time(datetime.utcnow(), WritePrecision.NS)
    write_api.write(bucket, org, point)

    # 写入方法3
    # sequence = ["mem,host=host1 used_percent=25.43234543",
    #         "mem,host=host1 available_percent=15.856523"]
    # write_api.write(bucket, org, sequence)

    # TODO 这里写查询

	# 用完关闭
	client.close()
