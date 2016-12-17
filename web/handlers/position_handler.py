# -*- coding: utf-8 -*-
from tornado import gen, websocket

from messaging import AsynchronousSubscriber

class PositionHandler(websocket.WebSocketHandler):

    @gen.engine
    def open(self):
        print("Starting websocket")
        self.sub = AsynchronousSubscriber("positions", callback=self.send_position)
        self.sub.start()

    def send_position(self, data):
        message = "{}:{}:{}:{}".format(data["mac"].replace(":", "_"), data["location"]['x'], data["location"]['y'], 0)
        print(message)
        self.write_message(message)

    def on_message(self, message):
        pass

    def on_close(self):
        print("Stopping websocket")
        self.sub.stop()
