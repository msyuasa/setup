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

mq.configureAutoReconnectBackoffTime(1, 16, 10)
mq.configureOfflinePublishQueueing(-1)
mq.configureDrainingFrequency(2)

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

while True:
    while conn.llen(key) <= 0:
      time.sleep(10)
    while conn.llen(key) > 0:
        topic = args.id + '/' + args.tenantid + '/sensor'
        #msg = conn.lpop(key)
        msg = conn.lindex(key, 0)
        sys.stderr.write(host_type + ':' + topic + ':' + msg + "\n");
        if isinstance(mq, mqtt.Client):
            #mq.publish(topic, msg, 1)
            mq_result, _  = mq.publish(topic, msg, 1)
            if mq_result is mqtt.MQTT_ERR_SUCCESS:
                delmsg = conn.lpop(key)
                sys.stderr.write('delete ' + host_type + ':' + topic + ':' + delmsg + "\n");
        else:
            #mq.publish(topic, msg, 1)
            mq_result = mq.publish(topic, msg, 1)
            if mq_result:
                delmsg = conn.lpop(key)
                sys.stderr.write('delete ' + host_type + ':' + topic + ':' + delmsg + "\n");
        time.sleep(1)
    if isinstance(mq, mqtt.Client):
        mq.reconnect()

