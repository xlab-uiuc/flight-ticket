import redis
import random
import json
import time
import ast

class Seat:
    def __init__(self, _travelDate, _airplaneNumber, _startStation, _destStation, _seatType):
        self.travelDate = _travelDate
        self.airplaneNumber = _airplaneNumber
        self.startStation = _startStation
        self.destStation = _destStation
        self.seatType = _seatType

class AircraftType:
    def __init__(self, _id, _economyClass, _confortClass, _avgSpeed):
        self.id = _id
        self.economyClass = _economyClass
        self.confortClass = _confortClass
        self.avgSpeed = _avgSpeed

class Ticket: 
    def __init__(self, _seatNo, _startStation, _destStation):
        self.seatNo = _seatNo
        self.startStation = _startStation
        self.destStation = _destStation

class Route:
    def __init__(self, _id, _stations, _distances, _startStation, _destStation):
        self.id = _id
        self.stations = _stations
        self.distances = _distances
        self.startStation = _startStation
        self.destStation = _destStation

class LeftTicketInfo:
    def __init__(self, _soldTickets):
        self.soldTickets = _soldTickets

class Config:
    def __init__(self, _name, _value, _descr):
        self.name = _name
        self.value = _value
        self.descr = _descr

def fake_main(params):
    tripId = params["tripId"]
    airplaneType = AircraftType(random.randint(0,20), random.randint(150,350), random.randint(20,100), random.randint(120,200))
    print(json.dumps(airplaneType.__dict__))
    time.sleep(0.1)
    return {"Result":json.dumps(airplaneType.__dict__)}

def main(params):
    airplaneId = params["airplaneTypeId"]
    myclient = redis.Redis(host="host.minikube.internal",port="6379",db=1)
    airplaneTypeRedisByte = myclient.hget("airplaneType",airplaneId)
    airplaneTypeRedisStr = airplaneTypeRedisByte.decode("utf-8")
    airplaneTypeRedis = ast.literal_eval(airplaneTypeRedisStr)
    airplaneType = AircraftType(airplaneTypeRedis["id"],airplaneTypeRedis["economyClass"],airplaneTypeRedis["confortClass"],airplaneTypeRedis["avgSpeed"])
    print(json.dumps(airplaneType.__dict__))
    return {"Result":json.dumps(airplaneType.__dict__)}
