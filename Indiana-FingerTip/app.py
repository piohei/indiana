from flask import Flask, request, jsonify
import requests
from domain import Location, APData

app = Flask("Indiana-FingerTip")


def get_location(MAC):
    url = 'http://localhost:8886/location/' + MAC
    response = requests.get(url)
    if response.status_code == 200:
        res_data_json = response.json()
        return Location(res_data_json['x'], res_data_json['y'], res_data_json['z'])
    else:
        return None


@app.route('/', methods=['POST'])
def post_location():
    #json {MAC:mac, x:x, y:y, z:z} w responsie błąd obliczeń silnika: {engineError: odlegloscOdPunktuWgEngina, engineLocation:{x:x, y:y, z:z}}
    MAC = request.json['MAC']
    real_location = Location(dictionary=request.json)
    location_from_engine = get_location(MAC)
    return jsonify(engineError=real_location.distance_from(location_from_engine), engineLocation=location_from_engine.to_dict())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8887)
