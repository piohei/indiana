# -*- coding: utf-8 -*-

from tornado import web, gen, ioloop, websocket
import requests
import time

class SocketHandler(websocket.WebSocketHandler):
    POSITION_REQUEST_INTERVAL = 5
    @gen.engine
    def open(self):
        while not self._on_close_called:
            response = requests.get("http://localhost:8886/location/11:12:13:14:15:16")

            if response.status_code == 200:
                location = response.json()
                self.write_message("{}:{}:{}".format(location["x"], location["y"], location["z"]))
            else:
                self.write_message("ERROR")

            yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + self.POSITION_REQUEST_INTERVAL)
