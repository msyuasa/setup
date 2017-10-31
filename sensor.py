#!/usr/bin/python
#!/usr/bin/env python
# coding: utf-8

import sys
import os
import redis
import math
import serial
import json
import argparse
import socket
from datetime import datetime

conn = redis.StrictRedis(host='localhost', port=6379)

opt = argparse.ArgumentParser(description='xxx')
#opt.add_argument('-i', '--id',       help='`Product id', default='iot')
#opt.add_argument('-h', '--houseid',  help='`house id',   default='test')
#opt.add_argument('-u', '--usb',    help='USB Device',  default='/dev/ttyACM0')
opt.add_argument('-d', '--device',   help='Device ID',   default='ttyUSB0')
args = opt.parse_args()

#if not os.path.isfile(args.usb):
#  sys.exit(1)

hostname = socket.gethostname()

sys.stderr.write("start sensor:" + args.device + "\n")

minute = {}
s = serial.Serial('/dev/' + args.device, 9600)
while True:
    c = s.read()
    if c != chr(2):
        continue
    line = c
    for i in range(1,16):
        line = line + s.read();
    if '4' == line[1:2]:
        if not line[7:15].isdigit():
            continue
#        print line[7:15]
#        print line[6:7]
        val = float(line[7:15]) / math.pow(10, float(line[6:7]))
        n = datetime.now()
        pos = line[2:3]
        #if not minute.get(pos):
        if minute.get(pos) is None:
            minute[pos] = -1
        m = minute[pos]
        if n.year < 2000:
            continue
        if n.minute == m:
            continue
        did = args.device + line[2:3]
        if '1' == line[5:6]:
            val = val * 1
        if '01' == line[3:5]:
            unit = 'C'
        elif '02' == line[3:5]:
            unit = 'F'
        elif '04' == line[3:5]:
            unit = '%RH'
        elif '05' == line[3:5]:
            unit = 'ph'
        elif '19' == line [3:5]:
            unit = 'ppm'
        else:
            unit = 'V'
            val = val

        minute[pos] = n.minute
        st = (int(n.strftime('%s')) / 60) * 60
#        print datetime.fromtimestamp(st)
        now = n.isoformat()
        msg = {
          "id": hostname + "/" + did,
          "device": did,
          "hostname": hostname,
          "timeserial": st,
          "timestamp": now,
          "value": val,
          "unit": unit
         }
        sys.stderr.write(json.dumps(msg)+"\n")
        conn.rpush('sensor/send', json.dumps(msg))
