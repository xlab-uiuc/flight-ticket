import random
import redis
import json

myclient = redis.Redis(host="localhost", port=6379, db=1)

def generate_percent():
    randNum = random.randint(0, 100)
    percent = float(randNum / 100)
    value = {
        "value": percent
    }
    return value

for i in range(1, 401):
    myclient.hset("entities", f"t{i}", json.dumps(generate_percent()))
