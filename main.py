import requests
import json

TOKEN = "5c654a4d150687f6235ec633060051b2386afd2d10060f8e7c68e9138e3fc7f1"
URL = "http://api.olhovivo.sptrans.com.br/v2.1/"
PATH = "/Linha/Buscar?termosBusca="

session = requests.Session()

def main():
    auth()
    inputText = ""
    while inputText != "exit":
        inputText = input("Ask for information...\n")
        response = getCommand(inputText)
        print(response.text)
        
        
    pass


def auth():
    print("Authenticating...")
    response = session.post(URL + "Login/Autenticar?token=" + TOKEN)
    if bool(response.text):
        print("Authenticated!")
    




    pass

def getCommand(inputText):
    return session.get(URL + PATH + inputText)
    
    

if __name__ == "__main__":
    main()