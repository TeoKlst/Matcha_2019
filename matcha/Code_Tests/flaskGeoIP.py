import requests
from flask import Flask, request
from flask import Flask, json, jsonify
import json, socket

key = 'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&ipAddress=8.8.8.8'

app = Flask(__name__)

@app.route('/', methods=["GET"])
def get_data():
    key = 'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&ipAddress=8.8.8.8'
    http    = 'https://ip-geolocation.whoisxmlapi.com/api/v1?'
    key     = 'apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&'
    json_request = requests.get('https://api.ipify.org?format=json').json()
    ip      = json_request['ip']
    ipAdress= 'ipAddress=' + ip
    json_request = requests.get(http + key + ipAdress).json()
    data  = (json_request)
    print (data['location']['country'])
    print (data['location']['city'])
    print (data['location']['lat'])
    print (data['location']['lng'])

    # --- DOESN'T WORK ---
    # ip_address = request.remote_addr
    # ip_address2= jsonify({'ip': request.remote_addr}), 200
    # ip_address3= request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # ip_address4= request.headers.get('X-Forwarded-For', request.remote_addr)
    # return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #return jsonify({'ip': request.remote_addr}), 200
    #return jsonify({'ip': request.environ['REMOTE_ADDR']}), 200
    # print("Requester IP1: ", ip_address)
    # print("Requester IP2: ", ip_address2)
    # print("Requester IP3: ", ip_address3)
    # print("Requester IP4: ", test)

    # --- WORKS ---
    # hostname = socket.gethostname()
    # ## getting the IP address using socket.gethostbyname() method
    # ip_address = socket.gethostbyname(hostname)
    # ## printing the hostname and ip_address
    # print(f"Hostname: {hostname}")
    # print(f"IP Address: {ip_address}")
    return (data)

if __name__ == '__main__':
    app.run(debug=True)
