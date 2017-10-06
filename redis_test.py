import redis

key = "sensor/send"

conn = redis.StrictRedis(host="localhost", port=6379)
print(conn.llen(key))
print(conn.lindex(key, 0))

