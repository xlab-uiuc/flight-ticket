import os
import glob
import pandas as pd
import redis
from concurrent.futures import ProcessPoolExecutor
import json

def process_file(file_path, chunk_size=10000):
    print(f"Processing file: {file_path}")
    routes_data = []
    with pd.read_stata(file_path, chunksize=chunk_size) as reader:
        for chunk in reader:
            chunk = chunk[['route', 'distance', 'origin', 'destination']].dropna()
            routes_data.append(chunk)
    return pd.concat(routes_data, ignore_index=True)

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 1))

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True, db=redis_db)
stations_key = "stations"
distances_key = "distances"
start_station_key = "startStation"
dest_station_key = "destStation"

redis_client.delete(stations_key)
redis_client.delete(distances_key)
redis_client.delete(start_station_key)
redis_client.delete(dest_station_key)

data_in = os.path.join(os.getcwd(), "clean/raw/")
file_paths = glob.glob(os.path.join(data_in, "DB1B_TICKETS_COUPONS_2016_1*"))

all_routes = []
with ProcessPoolExecutor() as executor:
    results = executor.map(process_file, file_paths)
    for result in results:
        all_routes.append(result)

combined_data = pd.concat(all_routes, ignore_index=True).drop_duplicates(subset='route')
combined_data['stations'] = combined_data['route'].apply(lambda x: json.dumps([x[i:i+3] for i in range(0, len(x), 3)]))

pipeline = redis_client.pipeline()
for idx, row in combined_data.iterrows():
    pipeline.hset(stations_key, row['route'], row['stations'])
    pipeline.hset(distances_key, row['route'], row['distance'])
    pipeline.hset(start_station_key, row['route'], row['origin'])
    pipeline.hset(dest_station_key, row['route'], row['destination'])

pipeline.execute()

total_routes = redis_client.hlen(stations_key)
print(f"Total routes: {total_routes}")
