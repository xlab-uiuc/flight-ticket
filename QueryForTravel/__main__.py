import requests
import json
import time

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

class TravelResult:
    def __init__(self, _status, _percent, _trainType, _prices):
        self.status = _status
        self.percent = _percent
        self.trainType = _trainType
        self.prices = _prices

    def to_dict(self):
        return {
            "status": self.status,
            "percent": self.percent,
            "trainType": self.trainType,
            "prices": self.prices
        }

def main(params):

    returnResult = TravelResult(True, 100, 1, {"map":"map"})
    APIHOST = "https://192.168.49.2:31001"
    AUTH_KEY = "23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP" 
    user_pass = AUTH_KEY.split(':')
    base_url = APIHOST + '/api/v1/namespaces/guest/actions/'
    url_func_3 = base_url + "get-route-by-route-id"
    url_func_4 = base_url + "get-train-type-by-train-type-id"
    url_func_5 = base_url + "get-price-by-route-id-and-train-type"
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
    
    trainTypeId = params["trainTypeId"]
    arguments = {"trainTypeId":trainTypeId}
    start = time.time()
    future = requests.post(url_func_4, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    print(future.text)
    jsonText_1 = json.loads(future.text)
    trainType = jsonText_1["Result"]

    if (trainType == "None"):
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

    trainTypeStr = trainType
    arguments = {"trainType":trainTypeStr, "rId":routeId, "seatClass":seatClass}
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
    indexStart = routeResult.stations.index(startId)
    print(f"indexStart: {indexStart}")
    indexEnd = routeResult.stations.index(endId)
    print(f"indexEnd: {indexEnd}")
    print(f"routeResult.distances: {routeResult.distances}")

    distance = routeResult.distances[indexEnd] - routeResult.distances[indexStart]
    print(f"Distances: {distance}")
    prices = {}
    prices["basic"] = distance * basic_rate
    prices["first_class"] = distance * first_class_rate

    returnResult.prices = prices
    returnResult.percent = 1
    returnResult.trainType = trainType

    return {
        "Result": {
            "status": returnResult.status,
            "percent": returnResult.percent,
            "trainType": returnResult.trainType,
            "prices": returnResult.prices
        }
    }
