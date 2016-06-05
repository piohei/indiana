import time
import requests
import json

from tornado import web, websocket, ioloop, gen


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("static/index.html")


class FingerTipHandler(web.RequestHandler):
    def get(self):
        self.render("static/finger_tip.html")

    def post(self):
        mac = self.get_argument('mac', '')
        x = self.get_argument('x', '')
        y = self.get_argument('y', '')
        z = self.get_argument('z', '')

        requests.post("http://localhost:8887/", json={
                "MAC": mac,
                "x": x,
                "y": y,
                "z": z,
            })

        self.redirect("/finger_tip")


class MapHandler(web.RequestHandler):
    def get(self):
        rooms = [
            { 'left_bottom': {'x': 10, 'y':  10}, 'right_up': {'x': 30, 'y': 35} },
            { 'left_bottom': {'x': 10, 'y': -40}, 'right_up': {'x': 50, 'y': 10} }
        ]

        routers = [
            {'x': 10, 'y': 10},
            {'x': 30, 'y': 35},
            {'x': 50, 'y': -40},
        ]

        result = {'rooms': rooms, 'routers': routers}
        self.write(json.dumps(result))


class SocketHandler(websocket.WebSocketHandler):
    @gen.engine
    def open(self):
        while not self._on_close_called:
            response = requests.get("http://localhost:8886/location/11:12:13:14:15:16")

            if response.status_code == 200:
                location = response.json()
                self.write_message("{}:{}:{}".format(location["x"], location["y"], location["z"]))
            else:
                self.write_message("ERROR")

            yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 1)


if __name__ == "__main__":
    app = web.Application([
        (r"/", IndexHandler),
        (r"/map", MapHandler),
        (r"/finger_tip", FingerTipHandler),
        (r"/static/(.*)", web.StaticFileHandler, {"path": __file__ + "/../static"}),
        (r"/websocket", SocketHandler)
    ])
    app.listen(8888)
    ioloop.IOLoop.instance().start()
