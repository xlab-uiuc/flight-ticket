import os
import glob
import redis
import pandas as pd
import json
import random
from concurrent.futures import ProcessPoolExecutor

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, db=1)
planeType_key = "planeType"
redis_client.delete(planeType_key)
data_in = os.path.join(os.getcwd(), "clean/raw/")
file_paths = glob.glob(os.path.join(data_in, "DB1B_TICKETS_COUPONS_2016_1*"))
route_plane_id_mapping = {}

def process_file(file_path, chunk_size=10000):
    print(f"Processing file: {file_path}")
    plane_types = {}

    with pd.read_stata(file_path, chunksize=chunk_size) as reader:
        for chunk in reader:
            chunk = chunk[['route', 'numpassengers_product']].dropna()

            for _, row in chunk.iterrows():
                route = row['route']
                num_passengers = int(row['numpassengers_product'])

                if route not in route_plane_id_mapping:
                    route_plane_id_mapping[route] = random.randint(1, 1000000)

                plane_id = route_plane_id_mapping[route]
                economy_class = num_passengers
                confort_class = max(0, num_passengers - 45)
                avg_speed = random.randint(0, 699)

                plane_type = {
                    "id": plane_id,
                    "economyClass": economy_class,
                    "confortClass": confort_class,
                    "avgSpeed": avg_speed,
                }

                plane_types[route] = json.dumps(plane_type)

    return plane_types

all_plane_types = {}
with ProcessPoolExecutor() as executor:
    results = executor.map(process_file, file_paths)
    for result in results:
        all_plane_types.update(result)

trip_ids = {}
for route in all_plane_types.keys():
    tripId = redis_client.hget("rId", route)
    if tripId:
        trip_ids[route] = tripId

pipeline = redis_client.pipeline()
for route, plane_type_data in all_plane_types.items():
    tripId = trip_ids.get(route)
    if tripId:
        pipeline.hset(planeType_key, tripId, plane_type_data)
pipeline.execute()

print(f"Total plane types stored in Redis: {redis_client.hlen(planeType_key)}")
