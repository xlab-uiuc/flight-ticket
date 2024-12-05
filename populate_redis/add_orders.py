import random
import redis
import string
from datetime import datetime, timedelta

myclient = redis.Redis(host="localhost", port=6379, db=1)

def random_date():
    start_date = datetime.now() - timedelta(days=365)
    return (start_date + timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")

def random_time():
    return f"{random.randint(0, 23):02}:{random.randint(0, 59):02}"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_price():
    return round(random.uniform(10, 500), 2)

contact_names = [
    "Liam Smith", "Olivia Johnson", "Noah Williams", "Emma Brown", "Oliver Jones",
    "Sophia Miller", "James Davis", "Ava Garcia", "William Martinez", "Isabella Rodriguez",
    "Benjamin Lee", "Mia Wilson", "Lucas Moore", "Charlotte Taylor", "Henry Anderson",
    "Amelia Thomas", "Alexander Harris", "Harper Martin", "Sebastian Jackson", "Evelyn Thompson",
    "Ethan White", "Abigail Lewis", "Michael Walker", "Ella Young", "Daniel King",
    "Aria Scott", "Matthew Green", "Lily Adams", "David Hall", "Sofia Campbell",
    "Jacob Baker", "Scarlett Mitchell", "Logan Perez", "Avery Roberts", "Jackson Turner",
    "Chloe Phillips", "Levi Carter", "Nora Gonzalez", "Mateo Rivera", "Layla Nelson",
    "Elijah Carter", "Grace Parker", "Jack Evans", "Zoe Edwards", "Owen Collins",
    "Victoria Cooper", "Samuel Sanders", "Ella Bell", "Joseph Torres", "Lillian Howard",
    "Joshua Ramirez", "Hannah Ward", "Luke Brooks", "Natalie Morgan", "Mason Bryant"
]

stations = myclient.hgetall("station")
station_names = [name.decode('utf-8') for name in stations.values()]

for i in range(1, 201):
    order_id = f"ord-{i}"
    bought_date = random_date()
    travel_date = random_date()
    travel_time = random_time()
    account_id = random_string(12)
    contacts_name = random.choice(contact_names)
    doc_type = random.choice(["Passport", "Driver License", "ID Card"])
    doc_num = random_string(9)
    plane_num = random.randint(1000, 9999)
    coach_num = random.randint(1, 20)
    seat_class = random.choice(["Economy", "Comfort", "Business"])
    seat_num = random.randint(1, 100)
    
    st_from = random.choice(station_names)
    st_to = random.choice(station_names)
    while st_from == st_to:
        st_to = random.choice(station_names)
    
    stat = random.randint(0, 2)
    price = random_price()

    myclient.hset("boughtDate", order_id, bought_date)
    myclient.hset("travelDate", order_id, travel_date)
    myclient.hset("travelTime", order_id, travel_time)
    myclient.hset("accountId", order_id, account_id)
    myclient.hset("contactsName", order_id, contacts_name)
    myclient.hset("docType", order_id, doc_type)
    myclient.hset("docNum", order_id, doc_num)
    myclient.hset("planeNum", order_id, plane_num)
    myclient.hset("coachNum", order_id, coach_num)
    myclient.hset("seatClass", order_id, seat_class)
    myclient.hset("seatNum", order_id, seat_num)
    myclient.hset("stFrom", order_id, st_from)
    myclient.hset("stTo", order_id, st_to)
    myclient.hset("stat", order_id, stat)
    myclient.hset("price", order_id, price)

print("200 random orders added to Redis.")

