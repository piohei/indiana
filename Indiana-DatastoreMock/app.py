from flask import Flask, request, json, jsonify

app = Flask("Indiana-DatastoreMock")

fingertips = {}
locations = {}

class Location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}


@app.route('/location/<MAC>', methods=['GET'])
def get_location(MAC):
    print(locations)
    coordinates = locations.get(MAC)
    if coordinates is not None:
        return jsonify(coordinates)
    else:
        res = jsonify(message='NotFound')
        res.status_code = 404
        return res


@app.route('/location/', methods=['GET'])
def get_all_locations():
    return jsonify(locations)


@app.route('/location/<MAC>', methods=['POST']) #w body json z propertiesami x y z
def post_location(MAC):
    locations[MAC] = Location(request.json['x'], request.json['y'], request.json['z']).to_dict()
    return jsonify(message='ok')


if __name__ == "__main__":
    app.run()