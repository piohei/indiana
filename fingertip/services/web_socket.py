# -*- coding: utf-8 -*-

from threading import RLock
from tornado.websocket import WebSocketClosedError


class WebSocketService(object):
    def __init__(self, lock=RLock()):
        self.list = []
        self.lock = lock

    def add_socket(self, web_socket):
        with self.lock:
            self.list.append(web_socket)

    def remove_socket(self, web_socket, message=''):
        with self.lock:
            try:
                self.list.remove(web_socket)
                web_socket.write_message(message)
            except WebSocketClosedError:
                pass
            finally:
                web_socket.close()

    def close_current_sockets(self, message='closed'):
        with self.lock:
            while self.list:
                web_socket = self.list.pop()
                self.remove_socket(web_socket, message)

    def broadcast(self, message):
        with self.lock:
            for ws in self.list:
                ws.write_message(message)
