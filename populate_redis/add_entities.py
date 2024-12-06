import json
import random
import redis
import ast

myclient = redis.Redis(host="localhost", port=6379, db=1)

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