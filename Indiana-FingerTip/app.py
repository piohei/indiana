from threading import RLock

from tornado import web, websocket, ioloop, gen
from tornado_json import schema
from tornado_json.exceptions import api_assert, APIError
from tornado_json.requesthandlers import APIHandler
from wrapt import synchronized

import db
from db import DbException
from services import *
import jobs

global_lock = RLock()

web_socket_service = WebSocketService()
fingertip_service = FingertipService(db, global_lock)


class ActualLocationHandler(APIHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS, DELETE')

    @schema.validate(input_schema={"type": "object"})
    def post(self):
        try:
            fingertip_service.set_fingertip(**(self.body))
        except FingertipException as e:
            raise APIError(400, e.message)
        return "ok"

    @synchronized(global_lock)
    def delete(self):
        try:
            fingertip_service.end_fingertip()
        except FingertipException as e:
            raise APIError(400, e.message)
        except DbException as e:
            raise APIError(500, e.message)
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
        # maybe assert if contains fingertip mac
        try:
            db.save_ap_data(self.body)
        except DbException as e:
            raise APIError(500, e.message)
        return "ok"


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    @gen.engine
    def open(self):
        web_socket_service.add_socket(self)
        self.write_message("subscribed")

    @synchronized(global_lock)
    def on_close(self):
        web_socket_service.remove_socket(self)


if __name__ == "__main__":
    app = web.Application([
        (r"/actual_location", ActualLocationHandler),
        (r"/status", SocketHandler),
        (r"/", APDataHandler)
    ])
    app.listen(8887, address="0.0.0.0")
    jobs.CleanupJob(fingertip_service).start()
    jobs.StatusJob(fingertip_service, web_socket_service).start()
    ioloop.IOLoop.instance().start()
