import requests
import json
import time
from datetime import datetime

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

class Order:
    def __init__(self, _id, _boughtDate, _travelDate, _travelTime, _accountId, _contactsName, _docType, _docNum, _trainNum, _coachNum, _seatClass, _seatNum, _stFrom, _stTo, _stat, _price):
        self.id = _id
        self.boughtDate = _boughtDate
        self.travelDate = _travelDate
        self.travelTime = _travelTime
        self.accountId = _accountId
        self.contactsName = _contactsName
        self.docType = _docType
        self.docNum = _docNum
        self.trainNum = _trainNum
        self.coachNum = _coachNum
        self.seatClass = _seatClass
        self.seatNum = _seatNum
        self.stFrom = _stFrom
        self.stTo = _stTo
        self.stat = _stat
        self.price = _price

def calcReturn(_myOrder):
    if _myOrder.stat == 0:
        return 0.0
    try:
        travel_date = datetime.strptime(_myOrder.travelDate, '%Y-%m-%d')
        travel_time = datetime.strptime(_myOrder.travelTime, '%H:%M').time()

        dateTravel = datetime.combine(travel_date, travel_time)
    except ValueError as e:
        print(f"Date conversion error: {e}")
        return 0.0

    dateNow = datetime.now()
    if dateNow > dateTravel:
        return 0.0

    return 0.8 * float(_myOrder.price)

def main(params):
    APIHOST = "https://192.168.49.2:31001"
    AUTH_KEY = "23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP" 
    user_pass = AUTH_KEY.split(':')
    base_url = APIHOST + '/api/v1/namespaces/guest/actions/'
    url_func_23 = base_url + "get-order-by-id"
    url_func_28 = base_url + "drawback"
    url_func_29 = base_url + "save-order-info"
    authentication = (user_pass[0], user_pass[1])
    parameters = {'blocking': 'true', 'result': 'true'}

    orderId = params["orderId"]
    loginId = params["loginId"]
    arguments = {'orderId':orderId}
    start = time.time()
    future = requests.post(url_func_23, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    try:
        jsonText_1 = json.loads(future.text)
        dictText_1 = json.loads(jsonText_1["Result"])
        orderResult = Order(dictText_1["id"],dictText_1["boughtDate"],dictText_1["travelDate"],dictText_1["travelTime"],dictText_1["accountId"],dictText_1["contactsName"],dictText_1["docType"],dictText_1["docNum"],dictText_1["trainNum"],dictText_1["coachNum"],dictText_1["seatClass"],dictText_1["seatNum"],dictText_1["stFrom"],dictText_1["stTo"],dictText_1["stat"],dictText_1["price"])
    except:
        return {"Order":"Not Found"}
    print(f"orderStat: {orderResult.stat}")
    if int(orderResult.stat) in [0, 1, 2]:
        print(orderResult.seatNum)
        orderResult.stat = 3

        arguments = {'order':orderResult.__dict__}
        start = time.time()
        future = requests.post(url_func_29, params=parameters, auth=authentication, json=arguments, verify=False)
        end = time.time()
        print(end - start)
        jsonText_2 = json.loads(future.text)
        response = int(jsonText_2["Result"])
        print(response)
        print(jsonText_2["Result"])
        if (response == 0):
            return {"Order":"Cannot cancel"}
        refund = calcReturn(orderResult)

        arguments = {'money':refund, 'loginId':loginId}
        start = time.time()
        future = requests.post(url_func_28, params=parameters, auth=authentication, json=arguments, verify=False)
        end = time.time()
        print(end - start)

        return {"Order":"Success"}

    else:
        return {"Order":"Not permitted operation"}
