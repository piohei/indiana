import collections
import threading

from flask import Flask, request, jsonify

from domain import Location, APData

app = Flask("Indiana-DatastoreMock")

fingertips = {}
locations = {}

lock = threading.Lock()
ap_data_store = collections.defaultdict(dict)


@app.route('/location/<MAC>', methods=['GET'])
def get_location(MAC):
    print(locations)
    coordinates = locations.get(MAC)
    if coordinates is not None:
        return jsonify(coordinates.to_dict())
    else:
        res = jsonify(message='NotFound')
        res.status_code = 404
        return res


@app.route('/location/', methods=['GET'])
def get_all_locations():
    locations_dict = dict((mac, location.to_dict()) for mac, location in locations.items())
    return jsonify(locations_dict)


@app.route('/location/<MAC>', methods=['POST']) #w body json z propertiesami x y z
def post_location(MAC):
    locations[MAC] = Location(dictionary=request.json)
    return jsonify(message="ok")


@app.route('/fingertip/', methods=['POST'])
def post_fingertip():
    fingertip_json = request.json
    location = Location(dictionary=fingertip_json['location'])
    metrics = fingertip_json['metrics']
    fingertips[str(location)] = metrics
    return jsonify(message="ok")

@app.route('/ap_data', methods=['POST'])
def post_ap_data():
    ap_data = APData(dictionary=request.json)
    with lock:
        device_ap_data = ap_data_store[ap_data.device_MAC]
        previous_ap_data = device_ap_data.get(ap_data.router_MAC)
        if previous_ap_data is None or previous_ap_data.timestamp <= ap_data.timestamp:
            device_ap_data[ap_data.router_MAC] = ap_data
            ap_data_store[ap_data.device_MAC] = device_ap_data
    return jsonify(message="ok")

@app.route('/ap_data/<MAC>', methods=['GET'])
def get_ap_data(MAC):
    device_ap_data = ap_data_store.get(MAC)
    if device_ap_data:
        dictionarised = dict((ap, data.to_dict()) for ap, data in device_ap_data.items())
        return jsonify(dictionarised)
    else:
        res = jsonify(message='notFound')
        res.status_code = 404
        return res

@app.route('/ap_data', methods=['GET'])
def get_all_ap_data():
    dictionarised = {}
    with lock:
        for device in ap_data_store:
            dictionarised[device] = dict((ap, data.to_dict()) for ap, data in ap_data_store[device].items())
    return jsonify(dictionarised)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8886)
