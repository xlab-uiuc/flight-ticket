import json
import time
import redis
import ast
import requests

class Seat:
    def __init__(self, _travelDate, _airplaneNumber, _startStation, _destStation, _seatType):
        self.travelDate = _travelDate
        self.airplaneNumber = _airplaneNumber
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
    print("Receive request")
    tripId = params["tripId"]
    print("Trip id = ", tripId)
    startStation = "start"
    destStation = "end"
    stations = []
    stations.append("start")
    stations.append("A")
    stations.append("B")
    stations.append("C")
    stations.append("D")
    stations.append("E")
    stations.append("F")
    stations.append("G")
    stations.append("H")
    stations.append("I")
    stations.append("J")
    stations.append("K")
    stations.append("L")
    stations.append("M")
    stations.append("N")
    stations.append("O")
    stations.append("P")
    stations.append("Q")
    stations.append("end")
    distances = []
    distances.append("100")
    distances.append("200")
    distances.append("70")
    distances.append("80")
    distances.append("60")
    print("Prepared Route object")
    routeResult = Route(1, stations, distances, startStation, destStation)
    print("Send result back")
    print(json.dumps(routeResult.__dict__))
    time.sleep(0.1)
    return {"Result":json.dumps(routeResult.__dict__)}

def main(params):
    APIHOST = "https://192.168.49.2:31001"
    AUTH_KEY = "23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP" 
    user_pass = AUTH_KEY.split(':')
    authentication = (user_pass[0], user_pass[1])
    parameters = {'blocking': 'true', 'result': 'true'}
    base_url = APIHOST + '/api/v1/namespaces/guest/actions/'
    url_func_9 = base_url + "get-route-by-route-id"
    tripId = params["tripId"]
    myclient = redis.Redis(host="host.minikube.internal",port="6379",db=1)
    rId = myclient.hget("rId",tripId).decode("utf-8")
    arguments = {'rId':rId}
    print(f"rId: {rId}")
    future = requests.post(url_func_9, params=parameters, auth=authentication, json=arguments, verify=False)
    jsonText_1 = json.loads(future.text)
    dictText_1 = json.loads(jsonText_1["Result"])
    routeResult = Route(dictText_1["id"],dictText_1["stations"],dictText_1["distances"],dictText_1["startStation"],dictText_1["destStation"])
    return {"Result":json.dumps(routeResult.__dict__)}
