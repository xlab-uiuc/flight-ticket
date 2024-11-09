import redis
import json
import random

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

# Retrieve the station data from the existing "station" hash
station_data = r.hgetall("station")

# Convert station data into a dictionary with IDs as keys and names as values
station_dict = {int(station_id): station_name for station_name, station_id in zip(station_data.keys(), station_data.values())}

# Generate at least 100 random routes
num_routes = 100
stations_ids = list(station_dict.keys())
routes = []

for _ in range(num_routes):
    # Randomly select a start station
    start_station_id = random.choice(stations_ids)

    # Ensure the route includes the start station and at least two other stations
    route_length = random.randint(3, 6)  # Route length between 3 to 6 stations
    route = [start_station_id]

    # Add random stations ensuring no duplicates and at least one destination station
    while len(route) < route_length:
        station_id = random.choice(stations_ids)
        if station_id not in route:  # Prevent duplicates
            route.append(station_id)

    # Ensure the last station is different from the start
    if route[-1] == start_station_id:
        route[-1] = random.choice([s for s in stations_ids if s != start_station_id])

    routes.append(route)

# Store the routes as hashes
r.delete("stations")      # Clear any existing "stations" key data
r.delete("startStation")  # Clear existing "startStation" data
r.delete("destStation")   # Clear existing "destStation" data

for i, route in enumerate(routes):
    # Store route as a hash
    route_key = f"route:{i + 1}"  # Use route number as key
    r.hset(route_key, mapping={
        "stations": json.dumps(route),
        "startStation": station_dict[route[0]],
        "destStation": station_dict[route[-1]]
    })

# For easy retrieval, store a list of route keys
r.delete("routeList")  # Clear existing route list
for i in range(num_routes):
    r.rpush("routeList", f"route:{i + 1}")

print("Routes stored successfully in Redis.")

