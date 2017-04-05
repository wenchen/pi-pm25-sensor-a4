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
    params = urllib.urlencode({'field1': pmdata[0], 'field2': pmdata[1], 'field3': pmdata[2], 'field4': pmdata[3], 'field5': pmdata[4], 'field6': pmdata[5], 'field7': pmdata[6], 'field8': pmdata[7], 'key':'YOUR WRITE KEY'})
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


