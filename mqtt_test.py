import paho.mqtt.client as mqtt
import redis

host = "192.168.0.2"
key = "sensor/send"

conn = redis.StrictRedis(host="localhost", port=6379)
msg = conn.lindex(key, 0)

mq = mqtt.Client(protocol=mqtt.MQTTv311)
mq_result, _ = mq.publish(topic, msg, 0)

