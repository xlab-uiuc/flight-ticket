import json
import time
import redis
import ast

class Seat:
    def __init__(self, _travelDate, _airplaneNumber, _startStation, _destStation, _seatType):
        self.travelDate = _travelDate
        self.airplaneNumber = _airplaneNumber
        self.startStation = _startStation
        self.destStation = _destStation
        self.seatType = _seatType

class AirairplaneType:
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
    stationName = params["stationName"]
    myclient = redis.Redis(host="host.minikube.internal",port="6379",db=1)
    stationId = myclient.hget("station",stationName)
    if stationId == None:
        return {"Result": -1}
    return {"Result":stationId}
