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

class Order:
    def __init__(self, _id, _boughtDate, _travelDate, _travelTime, _accountId, _contactsName, _docType, _docNum, _airplaneNum, _coachNum, _seatClass, _seatNum, _stFrom, _stTo, _stat, _price):
        self.id = _id
        self.boughtDate = _boughtDate
        self.travelDate = _travelDate
        self.travelTime = _travelTime
        self.accountId = _accountId
        self.contactsName = _contactsName
        self.docType = _docType
        self.docNum = _docNum
        self.airplaneNum = _airplaneNum
        self.coachNum = _coachNum
        self.seatClass = _seatClass
        self.seatNum = _seatNum
        self.stFrom = _stFrom
        self.stTo = _stTo
        self.stat = _stat
        self.price = _price

def main(params):
    print(params)
    dictText_1 = params
    dictText_1 = dictText_1.get('order', {})
    orderResult = Order(dictText_1.get("id"),dictText_1.get("boughtDate"),dictText_1.get("travelDate"),dictText_1.get("travelTime"),dictText_1.get("accountId"),dictText_1.get("contactsName"),dictText_1.get("docType"),dictText_1.get("docNum"),dictText_1.get("airplaneNum"),dictText_1.get("coachNum"),dictText_1.get("seatClass"),dictText_1.get("seatNum"),dictText_1.get("stFrom"),dictText_1.get("stTo"),dictText_1.get("stat"),dictText_1.get("price"))
    myclient = redis.Redis(host="host.minikube.internal",port="6379",db=1)
    print(params)
    print(orderResult.id)
    orderId = orderResult.id
    if (myclient.hget("boughtDate",orderId)==None):
        return {"Result":0}
        
    myclient.hset("boughtDate",orderId,orderResult.boughtDate)
    myclient.hset("travelTime",orderId,orderResult.travelTime)
    myclient.hset("travelDate",orderId,orderResult.travelDate)
    myclient.hset("accountId",orderId,orderResult.accountId)
    myclient.hset("contactsName",orderId,orderResult.contactsName)
    myclient.hset("docType",orderId,orderResult.docType)
    myclient.hset("docNum",orderId,orderResult.docNum)
    myclient.hset("airplaneNum",orderId,orderResult.airplaneNum)
    myclient.hset("coachNum",orderId,orderResult.coachNum)
    myclient.hset("seatClass",orderId,orderResult.seatClass)
    myclient.hset("seatNum",orderId,orderResult.seatNum)
    myclient.hset("stat",orderId,orderResult.stat)
    myclient.hset("stFrom",orderId,orderResult.stFrom)
    myclient.hset("stTo",orderId,orderResult.stTo)
    myclient.hset("price",orderId,orderResult.price)

    return {"Result":1}
