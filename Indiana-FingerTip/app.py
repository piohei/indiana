import json
import time
from threading import RLock
from wrapt import synchronized
from tornado import web, websocket, ioloop, gen
from tornado_json import schema
from tornado_json.exceptions import api_assert
from tornado_json.requesthandlers import APIHandler
from pymongo import MongoClient

global_lock = RLock()


def millis():
    return int(round(time.time() * 1000))


db = MongoClient('52.42.120.42', 27017).indiana_db
ap_data_collection = db.ap_data
fingertip_collection = db.fingertips


class Fingertip(object):
    VALIDITY_PERIOD = 300000

    def __init__(self, mac="", x=0, y=0, z=0):
        self.mac = mac
        self.location = {"x": float(x), "y": float(y), "z": float(z)}
        self.start_time = millis()
        self.end_time = None

    def to_dict(self):
        return {"mac": self.mac, "start_time": self.start_time, "end_time": self.end_time, "location": self.location}

    def is_outdated(self):
        return millis() > (self.start_time + self.VALIDITY_PERIOD)

    def is_same_fingertip(self, other):
        return other is not None and self.location == other.location and self.mac == other.mac

class FingertipService(object):
    def __init__(self):
        self.current_fingertip = None
        self.current_websockets=[]

    @synchronized(global_lock)
    def set_fingertip(self, mac="", x=0, y=0, z=0):
        new_fingertip = Fingertip(mac, x, y, z)
        api_assert(not new_fingertip.is_same_fingertip(self.current_fingertip), 400, "Same as current")
        if self.current_fingertip is not None:
            self.end_fingertip()
        self.current_fingertip = new_fingertip

    @synchronized(global_lock)
    def end_fingertip(self):
        if self.current_fingertip is not None:
            self.current_fingertip.end_time = millis()
            try:
                self.save_fingertip()
            finally:
                self.close_current_websockets(errored=True)
                self.current_fingertip = None

    @synchronized(global_lock)
    def save_fingertip(self):
        if self.current_fingertip is None:
            raise ValueError("no current fingertip")
        inserted = fingertip_collection.insert_one(self.current_fingertip.to_dict())
        if not inserted.acknowledged:
            raise ValueError("not inserted")
        self.current_fingertip.id = inserted.inserted_id

    @synchronized(global_lock)
    def close_current_websockets(self, errored=False):
        while self.current_websockets:
            wsocket = self.current_websockets.pop()
            wsocket.write_message("ending fingertip")
            wsocket.close()

    @synchronized(global_lock)
    def add_socket(self, sock):
        self.current_websockets.append(sock)

    @synchronized(global_lock)
    def end_if_outdated(self):
        if self.current_fingertip and self.current_fingertip.is_outdated():
            self.end_fingertip()


fingertip_service = FingertipService()


class ActualLocationHandler(APIHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS, DELETE')

    @schema.validate(input_schema={"type": "object"})
    def post(self):
        fingertip_service.set_fingertip(**(self.body))
        return "ok"

    def delete(self):
        fingertip_service.end_fingertip()
        self.success("ok")

    def options(self):
        self.set_status(204)
        self.finish()

class APDataHandler(APIHandler):
    @schema.validate(input_schema={"type": "object"})
    def post(self):
        fingertip = fingertip_service.current_fingertip
        api_assert(fingertip is not None and not fingertip.is_outdated(), 400, "fingertip gone or outdated")
        api_assert(self.body["data"], 400, "empty data")
        #maybe assert if contains fingertip mac
        result = ap_data_collection.insert_one(self.body)
        api_assert(result.acknowledged, 500, "error saving")
        return "ok"


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    @gen.engine
    def open(self):
        fingertip = fingertip_service.current_fingertip
        if fingertip is None:
            self.write_message("No fingertip")
            self.close()
        else:
            mac = fingertip.mac
            fingertip_service.add_socket(self)
            while not self._on_close_called:
                fingertip = fingertip_service.current_fingertip
                if fingertip is None or mac != fingertip.mac:
                    self.write_message("Fingertip ended")
                    self.close()
                else:
                    count = ap_data_collection.count({"time": {"$gt": fingertip.start_time}})
                    self.write_message("collected {}".format(count))
                    yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 10)

    @synchronized(global_lock)
    def on_close(self):
        if self in fingertip_service.current_websockets:
            fingertip_service.current_websockets.remove(self)

class CleanupJob(ioloop.PeriodicCallback):
    CALLBACK_TIME = 30000

    def __init__(self):
        super().__init__(CleanupJob.clear, self.CALLBACK_TIME)

    @staticmethod
    def clear():
        fingertip_service.end_if_outdated()


if __name__ == "__main__":
    app = web.Application([
        (r"/actual_location", ActualLocationHandler),
        (r"/status", SocketHandler),
        (r"/", APDataHandler)
    ])
    app.listen(8887)
    CleanupJob().start()
    ioloop.IOLoop.instance().start()
