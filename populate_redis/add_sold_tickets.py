import os
import glob
import pandas as pd
import redis
import json
from concurrent.futures import ProcessPoolExecutor

def process_file(file_path, chunk_size=10000):
    print(f"Processing file: {file_path}")
    ticket_data = []
    with pd.read_stata(file_path, chunksize=chunk_size) as reader:
        for chunk in reader:
            chunk = chunk[['flight_id', 'ritinfare', 'origin', 'destination', 'year', 'quarter']].dropna()
            ticket_data.append(chunk)
    return pd.concat(ticket_data, ignore_index=True)

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, db=1)
sold_tickets_key = "soldTickets"

redis_client.delete(sold_tickets_key)

data_in = os.path.join(os.getcwd(), "clean/raw/")
file_paths = glob.glob(os.path.join(data_in, "DB1B_TICKETS_COUPONS_2016_1*"))

all_tickets = []
with ProcessPoolExecutor() as executor:
    results = executor.map(process_file, file_paths)
    for result in results:
        all_tickets.append(result)

combined_tickets = pd.concat(all_tickets, ignore_index=True)
grouped = combined_tickets.groupby('flight_id')
pipeline = redis_client.pipeline()

for flight_id, group in grouped:
    tickets = []
    for _, row in group.iterrows():
        ticket = {
            "seatNo": round(row['ritinfare']),
            "startStation": row['origin'],
            "destStation": row['destination'],
            "date": f"{int(row['year'])}-{int(row['quarter'])}"
        }
        tickets.append(ticket)
    
    pipeline.hset(sold_tickets_key, str(int(flight_id)), json.dumps(tickets))

pipeline.execute()

total_flights = redis_client.hlen(sold_tickets_key)
print(f"Total flights stored : {total_flights}")
