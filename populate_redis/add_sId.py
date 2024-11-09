import redis
from datetime import datetime, timedelta

myclient = redis.Redis(host="localhost", port=6379, db=1)
stations = myclient.hgetall("station")

j = 1
for i in stations:
    myclient.hset("sId", f"sID_{j}", i)
    j += 1
