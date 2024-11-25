import os
import glob
import redis
import pandas as pd
import json
import random
from concurrent.futures import ProcessPoolExecutor

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, db=1)
airplaneType_key = "airplaneType"
redis_client.delete(airplaneType_key)
data_in = os.path.join(os.getcwd(), "clean/raw/")
file_paths = glob.glob(os.path.join(data_in, "DB1B_TICKETS_COUPONS_2016_1*"))
route_airplane_id_mapping = {}

def process_file(file_path, chunk_size=10000):
    print(f"Processing file: {file_path}")
    airplane_types = {}

    with pd.read_stata(file_path, chunksize=chunk_size) as reader:
        for chunk in reader:
            chunk = chunk[['route', 'numpassengers_product']].dropna()

            for _, row in chunk.iterrows():
                route = row['route']
                num_passengers = int(row['numpassengers_product'])

                if route not in route_airplane_id_mapping:
                    route_airplane_id_mapping[route] = random.randint(1, 1000000)

                airplane_id = route_airplane_id_mapping[route]
                economy_class = num_passengers
                confort_class = max(0, num_passengers - 45)
                avg_speed = random.randint(0, 699)

                airplane_type = {
                    "id": airplane_id,
                    "economyClass": economy_class,
                    "confortClass": confort_class,
                    "avgSpeed": avg_speed,
                }

                airplane_types[route] = json.dumps(airplane_type)

    return airplane_types


all_airplane_types = {}
with ProcessPoolExecutor() as executor:
    results = executor.map(process_file, file_paths)
    for result in results:
        all_airplane_types.update(result)

pipeline = redis_client.pipeline()
for route, airplane_type_data in all_airplane_types.items():
    pipeline.hset(airplaneType_key, route, airplane_type_data)
pipeline.execute()

print(f"Total airplane types stored in Redis: {redis_client.hlen(airplaneType_key)}")
