import json
import time
import redis
import ast

class Seat:
    def __init__(self, _travelDate, _trainNumber, _startStation, _destStation, _seatType):
        self.travelDate = _travelDate
        self.trainNumber = _trainNumber
        self.startStation = _startStation
        self.destStation = _destStation
        self.seatType = _seatType

class TrainType:
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
    routeId = params["rId"]
    trainType = params["trainType"]
    seatClass = params["seatClass"]
    myclient = redis.Redis(host="host.minikube.internal",port="6379",db=1)
    prices = myclient.hget("priceRoute", routeId)
    prices = prices.decode("utf-8") 
    prices = ast.literal_eval(prices)
    print(f"prices: {prices}")
    print(f"trainType: {trainType}")
    price = prices[seatClass]
    return {"Result": {"basic_rate":price["basic"], "first_class_rate":price["first_class"]}}
