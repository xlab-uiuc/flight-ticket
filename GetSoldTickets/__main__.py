import redis
import ast
import json
import random
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

def fake_main(params):
    stations = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
    print("Stations ok")
    randNum = random.randint(50, 200)
    print("Number of tickets ", randNum)
    tickets = []
    for index in range (0, randNum):
        startIndex = random.randint(0,9)
        endIndex = random.randint(startIndex+1, 10)
        ticket = Ticket(index,stations[startIndex],stations[endIndex])
        tickets.append(ticket)
    #leftTicketInfo = LeftTicketInfo(tickets)
    #print(tickets)
    #print("Send result back")
    ticketsInJson = []
    for index in range (0, randNum):
        ticketsInJson.append(json.dumps(tickets[index].__dict__))
    print(ticketsInJson)
    time.sleep(0.1)
    return {"Result":ticketsInJson}

def main(params):
    tripId = params["tripId"]
    myclient = redis.Redis(host="host.minikube.internal",port="6379",db=1)
    allSoldTicketsBytes = myclient.hget("soldTickets",tripId)
    allSoldTicketsStr = allSoldTicketsBytes.decode("utf-8")
    allSoldTickets = ast.literal_eval(allSoldTicketsStr)
    ticketsInJson = []
    for ticket in allSoldTickets:
        if ticket["date"] == params["date"]:
            ticketObj = Ticket(ticket["seatNo"],ticket["startStation"],ticket["destStation"])
            ticketsInJson.append(json.dumps(ticketObj.__dict__))
    return {"Result":ticketsInJson}
