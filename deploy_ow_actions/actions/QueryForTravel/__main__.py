import requests
import json
import time
from utils import utils

class Seat:
    def __init__(self, _travelDate, _planeNumber, _startStation, _destStation, _seatType):
        self.travelDate = _travelDate
        self.planeNumber = _planeNumber
        self.startStation = _startStation
        self.destStation = _destStation
        self.seatType = _seatType

class planeType:
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

class TravelResult:
    def __init__(self, _status, _percent, _planeType, _prices):
        self.status = _status
        self.percent = _percent
        self.planeType = _planeType
        self.prices = _prices

    def to_dict(self):
        return {
            "status": self.status,
            "percent": self.percent,
            "planeType": self.planeType,
            "prices": self.prices
        }

def main(params):

    returnResult = TravelResult(True, 100, 1, {"map":"map"})
    config = utils.load_config()
    WSK_API_HOST = config.get("WSK_API_HOST")
    WSK_AUTH_KEY = config.get("WSK_AUTH_KEY")
    user_pass = WSK_AUTH_KEY.split(':')
    base_url = WSK_API_HOST + '/api/v1/namespaces/guest/actions/'
    url_func_3 = base_url + "get-route-by-route-id"
    url_func_4 = base_url + "get-plane-type-by-plane-type-id"
    url_func_5 = base_url + "get-price-by-route-id-and-plane-type"
    url_func_7 = base_url + "query-for-station-id-by-station-name"
    authentication = (user_pass[0], user_pass[1])
    parameters = {'blocking': 'true', 'result': 'true'}

    startSt = params["start"]
    endSt = params["end"]
    seatClass = params["seatClass"]

    arguments = {"stationName":startSt}
    start = time.time()
    future = requests.post(url_func_7, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    print(future.text)
    jsonText_1 = json.loads(future.text)
    print("invoking query_for_station_id_by_station_name")
    startId = jsonText_1["Result"]

    arguments = {"stationName":endSt}
    start = time.time()
    future = requests.post(url_func_7, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    print(future.text)
    jsonText_1 = json.loads(future.text)
    endId = jsonText_1["Result"]

    if (startId == -1 or endId == -1):
        returnResult.status = False
        return {"Result": returnResult}
    
    planeTypeId = params["planeTypeId"]
    arguments = {"planeTypeId":planeTypeId}
    start = time.time()
    future = requests.post(url_func_4, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    print(future.text)
    jsonText_1 = json.loads(future.text)
    planeType = jsonText_1["Result"]

    if (planeType == "None"):
        returnResult.status = False
        return {"Result": returnResult}
    
    routeId = params["rId"]
    arguments = {'rId':routeId}
    start = time.time()
    future = requests.post(url_func_3, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    print(future.text)
    jsonText_1 = json.loads(future.text)
    dictText_1 = json.loads(jsonText_1["Result"])
    routeResult = Route(dictText_1["id"],dictText_1["stations"],dictText_1["distances"],dictText_1["startStation"],dictText_1["destStation"])

    arguments = {"stationName":startSt}
    start = time.time()
    future = requests.post(url_func_7, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    print(future.text)
    jsonText_1 = json.loads(future.text)
    startId = jsonText_1["Result"]

    arguments = {"stationName":endSt}
    start = time.time()
    future = requests.post(url_func_7, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    print(future.text)
    jsonText_1 = json.loads(future.text)
    endId = jsonText_1["Result"]

    planeTypeStr = planeType
    arguments = {"planeType":planeTypeStr, "rId":routeId, "seatClass":seatClass}
    start = time.time()
    future = requests.post(url_func_5, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    print(future.text)
    jsonText_1 = json.loads(future.text)
    print(jsonText_1)
    dictText_1 = jsonText_1["Result"]
    print(dictText_1)
    basic_rate = dictText_1["basic_rate"]
    first_class_rate = dictText_1["first_class_rate"] 
    print(basic_rate)
    print(first_class_rate)

    print(f"routeResult.stations: {routeResult.stations}")
    indexStart = routeResult.stations.index(startSt)
    print(f"indexStart: {indexStart}")
    indexEnd = routeResult.stations.index(endSt)
    print(f"indexEnd: {indexEnd}")
    print(f"routeResult.distances: {routeResult.distances}")

    distance = routeResult.distances
    print(f"Distances: {distance}")
    prices = {}
    prices["basic"] = distance * basic_rate
    prices["first_class"] = distance * first_class_rate

    returnResult.prices = prices
    returnResult.percent = 1
    returnResult.planeType = planeType

    return {
        "Result": {
            "status": returnResult.status,
            "percent": returnResult.percent,
            "planeType": returnResult.planeType,
            "prices": returnResult.prices
        }
    }
