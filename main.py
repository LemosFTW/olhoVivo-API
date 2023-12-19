from os import name
import requests
import http.client
import json

TOKEN = "5c654a4d150687f6235ec633060051b2386afd2d10060f8e7c68e9138e3fc7f1"
URL = "http://api.olhovivo.sptrans.com.br/v2.1/"
PATHROUTE = "/Linha/Buscar?termosBusca="
PATHROUTEDIRECTION = (
    "/Linha/BuscarLinhaSentido?termosBusca={codigoLinha}&sentido={sentido}"
)
PATHSTOP = "/Parada/Buscar?termosBusca={termosBusca}"
PATHSTOPROUTE = "/Parada/BuscarParadasPorLinha?codigoLinha="
PATHSTOPRACER = "/Parada/BuscarParadasPorCorredor?codigoCorredor="
PATHRACER = "/Corredor"
PATHCOMPANIES = "/Empresa"
PATHPOSITION = "/Posicao"
PATHPOSITIONROUTE = "/Posicao/Linha?codigoLinha="
PATHPOSITIONRACER = "/Posicao/Corredor?codigoCorredor="
PATHARRIVAL = "/Previsao?codigoParada={codigoParada}&codigoLinha={codigoLinha}"




session = requests.Session()

#TODO: implementar o uso de https
#conn = http.client.HTTPSConnection(URL)
#conn.request("GET", "")







class Route:
    def __init__(self, id, circular, sign1, sign2, direction, signString1, signString2):
        self.id = id
        self.circular = circular
        self.sign1 = sign1
        self.sign2 = sign2
        self.direction = direction
        self.signString1 = signString1
        self.signString2 = signString2

    def __str__(self):
        return (
            "Route: "
            + str(self.id)
            + "\nCircular: "
            + str(self.circular)
            + "\nSign1: "
            + str(self.sign1)
            + "\nSign2: "
            + str(self.sign2)
            + "\nDirection: "
            + str(self.direction)
            + "\nSignString1: "
            + str(self.signString1)
            + "\nSignString2: "
            + str(self.signString2)
        )
    





class Stop:
    def __init__(self, id, name, address, latitude, longitude):
        self.id = id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return (
            "Stop: "
            + str(self.id)
            + "\nName: "
            + str(self.name)
            + "\nAddress: "
            + str(self.address)
            + "\nLatitude: "
            + str(self.latitude)
            + "\nLongitude: "
            + str(self.longitude)
        )
    






class Racer:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "Racer: " + str(self.id) + "\nName: " + str(self.name)









def main():
    auth()
    inputText = ""
    while inputText != "exit":
        inputText = input("Ask for information...\n")
        getCommand(inputText)

    pass








def auth():
    print("Authenticating...")
    response = session.post(URL + "Login/Autenticar?token=" + TOKEN)
    if bool(response.text):
        print("Authenticated!")

    pass












def getCommand(inputText):
    match str(inputText).lower():



        case "route":
            print()
            routeNum = input("Witch bus route?\n")
            print()
            searchByDirection = input("Do you want to search by direction? (y/n)\n")
            print()

            if searchByDirection == "y":
                direction = input("Witch direction? (1/2)\n")
                print()
                getRoute(routeNum, direction)

            elif searchByDirection == "n":
                getRoute(routeNum, None)

            else:
                print("Invalid input")
                print()
            return
        




        case "stops":
            inputText = input("Search by:  (stopName/routeNumber/racer)\n")

            match str(inputText).lower():
                case "stopname":
                    inputName = input("Witch stop?\n")
                    getStop("stopName", inputName)

                    return
                case "routenumber":
                    inputNumber = input("Witch route?\n")
                    getStop("routeNumber", inputNumber)
                    return
                case "racer":
                    inputRacer = input("Witch racer?\n")
                    getStop("racer", inputRacer)
                    print(inputRacer)

                    return
                case _:
                    print("Invalid input")
                    print()
                    return

        




        case "racer":
            getRacers()
            return
        



        case "companies":

            return
        case "positon":
            print("positon")
            return
        case "arrival":
            print("arrival")
            return
        case "speed":
            print("speed")
            return
        case _:
            print()
            print("Invalid input")
            print()

    return











def iterateRouteJSON(json,type):
    jsonSet = []


    match str(type):
        case "racer":
            for item in json:
                # identifier of the racer
                id = item["cc"]
                # name of the racer
                name = item["nc"]

                racer = Racer(id, name)
                print(racer.__str__())
                print()
                jsonSet.append(racer)


        case "route":
            for item in json:

                # identifier of the route
                id = item["cl"]

                # indicates if the route is circular or not (if is circular, doesnt have a secondary terminal)
                circular = item["lc"]

                # indicates the first part of the bus sign
                sign1 = item["lt"]

                # indicates the second part of the route BASE (10), ATENDIMENTO (21, 23, 32, 41)
                sign2 = item["tl"]

                # indicates the direction, if is 1 means that is starting from the main terminal to the secondary terminal, if is 2 means that is starting from the secondary terminal to the main terminal
                direction = item["sl"]

                # indicates the descriptive sign of the route in the direction of main terminal to secondary terminal
                signString1 = item["tp"]

                # indicates the descriptive sign of the route in the direction of Secondary Terminal to Main Terminal
                signString2 = item["ts"]

                route = Route(id, circular, sign1, sign2, direction, signString1, signString2)
                print(route.__str__())
                print()
                jsonSet.append(route)

        case "stop":
            for item in json:
                # identifier of the stop
                id = item["cp"]
                # name of the stop
                name = item["np"]
                # address of the stop
                address = item["ed"]
                # latitude of the stop
                latitude = item["py"]
                # longitude of the stop
                longitude = item["px"]

                stop = Stop(id, name, address, latitude, longitude)
                print(stop.__str__())
                print()
                jsonSet.append(stop)
                
                
            
    return jsonSet












def getStop(type, argument): 

    match str(type).lower():
        case "stopname":
            response = session.get(URL + PATHSTOP.format(termosBusca=argument))
            jsonObject = json.loads(response.text)
            stopSet = iterateRouteJSON(jsonObject, "stop")

            return
        case "routenumber":

            response = session.get(URL + PATHSTOPROUTE + argument)
            jsonObject = json.loads(response.text)
            stopSet = iterateRouteJSON(jsonObject, "stop")
            return
        case "racer":
            response = session.get(URL + PATHSTOPRACER + argument)
            jsonObject = json.loads(response.text)
            stopSet = iterateRouteJSON(jsonObject, "stop")
            
            return







def getRacers():
    response = session.get(URL + PATHRACER)
    jsonObject = json.loads(response.text)
    racerSet = iterateRouteJSON(jsonObject, "racer")

    return racerSet






def getRoute(routeNum, direction):
    if direction == None:
        response = session.get(URL + PATHROUTE + routeNum)
    else:
        response = session.get(URL + PATHROUTEDIRECTION.format(codigoLinha=routeNum, sentido=direction))

    jsonObject = json.loads(response.text)
    routeSet = iterateRouteJSON(jsonObject, "route")

    return routeSet







if __name__ == "__main__":
    main()
