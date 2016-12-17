# -*- coding: utf-8 -*-

from tornado import websocket


class SocketHandler(websocket.WebSocketHandler):
    def initialize(self, web_socket_service):
        self.web_socket_service = web_socket_service

    def check_origin(self, origin):
        return True

    def open(self):
        self.web_socket_service.add_socket(self)
        self.write_message('subscribed')

    def on_close(self):
        self.web_socket_service.remove_socket(self)
