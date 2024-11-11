import requests
import json
import time

class Seat:
    def __init__(self, _travelDate, _airplaneNumber, _startStation, _destStation, _seatType):
        self.travelDate = _travelDate
        self.airplaneNumber = _airplaneNumber
        self.startStation = _startStation
        self.destStation = _destStation
        self.seatType = _seatType

class AirplaneType:
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
    startBig = time.time()
    APIHOST = "https://192.168.49.2:31001"
    AUTH_KEY = "23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP" 
    user_pass = AUTH_KEY.split(':')
    base_url = APIHOST + '/api/v1/namespaces/guest/actions/'
    url_func_9 = base_url + "get-route-by-trip-id"
    url_func_10 = base_url + "get-sold-tickets"
    url_func_11 = base_url + "get-airplane-type-by-trip-id"
    url_func_12 = base_url + "query-config-entity-by-config-name"
    authentication = (user_pass[0], user_pass[1])
    parameters = {'blocking': 'true', 'result': 'true'}

    numOfLeftTickets = 0
    tripId = params["tripId"]
    seatClass = params["seatClass"]
    arguments = {'tripId':tripId}
    start = time.time()
    future = requests.post(url_func_9, params=parameters, auth=authentication, json=arguments, verify=False)
    print("invoked get-route-by-tripid")
    end = time.time()
    print(end - start)
    jsonText_1 = json.loads(future.text)
    dictText_1 = json.loads(jsonText_1["Result"])
    routeResult = Route(dictText_1["id"],dictText_1["stations"],dictText_1["distances"],dictText_1["startStation"],dictText_1["destStation"])

    date = params["date"]
    arguments = {'tripId':tripId, 'date':date}
    start = time.time()
    future = requests.post(url_func_10, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    jsonText_2 = json.loads(future.text)
    list_Tickets = jsonText_2["Result"]
    soldTickets = []
    for ticketStr in list_Tickets:
        ticket = json.loads(ticketStr)
        soldTickets.append(Ticket(ticket["seatNo"],ticket["startStation"],ticket["destStation"]))
    leftTicketInfo = LeftTicketInfo(soldTickets)

    arguments = {'tripId':tripId}
    start = time.time()
    future = requests.post(url_func_11, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    jsonText_3 = json.loads(future.text)
    dictText_3 = json.loads(jsonText_3["Result"])
    airplaneTypeResult = AirplaneType(dictText_3["id"],dictText_3["economyClass"],dictText_3["confortClass"],dictText_3["avgSpeed"])

    seatTotalNum = 0
    if seatClass == "FIRST":
        seatTotalNum = airplaneTypeResult.confortClass
    else:
        seatTotalNum = airplaneTypeResult.economyClass
    
    stationList = []
    stationList = routeResult.stations

    soldTicketSize = 0
    if leftTicketInfo is not None:
        startStation = params["startStation"]
        soldTickets = []
        soldTickets = leftTicketInfo.soldTickets
        soldTicketSize = len(soldTickets)
        for soldTicket in soldTickets:
            soldTicketDestStation = soldTicket.destStation
            try:
                if (stationList.index(soldTicketDestStation) < stationList.index(startStation)):
                    numOfLeftTickets += 1
            except Exception as e:
                print(e)
    
    arguments = {'tripId':tripId}
    start = time.time()
    future = requests.post(url_func_12, params=parameters, auth=authentication, json=arguments, verify=False)
    end = time.time()
    print(end - start)
    jsonText_4 = json.loads(future.text)
    direstPart = float((jsonText_4["Result"]))

    if (routeResult.stations[0] == params["startStation"] and routeResult.stations[len(routeResult.stations()) - 1] == params["destStation"]):
        direstPart = direstPart
    else:
        direstPart = 1.0 - direstPart
    unusedNum = (int) (seatTotalNum * direstPart) - soldTicketSize
    numOfLeftTickets += unusedNum
    endBig = time.time()
    print("Overall time = ", endBig - startBig)
    return {"Result": "Good!"}
