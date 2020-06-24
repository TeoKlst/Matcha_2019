from flask import Flask, jsonify
from flask_simple_geoip import SimpleGeoIP

key = 'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_FsPa7wR7Y78vT9riB4HeMjpAWhD3N&ipAddress=8.8.8.8'

app = Flask(__name__)

# Initialize the extension
simple_geoip = SimpleGeoIP(app)


@app.route('/')
def test():
    # Retrieve geoip data for the given requester
    geoip_data = simple_geoip.get_geoip_data()

    return jsonify(data=geoip_data)