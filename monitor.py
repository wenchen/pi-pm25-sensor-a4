#!/usr/bin/python

import time
import datetime
import os
import httplib, urllib
import a4

air=a4.a4sensor()
while True:
    try:
        pmdata=air.read("/dev/ttyAMA0")
    except:
        pmdata=[0,0,0,0,0,0,0,0,0]
        continue

    # thingspeak
    # 答：A4-CG输出标准体积（0.1L）的颗粒物浓度和粒子个数；
    # 输出PM1、PM2.5、PM10颗粒物浓度，其中只有PM2.5是精确的，PM1和PM10为结合TSI经验参考值，PM10≥PM2.5≥PM1.0；
    # 输出单位体积0.1L内的PM0.3、PM0.5、PM1、PM2.5、PM5、PM10粒子个数，其中PM1、PM2.5、PM5、PM10为真实参考值，PM0.3、PM0.5是经验参考值，PM0.3＞PM0.5＞PM1＞PM2.5＞PM5＞PM10。

    # Output pm1, pm2.5, pm10, 1.0μm/0.1L, 2.5μm/0.1L, 5.0μm/0.1L, 10.0μm/0.1L
    params = urllib.urlencode({'field1': pmdata[0], 'field2': pmdata[1], 'field3': pmdata[2], 'field4': pmdata[5], 'field5': pmdata[6], 'field6': pmdata[7], 'field7': pmdata[8], 'key':'Thinkspeak API KEY'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    try:
        tconn = httplib.HTTPConnection("api.thingspeak.com:80")
        tconn.request("POST", "/update", params, headers)
        response = tconn.getresponse()
        data = response.read()
        tconn.close()
    except:
        continue
    time.sleep(600)


