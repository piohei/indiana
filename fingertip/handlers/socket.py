# -*- coding: utf-8 -*-

from wrapt import synchronized
from tornado import websocket, gen

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    @gen.engine
    def open(self):
        web_socket_service.add_socket(self)
        self.write_message('subscribed')

    def on_close(self):
        web_socket_service.remove_socket(self)
