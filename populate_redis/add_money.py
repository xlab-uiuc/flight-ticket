import random
import redis
import string
from datetime import datetime, timedelta
import os

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 1))

myclient = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

def generate_money():
    return round(random.uniform(10, 1000000), 2)

for i in range(1, 601):
    money = generate_money()
    userId = f"id_{i}"
    myclient.hset("money", userId, money)

print("Money added")
