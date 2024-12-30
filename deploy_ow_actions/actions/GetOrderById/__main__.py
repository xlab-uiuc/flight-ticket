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
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    orderId = params["orderId"]
    myclient = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=1)
    ordBoughtDate = myclient.hget("boughtDate",orderId).decode("utf-8")
    ordTravelTime = myclient.hget("travelTime",orderId).decode("utf-8")
    ordTravelDate = myclient.hget("travelDate",orderId).decode("utf-8")
    ordAccountId = myclient.hget("accountId",orderId).decode("utf-8")
    ordContactsName = myclient.hget("contactsName",orderId).decode("utf-8")
    ordDocType = myclient.hget("docType",orderId).decode("utf-8")
    ordDocNum = myclient.hget("docNum",orderId).decode("utf-8")
    ordPlaneNum = myclient.hget("planeNum",orderId).decode("utf-8")
    ordCoachNum = myclient.hget("coachNum",orderId).decode("utf-8")
    ordSeatClass = myclient.hget("seatClass",orderId).decode("utf-8")
    ordSeatNum = myclient.hget("seatNum",orderId).decode("utf-8")
    ordStat = myclient.hget("stat",orderId).decode("utf-8")
    ordStFrom = myclient.hget("stFrom",orderId).decode("utf-8")
    ordStTo = myclient.hget("stTo",orderId).decode("utf-8")
    ordPrice = myclient.hget("price",orderId).decode("utf-8")

    orderResult = Order(orderId, ordBoughtDate, ordTravelDate, ordTravelTime, ordAccountId, ordContactsName, ordDocType, ordDocNum, ordPlaneNum,
        ordCoachNum, ordSeatClass, ordSeatNum, ordStFrom, ordStTo, ordStat, ordPrice)
    return {"Result":json.dumps(orderResult.__dict__)}
