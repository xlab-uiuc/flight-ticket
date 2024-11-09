import os
import glob
from concurrent.futures import ProcessPoolExecutor
import pandas as pd

def process_file(file_path):
    print(f"Processing file: {file_path}")
    filtered_rows = []
    with pd.read_stata(file_path, iterator=True) as reader:
        try:
            while True:
                # Read file in chunks
                chunk = reader.read(1000)  # Adjust chunk size as needed
                # Filter rows where 'num_connections' is not 1
                for _, row in chunk[chunk['itinid'] != 1].iterrows():
                    print(row.to_dict())
                    filtered_rows.append(row.to_dict())
        except StopIteration:
            pass
    return filtered_rows

current_path = os.getcwd()
data_in = os.path.join(current_path, "clean/raw/")
file_paths = glob.glob(os.path.join(data_in, "DB1B_TICKETS_COUPONS_2016_1*"))

with ProcessPoolExecutor() as executor:
    results = list(executor.map(process_file, file_paths))

for idx, rows in enumerate(results):
    print(f"Filtered rows in file {file_paths[idx]}:")
    for row in rows:
        print(row)
