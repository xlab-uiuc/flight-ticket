import redis
import os
from datetime import datetime, timedelta

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 1))

myclient = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
stations = myclient.hgetall("station")

j = 1
for i in stations:
    myclient.hset("sId", f"sID_{j}", i)
    j += 1
