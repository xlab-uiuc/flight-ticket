import numpy as np
import subprocess
import redis
import argparse
import random
import ast
import time
import os
from datetime import datetime, timedelta

def EnforceActivityWindow(start_time, end_time, instance_events):
    events_iit = []
    events_abs = [0] + instance_events
    event_times = [sum(events_abs[:i]) for i in range(1, len(events_abs) + 1)]
    event_times = [e for e in event_times if (e > start_time) and (e < end_time)]
    try:
        events_iit = [event_times[0]] + [event_times[i] - event_times[i - 1] for i in range(1, len(event_times))]
    except:
        pass
    return events_iit

def calculate_p99(latencies):
    return np.percentile(latencies, 99)

def write_p99_to_file(latencies, file_name="p99.txt"):
    p99_latency = calculate_p99(latencies)
    with open(file_name, "w") as f:
        f.write(f'P99 latency: {p99_latency} ms\n')

def calculate_average(latencies):
    return sum(latencies) / len(latencies) if latencies else 0

def write_average_latency_to_file(latencies, file_name="average_latency.txt"):
    avg_latency = calculate_average(latencies)
    with open(file_name, "w") as f:
        f.write(f'Average latency: {avg_latency:.2f} ms\n')

def time_invocation(command):
    print('Running command:', command)
    start = time.time()
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 202:
            print(f"Ignoring exit code 202 meaning the request is taking longer than expected; no problem: {e}")
    end = time.time()
    return (end - start) * 1000

# running query-for-travel
# wsk -i action invoke query-for-travel --param start "SFO" --param end "SFO" --param "planeTypeId" 201601387274 --param "rId" SFOPHXBOSCLTSFO --param seatClass "economyClass" --blocking --result
def invoke_query(client):
    stations = client.hgetall("stations")
    stations = {key.decode('utf-8'): ast.literal_eval(value.decode('utf-8')) for key, value in stations.items()}
    keys = client.hkeys("stations")
    random_route = random.choice(keys).decode('utf-8')

    route = stations.get(random_route)
    start_index = random.randint(0, len(route) - 2)
    end_index = random.randint(start_index + 1, len(route) - 1)

    # grab station names
    startSt = route[start_index]
    endSt = route[end_index]

    # grab plane
    random_plane = client.hget("trips", random_route).decode('utf-8')

    # select random seat class
    seat_class = random.choice(["economyClass", "confortClass"])

    # invoke query-for-travel
    invoke_query_cmd = f"wsk -i action invoke query-for-travel --param start \"{startSt}\" --param end \"{endSt}\" --param planeTypeId \"{random_plane}\" --param rId \"{random_route}\" --param seatClass \"{seat_class}\" --result --blocking"
    print('invoking query for travel')
    return time_invocation(invoke_query_cmd)

# running seat-service
# wsk -i action invoke seat-service --param tripId "201601387274" --param "date" "12-23-2024" --param startStation "SFO" --param destStation "SFO" --param seatClass "economyClass" --blocking --result
def invoke_seat_service(client):
    stations = client.hgetall("stations")
    stations = {key.decode('utf-8'): ast.literal_eval(value.decode('utf-8')) for key, value in stations.items()}
    keys = client.hkeys("stations")
    random_route = random.choice(keys).decode('utf-8')

    print(random_route)
    route = stations.get(random_route)
    start_index = random.randint(0, len(route) - 2)
    end_index = random.randint(start_index + 1, len(route) - 1)

    # grab station names
    startSt = route[start_index]
    endSt = route[end_index]

    trip_id = client.hget("trips", random_route).decode('utf-8')

    travel_date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    seat_class = random.choice(["economyClass", "confortClass"])

    invoke_seat_service_cmd = f"wsk -i action invoke seat-service --param tripId \"{trip_id}\" --param date \"{travel_date}\" --param startStation \"{startSt}\" --param destStation \"{endSt}\" --param seatClass \"{seat_class}\" --result --blocking"
    print('invoking seat service')
    return time_invocation(invoke_seat_service_cmd)

# running cancel-service
# after running this we must change back the 'stat' of the orders
# wsk -i action invoke cancel-service --param orderId "ord-200" --param loginId "id_444" --blocking --result
def invoke_cancel_service(calls_count):
    order = f"ord-{random.randint(1,200)}"
    loginId = f"id_{random.randint(1,600)}"

    if calls_count % 50 == 0 and calls_count != 0:
        reset_orders_to_active_status_cmd = "python3 populate_redis/reset_order_status.py"
        print('resetted order status')
        subprocess.run(reset_orders_to_active_status_cmd, shell=True, check=True)

    invoke_cancel_service_cmd = f"wsk -i action invoke cancel-service --param orderId \"{order}\" --param loginId \"{loginId}\" --result --blocking"
    print('Invoking cancel service')
    return time_invocation(invoke_cancel_service_cmd)


def main():
    seed = 100
    loads = [1]
    load_desc = ["LOW_LOAD", "MED_LOAD", "HIGH_LOAD"]
    np.random.seed(100)

    parser = argparse.ArgumentParser(description='Process args')
    parser.add_argument('--minutes', type=str, help='Duration in minutes to run the workflow')
    args = parser.parse_args()
    minutes = 60 * int(args.minutes)
    calls_count = 0
    latencies = []

    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    redis_db = int(os.getenv('REDIS_DB', 1))

    client = redis.Redis(host='owdev-redis.openwhisk.svc.cluster.local', port=6379, db=1)

    start_time = time.time()
    while time.time() - start_time < minutes:
        for load in loads:
            # generate Poisson's distribution of events 
            seed = 101
            np.random.seed(seed)
            rate = load / 60
            inter_arrivals = list(np.random.exponential(scale=1.0 / rate, size=int(2 * minutes * rate)))
            instance_events = EnforceActivityWindow(0, minutes, inter_arrivals)

            start_time = time.time()
            for inter_arrival in instance_events:
                if time.time() - start_time > minutes:
                    break

                print(inter_arrival)
                
                latencies.append(invoke_cancel_service(calls_count))
                latencies.append(invoke_query(client))
                latencies.append(invoke_seat_service(client))
                
                calls_count += 1

                # wait for the next event (inter-arrival time)
                time.sleep(inter_arrival)
                
    write_p99_to_file(latencies)
    write_average_latency_to_file(latencies)

if __name__ == "__main__":
    main()
