import random
import redis
import string
from datetime import datetime, timedelta

myclient = redis.Redis(host="localhost", port=6379, db=1)
myclient.delete("stat")

for order_id in range(1, 201):
    stat = random.randint(0,2)
    myclient.hset("stat", f"ord-{order_id}", stat)
