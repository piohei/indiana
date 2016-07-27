import time
import requests
import json

from tornado import web, websocket, ioloop, gen


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("views/index.html")


class Visualizaton3DHandler(web.RequestHandler):
    def get(self):
        self.render("views/visualization_3d.html")


class Visualizaton2DHandler(web.RequestHandler):
    def get(self):
        self.render("views/visualization_2d.html")


class FingerTipHandler(web.RequestHandler):
    def get(self):
        self.render("views/finger_tip.html")

class MapHandler(web.RequestHandler):
    def get(self):
        floor = [
            {'x': 0.00,  'y':  0.00},
            {'x': 12.00, 'y':  0.00},
            {'x': 12.00, 'y':  3.40},
            {'x': 14.50, 'y':  3.40},
            {'x': 14.50, 'y':  5.10},
            {'x': 21.00, 'y':  5.10},
            {'x': 21.00, 'y':  0.00},
            {'x': 33.00, 'y':  0.00},
            {'x': 33.00, 'y': 12.00},
            {'x':  0.00, 'y': 12.00},
        ]

        walls = [
            { 'start': {'x':  0.00, 'y':  0.00}, 'end': {'x': 12.00, 'y':  0.00} },
            { 'start': {'x': 12.00, 'y':  0.00}, 'end': {'x': 12.00, 'y':  3.40} },
            { 'start': {'x': 12.00, 'y':  3.40}, 'end': {'x': 14.50, 'y':  3.40} },
            { 'start': {'x': 14.50, 'y':  3.40}, 'end': {'x': 14.50, 'y':  5.10} },
            { 'start': {'x': 14.50, 'y':  5.10}, 'end': {'x': 21.00, 'y':  5.10} },
            { 'start': {'x': 21.00, 'y':  5.10}, 'end': {'x': 21.00, 'y':  0.00} },
            { 'start': {'x': 21.00, 'y':  0.00}, 'end': {'x': 33.00, 'y':  0.00} },
            { 'start': {'x': 33.00, 'y':  0.00}, 'end': {'x': 33.00, 'y': 12.00} },
            { 'start': {'x': 33.00, 'y': 12.00}, 'end': {'x':  0.00, 'y': 12.00} },
            { 'start': {'x':  0.00, 'y': 12.00}, 'end': {'x':  0.00, 'y':  0.00} },

            { 'start': {'x':  0.00, 'y':  4.80}, 'end': {'x':  4.70, 'y':  4.80} },
            { 'start': {'x':  4.70, 'y':  4.80}, 'end': {'x':  4.70, 'y':  7.30} },
            { 'start': {'x':  4.70, 'y':  7.30}, 'end': {'x':  0.00, 'y':  7.30} },

            { 'start': {'x':  5.80, 'y':  4.80}, 'end': {'x':  6.70, 'y':  4.80} },
            { 'start': {'x':  6.70, 'y':  4.80}, 'end': {'x':  6.70, 'y':  7.30} },
            { 'start': {'x':  6.70, 'y':  7.30}, 'end': {'x':  5.80, 'y':  7.30} },

            { 'start': {'x':  6.00, 'y': 12.00}, 'end': {'x':  6.00, 'y':  8.50} },

            { 'start': {'x':  9.50, 'y':  1.70}, 'end': {'x': 12.00, 'y':  1.70} },
            { 'start': {'x':  9.50, 'y':  3.40}, 'end': {'x': 12.00, 'y':  3.40} },
            { 'start': {'x':  9.50, 'y':  1.00}, 'end': {'x':  9.50, 'y':  5.10} },
            { 'start': {'x':  9.50, 'y':  5.10}, 'end': {'x': 12.30, 'y':  5.10} },
            { 'start': {'x': 11.90, 'y':  3.40}, 'end': {'x': 11.90, 'y':  5.10} },
            { 'start': {'x': 12.30, 'y':  3.40}, 'end': {'x': 12.30, 'y':  5.10} },

            { 'start': {'x': 11.80, 'y': 12.00}, 'end': {'x': 11.80, 'y':  6.90} },
            { 'start': {'x': 10.60, 'y':  6.90}, 'end': {'x': 12.30, 'y':  6.90} },
            { 'start': {'x': 10.60, 'y':  6.90}, 'end': {'x': 10.60, 'y':  7.90} },
            { 'start': {'x': 10.60, 'y':  7.90}, 'end': {'x': 11.80, 'y':  7.90} },

            { 'start': {'x': 16.70, 'y': 12.00}, 'end': {'x': 16.70, 'y':  6.90} },
            { 'start': {'x': 18.30, 'y': 12.00}, 'end': {'x': 18.30, 'y':  6.90} },
            { 'start': {'x': 21.00, 'y': 12.00}, 'end': {'x': 21.00, 'y':  6.90} },
            { 'start': {'x': 24.00, 'y': 12.00}, 'end': {'x': 24.00, 'y':  6.90} },
            { 'start': {'x': 26.90, 'y': 12.00}, 'end': {'x': 26.90, 'y':  6.90} },
            { 'start': {'x': 18.30, 'y':  6.90}, 'end': {'x': 21.00, 'y':  6.90} },
            { 'start': {'x': 24.00, 'y':  6.90}, 'end': {'x': 26.90, 'y':  6.90} },
            { 'start': {'x': 16.70, 'y':  7.50}, 'end': {'x': 18.30, 'y':  7.50} },
            { 'start': {'x': 22.70, 'y': 12.00}, 'end': {'x': 22.70, 'y':  9.20} },
            { 'start': {'x': 21.00, 'y': 10.50}, 'end': {'x': 22.70, 'y': 10.50} },
            { 'start': {'x': 21.00, 'y':  9.20}, 'end': {'x': 22.70, 'y':  9.20} },
            { 'start': {'x': 21.00, 'y':  7.80}, 'end': {'x': 24.00, 'y':  7.80} },
            { 'start': {'x': 21.00, 'y':  6.90}, 'end': {'x': 22.20, 'y':  6.90} },
            { 'start': {'x': 22.20, 'y':  6.90}, 'end': {'x': 22.20, 'y':  7.80} },

            { 'start': {'x': 24.00, 'y':  0.00}, 'end': {'x': 24.00, 'y':  5.10} },
            { 'start': {'x': 24.00, 'y':  5.10}, 'end': {'x': 33.00, 'y':  5.10} },

            { 'start': {'x': 21.00, 'y':  1.80}, 'end': {'x': 24.00, 'y':  1.80} },
            { 'start': {'x': 22.60, 'y':  0.00}, 'end': {'x': 22.60, 'y':  1.80} },
            { 'start': {'x': 21.00, 'y':  3.00}, 'end': {'x': 22.80, 'y':  3.00} },
            { 'start': {'x': 21.00, 'y':  5.10}, 'end': {'x': 22.20, 'y':  5.10} },
            { 'start': {'x': 22.20, 'y':  5.10}, 'end': {'x': 22.20, 'y':  3.00} },
            { 'start': {'x': 22.20, 'y':  4.20}, 'end': {'x': 24.00, 'y':  4.20} },

            { 'start': {'x': 32.00, 'y':  8.00}, 'end': {'x': 33.00, 'y':  8.00} },
            { 'start': {'x': 32.00, 'y':  8.00}, 'end': {'x': 32.00, 'y':  5.10} },
            { 'start': {'x': 28.30, 'y':  7.50}, 'end': {'x': 32.00, 'y':  7.50} },
            { 'start': {'x': 28.30, 'y':  7.50}, 'end': {'x': 28.30, 'y':  6.40} },
        ]

        routers = [
            {'x':  0.30, 'y':  0.30},
            {'x':  9.10, 'y':  0.30},
            {'x':  4.00, 'y': 11.75},
            {'x': 10.80, 'y':  6.60},
            {'x': 12.10, 'y': 11.70},
            {'x': 20.80, 'y':  6.60},
            {'x': 26.60, 'y': 11.70},
            {'x': 32.70, 'y': 11.70},
            {'x': 32.70, 'y':  0.30},
        ]

        result = {
            'floors': {
                '1': {
                    'floor': floor,
                    'walls': walls,
                    'routers': routers
                }
            }
        }

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
        (r"/visualization_3d", Visualizaton3DHandler),
        (r"/visualization_2d", Visualizaton2DHandler),
        (r"/finger_tip", FingerTipHandler),
        (r"/static/(.*)", web.StaticFileHandler, {"path": __file__ + "/../static"}),
        (r"/map", MapHandler),
        (r"/websocket", SocketHandler)
    ])
    app.listen(8888)
    ioloop.IOLoop.instance().start()
