import json
import time
import redis
import ast
import os

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

def main(params):
    config = utils.load_config()
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    routeId = params["rId"]
    myclient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,db=1)
    stations = ast.literal_eval(myclient.hget("stations",routeId).decode("utf-8"))
    distances = ast.literal_eval(myclient.hget("distances",routeId).decode("utf-8"))
    startStation = myclient.hget("startStation",routeId).decode("utf-8")
    destStation = myclient.hget("destStation",routeId).decode("utf-8")
    routeResult = Route(routeId, stations, distances, startStation, destStation)
    return {"Result":json.dumps(routeResult.__dict__)}
