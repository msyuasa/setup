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

host = args.endpoint
rootCA = './pki/root-CA.crt'
cert = './pki/cert.pem'
key = './pki/private-key.pem'

host_type = "aws"
mq = AWSIoTMQTTClient("basicPubSub")
mq.configureEndpoint(host, 8883)
mq.configureCredentials(rootCA, key, cert)
try:
      mq.connect()
except Exception as e:
   try:
      host_type = "local"
      mq = mqtt.Client(protocol=mqtt.MQTTv311)
      mq.connect(host)
   except Exception as e:
      import traceback
      print(e)
      traceback.print_exc()
      sys.exit(1)


conn = redis.StrictRedis(host='localhost', port=6379)
key  = 'sensor/send'

count = 0
while True:
   while true:
      topic = args.id + '/' + args.tenantid + '/sensor'
      msg_ori = 
      n = datetime.now()
      st = (int(n.strftime('%s')) / 60) * 60
      now = n.isoformat()
      hostname = socket.gethostname()
      msg_ori = {
         "id": hostname + "/" + did,
         "device": "ttySYSTEM0",
         "hostname": hostname,
         "timeserial": st,
         "timestamp": now,
         "value": 1,
      }
      msg = json.dumps(msg)
      print(host_type + ':' + topic + ':' + msg + "\n");
      if isinstance(mq, mqtt.Client):
         #mq.publish(topic, msg, 1)
         mq_result = mq.publish(topic, msg, 1)
         if mq_result[0] is mqtt.MQTT_ERR_SUCCESS:
            print('send succes:')
            count += 1
      else:
         #mq.publish(topic, msg, 1)
         mq_result = mq.publish(topic, msg, 1)
         if mq_result:
                print('send succes:')
                count += 1
      time.sleep(5)
   if isinstance(mq, mqtt.Client):
      mq.reconnect()
