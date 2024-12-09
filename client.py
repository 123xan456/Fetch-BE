import requests
from datetime import datetime, timezone

port = 8000
host = "localhost"
baseurl = "http://" + host + ":" + str(port)

def prompt():
    try:
        print()
        print(">> Enter a command:")
        print("   0 => end")
        print("   1 => add")
        print("   2 => spend")
        print("   3 => balance")
        print("   4 => clear")
        cmd = int(input())
        return cmd

    except Exception as e:
        print("ERROR")
        print("ERROR: invalid input")
        print("ERROR")
        return -1
    
    
def add(baseurl):
    url = baseurl + "/add"
    
    print("Enter payer name:")
    payer = input().strip()

    print("Enter amount to add:")
    points = int(input().strip())
    
    time = datetime.now(timezone.utc)
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    data = {
        "payer":payer,
        "points": points,
        "timestamp": timestamp
    }
    
    response = requests.post(url, json = data)
    print(f"Response received with status {response.status_code}")
    
    if response.status_code == 400:
        body = response.json()
        print(f"Error: {body['error']}")

    
def spend(baseurl):
    url = baseurl + "/spend"
    
    print("Points to spend:")
    points = int(input().strip())
    
    data = {"points": points}
    response = requests.post(url, json = data)

    print(f"Response received with status {response.status_code}")  
    if response.status_code == 400:
        body = response.json()
        print(f"Error: {body['error']}")
    elif response.status_code == 200: 
        body = response.json()
        for record in body:
            print(f"Payer: {record['payer']}, Points: {record['points']}")
    

def balance(baseurl):
    url = baseurl + "/balance"
    response = requests.get(url)
    print(f"Response received with status {response.status_code}")
    
    if response.status_code == 400:
        body = response.json()
        print(f"Error: {body['error']}")
    elif response.status_code == 200:
        body = response.json()
        for key, val in body.items():
            print(f"Payer: {key}, Points: {val}")

def clear(baseurl):
    url = baseurl + "/clear"
    response = requests.get(url)
    print(f"Response received with status {response.status_code}")
    
    if response.status_code == 400:
        body = response.json()
        print(f"Error: {body['error']}")
    elif response.status_code == 200:
        print("Successfully cleared all transactions from record")
        

cmd = prompt()

while cmd != 0:
    if cmd == 1:
        add(baseurl)
    elif cmd == 2:
        spend(baseurl)
    elif cmd == 3:
        balance(baseurl)
    elif cmd == 4:
        clear(baseurl)
    else:
        print("Unknown command.")
        
    cmd = prompt()

    