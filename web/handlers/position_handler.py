# -*- coding: utf-8 -*-
from tornado import gen, websocket, ioloop
from threading import Thread

from herald import AsynchronousSubscriber

class PositionHandler(websocket.WebSocketHandler):

    @gen.engine
    def open(self, mac):
        print("Starting websocket for {}".format(mac))
        self.mac = mac
        self.sub = AsynchronousSubscriber("positions." + mac.replace("-", "_"), callback=self.send_position)
        self.sub.start()

    def send_position(self, data):
        message = "{}:{}:{}".format(data['x'], data['y'], data['z'])
        print(message)
        self.write_message(message)

    def on_message(self, message):
        pass

    def on_close(self):
        print("Stopping websocket for {}".format(self.mac))
        self.sub.stop()
