import random
import redis
import string
from datetime import datetime, timedelta

myclient = redis.Redis(host="localhost", port=6379, db=1)

def generate_money():
    return round(random.uniform(10, 1000000), 2)

for i in range(1, 601):
    money = generate_money()
    userId = f"id_{i}"
    myclient.hset("money", userId, money)

print("Money added")
