#!/usr/bin/python
#!/usr/bin/env python
# coding: utf-8

import redis
import json
import time
import argparse
import sys
import paho.mqtt.client as mqtt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
import socket

opt = argparse.ArgumentParser(description='xxx')
opt.add_argument('-i', '--id',       help='`product id', default='iot')
opt.add_argument('-e', '--endpoint', help='`aws endpoint', default='')
opt.add_argument('-t', '--tenantid', help='`tenant id',   default='test')
#opt.add_argument('-u', '--usb',    help='USB Device',  default='/dev/ttyACM0')
args = opt.parse_args()



conn = redis.StrictRedis(host='localhost', port=6379)
key  = 'sensor/send'

count = 0
while True:
   topic = args.id + '/' + args.tenantid + '/sensor'
   n = datetime.now()
   st = (int(n.strftime('%s')) / 60) * 60
   now = n.isoformat()
   hostname = socket.gethostname()
   did = "ttySYSTEM0"
   msg_ori = {
      "id": hostname + "/" + did,
      "device": did,
      "hostname": hostname,
      "timeserial": st,
      "timestamp": now,
      "value": 1,
   }
   msg = json.dumps(msg_ori)
   print(topic + ':' + msg + "\n")
   conn.rpush('sensor/send', msg)
   count += 1
   print("success push:", count)
   print(conn.llen(key))
   time.sleep(5)

