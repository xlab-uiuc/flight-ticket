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

class Order:
    def __init__(self, _id, _boughtDate, _travelDate, _travelTime, _accountId, _contactsName, _docType, _docNum, _planeNum, _coachNum, _seatClass, _seatNum, _stFrom, _stTo, _stat, _price):
        self.id = _id
        self.boughtDate = _boughtDate
        self.travelDate = _travelDate
        self.travelTime = _travelTime
        self.accountId = _accountId
        self.contactsName = _contactsName
        self.docType = _docType
        self.docNum = _docNum
        self.planeNum = _planeNum
        self.coachNum = _coachNum
        self.seatClass = _seatClass
        self.seatNum = _seatNum
        self.stFrom = _stFrom
        self.stTo = _stTo
        self.stat = _stat
        self.price = _price


def main(params):
    money = float(params["money"])
    user = params["loginId"]

    config = utils.load_config()
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    myclient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
    
    oldValue = myclient.hget("money", user)
    if oldValue is None:
        oldValue = 0.0
    else:
        oldValue = float(oldValue.decode())

    newValue = oldValue + money

    myclient.hset("money", user, str(newValue))
    return {"Result": 1}
