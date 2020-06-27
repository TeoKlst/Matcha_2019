import requests
from flask import Flask
from flask import Flask, json, jsonify
import json

key = 'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&ipAddress=8.8.8.8'

app = Flask(__name__)

@app.route('/')
def get_data():
    key = 'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&ipAddress=8.8.8.8'
    http    = 'https://ip-geolocation.whoisxmlapi.com/api/v1?'
    key     = 'apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&'
    ip      = '105.232.99.12'
    ipAdress= 'ipAddress=' + ip
    # return requests.get('https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&ipAddress=105.232.99.12').json()
    json_request = requests.get(http + key + ipAdress).json()
    data  = (json_request)
    print (data['location']['city'])
    return requests.get(http + key + ipAdress).json()

# @app.route("/get_my_ip", methods=["GET"])
# def get_my_ip():
#     return jsonify({'ip': requests.remote_addr}), 200

# @app.route("/")
# def proxy_example():
#     r = requests.get("https://ip-geolocation.whoisxmlapi.com/api")
#     Response = []
#     return Response(
#         r.text,
#         status=r.status_code,
#         content_type=r.headers['content-type'],
#     )


# @app.route('/')
# def index():
#     url = 'https://ip-geolocation.whoisxmlapi.com/api'
#     r = requests.get(url)
#     j = json.loads(r.text)
#     # city = j['city']
#     print('TEST')
#     # print(city)

if __name__ == '__main__':
    app.run(debug=True)
