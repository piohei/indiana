from flask import Flask, request, json
import requests

app = Flask("Indiana-FingerTip")


class Location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def __str__(self, *args, **kwargs):
        return str(self.x) + ';' + self.y + ';' + self.z


def get_location(MAC):
    url = 'http://localhost:5050/location/' + MAC
    response = requests.get(url)
    if response.status_code == 200:
        res_data_json = response.json()['json']
        return Location(res_data_json['x'], res_data_json['y'], res_data_json['z'])
    else:
        return None


@app.route('/', methods=['POST'])
def post_location():
    #json {MAC:mac, x:x, y:y, z:z} w responsie błąd obliczeń silnika: {engineError: odlegloscOdPunktuWgEngina, engineLocation:{x:x, y:y, z:z}}
    MAC = request.json['MAC']
    real_location = Location(request.json['x'], request.json['y'], request.json['z'])
    location_from_engine = get_location(MAC)
    print(json.dumps(request.json))
    return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8887)
