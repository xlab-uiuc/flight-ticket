import os
import glob
import redis
import pandas as pd
import json
from concurrent.futures import ProcessPoolExecutor

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 1))

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True, db=redis_db)
priceRoute_key = "priceRoute"
redis_client.delete(priceRoute_key)
data_in = os.path.join(os.getcwd(), "clean/raw/")
file_paths = glob.glob(os.path.join(data_in, "DB1B_TICKETS_COUPONS_2016_1*"))

def process_file(file_path, chunk_size=10000):
    print(f"Processing file: {file_path}")
    route_prices = {}
    with pd.read_stata(file_path, chunksize=chunk_size) as reader:
        for chunk in reader:
            chunk = chunk[['route', 'ritinfare', 'price_productpassenger_weighted', 'passengers']].dropna()

            grouped = chunk.groupby('route').agg({
                'ritinfare': 'mean',
                'price_productpassenger_weighted': 'mean',
                'passengers': 'sum'
            }).reset_index()

            for _, row in grouped.iterrows():
                route_id = row['route']
                economy_basic = round(row['ritinfare'])
                economy_first_class = economy_basic + 500
                confort_basic = round(row['price_productpassenger_weighted'] * row['passengers'])
                confort_first_class = confort_basic + 500

                prices = {
                    "economyClass": {
                        "basic": economy_basic,
                        "first_class": economy_first_class
                    },
                    "confortClass": {
                        "basic": confort_basic,
                        "first_class": confort_first_class
                    }
                }
                route_prices[route_id] = json.dumps(prices)

    return route_prices

all_prices = {}
with ProcessPoolExecutor() as executor:
    results = executor.map(process_file, file_paths)
    for result in results:
        all_prices.update(result)

pipeline = redis_client.pipeline()
for route_id, price_data in all_prices.items():
    pipeline.hset(priceRoute_key, route_id, price_data)
pipeline.execute()

print(f"Total routes' prices added: {redis_client.hlen(priceRoute_key)}")
