#!/bin/python
import serial
import time
import sys
from struct import *
debug=0
# work for A4
# data structure: http://www.senseiot.com/upload/20151191675162971.pdf

class a4sensor():
    def __init__(self):
        if debug: print "init"
        self.endian = sys.byteorder

    def conn_serial_port(self, device):
        if debug: print device
        self.serial = serial.Serial(device, baudrate=9600)
        if debug: print "conn ok"

    def check_keyword(self):
        if debug: print "check_keyword"
        while True:
            token = self.serial.read()
            token_hex=token.encode('hex')
            if debug: print token_hex
            if token_hex == '32':
                if debug: print "get 32"
                token2 = self.serial.read()
                token2_hex=token2.encode('hex')
                if debug: print token2_hex
                if token2_hex == '3d':
                    if debug: print "get 3d"
                    return True

    def vertify_data(self, data):
        if debug: print data
        n = 2
        sum = int('32',16)+int('3d',16)
        for i in range(0, len(data)-4, n):
            sum=sum+int(data[i:i+n],16)
        versum = int(data[56]+data[57]+data[58]+data[59],16)
        if debug: print sum
        if debug: print versum
        if sum == versum:
            print "data correct"

    def read_data(self):
        data = self.serial.read(30)
        data_hex=data.encode('hex')
        if debug: self.vertify_data(data_hex)
        pm1_cf=int(data_hex[4]+data_hex[5]+data_hex[6]+data_hex[7],16)
        pm25_cf=int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16)
        pm10_cf=int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16)
        um3=int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16)
        um5=int(data_hex[20]+data_hex[21]+data_hex[22]+data_hex[23],16)
        um10=int(data_hex[24]+data_hex[25]+data_hex[26]+data_hex[27],16)
        um25=int(data_hex[28]+data_hex[29]+data_hex[30]+data_hex[31],16)
        um50=int(data_hex[32]+data_hex[33]+data_hex[34]+data_hex[35],16)
        um100=int(data_hex[36]+data_hex[37]+data_hex[38]+data_hex[39],16)
        if debug: print "pm1: "+str(pm1_cf)
        if debug: print "pm25: "+str(pm25_cf)
        if debug: print "pm10: "+str(pm10_cf)
        if debug: print "um03: "+str(um3)
        if debug: print "um05: "+str(um5)
        if debug: print "um10: "+str(um10)
        if debug: print "um25: "+str(um25)
        if debug: print "um50: "+str(um50)
        if debug: print "um100: "+str(um100)
        data = [pm1_cf, pm10_cf, pm25_cf, um3, um5, um10, um25, um50, um100]
        self.serial.close()
        return data

    def read(self, argv):
        tty=argv[0:]
        self.conn_serial_port(tty)
        if self.check_keyword() == True:
            self.data = self.read_data()
            if debug: print self.data
            return self.data

if __name__ == '__main__':
    air=a4sensor()
    while True:
        pmdata=0
        try:
            pmdata=air.read("/dev/ttyAMA0")
        except:
            next
        if pmdata != 0:
            print pmdata
            break