import os
import glob
import pandas as pd
import redis
from concurrent.futures import ProcessPoolExecutor
import json

def process_file(file_path, chunk_size=10000):
    print(f"Processing file: {file_path}")
    trip_data = []
    with pd.read_stata(file_path, chunksize=chunk_size) as reader:
        for chunk in reader:
            chunk = chunk[['flight_id', 'route']].dropna()
            trip_data.append(chunk)
    return pd.concat(trip_data, ignore_index=True)

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, db=1)
trips_key = "rId"
redis_client.delete(trips_key)
data_in = os.path.join(os.getcwd(), "clean/raw/")
file_paths = glob.glob(os.path.join(data_in, "DB1B_TICKETS_COUPONS_2016_1*"))

all_trips = []
with ProcessPoolExecutor() as executor:
    results = executor.map(process_file, file_paths)
    for result in results:
        all_trips.append(result)

combined_trips = pd.concat(all_trips, ignore_index=True).drop_duplicates(subset='flight_id')
pipeline = redis_client.pipeline()
for _, row in combined_trips.iterrows():
    pipeline.hset(trips_key, int(row['flight_id']), row['route'])
pipeline.execute()

total_trips = redis_client.hlen(trips_key)
print(f"Total trips stored: {total_trips}")
