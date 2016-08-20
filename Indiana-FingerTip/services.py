from threading import RLock

from domain import Fingertip
from utils import millis


class FingertipException(Exception):
    def __init__(self, message):
        self.message = message


class WebSocketService(object):
    def __init__(self, lock=RLock()):
        self.list = []
        self.lock = lock

    def add_socket(self, web_socket):
        with self.lock:
            self.list.append(web_socket)

    def remove_socket(self, web_socket, message=""):
        with self.lock:
            try:
                self.list.remove(web_socket)
            finally:
                web_socket.write_message(message)
                web_socket.close()

    def close_current_sockets(self, message="closed"):
        with self.lock:
            while self.list:
                web_socket = self.list.pop()
                self.remove_socket(web_socket, message)

    def broadcast(self, message):
        with self.lock:
            for ws in self.list:
                ws.write_message(message)


class FingertipService(object):
    def __init__(self, db, lock=RLock()):
        self.current_fingertip = None
        self.lock = lock
        self.db = db

    def set_fingertip(self, mac="", x=0, y=0, z=0):
        with self.lock:
            new_fingertip = Fingertip(mac, x, y, z)
            if new_fingertip.is_same_fingertip(self.current_fingertip):
                raise FingertipException("same as current")
            if self.current_fingertip is not None:
                self.end_fingertip()
            self.current_fingertip = new_fingertip

    def end_fingertip(self):
        with self.lock:
            if self.current_fingertip is not None:
                self.current_fingertip.end_time = millis()
                try:
                    self.db.save_fingertip(self.current_fingertip)
                finally:
                    self.current_fingertip = None
            else:
                raise FingertipException("no current fingertip")

    def end_if_outdated(self):
        with self.lock:
            if self.current_fingertip and self.current_fingertip.is_outdated():
                self.end_fingertip()

    def get_status(self):
        with self.lock:
            if self.current_fingertip is None:
                return "no fingertip"
            count = self.db.count_ap_data_entries_since(self.current_fingertip.start_time)
            return "fingertip is: {}; collected samples {}".format(self.current_fingertip, count)


