import os
import glob
import pandas as pd
import redis
from concurrent.futures import ProcessPoolExecutor

def process_file(file_path):
    print(f"Processing file: {file_path}")
    unique_stations = set()
    with pd.read_stata(file_path, iterator=True) as reader:
        try:
            while True:
                chunk = reader.read(1000)
                unique_stations.update(chunk['origin'].unique())
                unique_stations.update(chunk['destination'].unique())
        except StopIteration:
            pass
    return unique_stations

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 1))

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True, db=redis_db)
station_key = "station"
redis_client.delete(station_key)
data_in = os.path.join(os.getcwd(), "clean/raw/")
file_paths = glob.glob(os.path.join(data_in, "DB1B_TICKETS_COUPONS_2016_1*"))

all_unique_stations = set()
with ProcessPoolExecutor() as executor:
    results = executor.map(process_file, file_paths)
    for result in results:
        all_unique_stations.update(result)

j = 1
for station in all_unique_stations:
    redis_client.hset(station_key, station, f"sID_{j}")
    j +=1 

total_stations = redis_client.hlen(station_key)
print(f"Total stations: {total_stations}")
