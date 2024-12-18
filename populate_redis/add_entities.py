import json
import random
import redis
import ast
import os

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 1))

myclient = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

def generate_percent():
    randNum = random.randint(0, 100)
    percent = float(randNum / 100)
    value = {
        "value": percent
    }
    return value

trips = myclient.hgetall("trips")
trips = {key.decode('utf-8'): ast.literal_eval(value.decode('utf-8')) for key, value in trips.items()}

for trip_key, trip_value in trips.items():
    myclient.hset("entities", json.dumps(trip_value), json.dumps(generate_percent()))

print("entities added")