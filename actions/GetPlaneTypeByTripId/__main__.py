import redis
import random
import json
import time
import ast

class Seat:
    def __init__(self, _travelDate, _planeNumber, _startStation, _destStation, _seatType):
        self.travelDate = _travelDate
        self.planeNumber = _planeNumber
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
    planeType = AircraftType(random.randint(0,20), random.randint(150,350), random.randint(20,100), random.randint(120,200))
    print(json.dumps(planeType.__dict__))
    time.sleep(0.1)
    return {"Result":json.dumps(planeType.__dict__)}

def main(params):
    tripId = params["tripId"]
    myclient = redis.Redis(host="host.minikube.internal",port="6379",db=1)
    planeTypeRedisByte = myclient.hget("planeType",tripId)
    planeTypeRedisStr = planeTypeRedisByte.decode("utf-8")
    planeTypeRedis = ast.literal_eval(planeTypeRedisStr)
    planeType = AircraftType(planeTypeRedis["id"],planeTypeRedis["economyClass"],planeTypeRedis["confortClass"],planeTypeRedis["avgSpeed"])
    print(json.dumps(planeType.__dict__))
    return {"Result":json.dumps(planeType.__dict__)}
