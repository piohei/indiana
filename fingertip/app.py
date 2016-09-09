# -*- coding: utf-8 -*-

from threading import RLock
from tornado import web, ioloop

import handlers
import services
import jobs

class App:
    def __init__(self):
        self.global_lock = RLock()

        self.fingertip_service = services.FingertipService(self.global_lock)
        self.web_socket_service = services.WebSocketService(self.global_lock)

        self.app = web.Application([
            (r"/actual_location", handlers.ActualLocationHandler),
            (r"/status", handlers.SocketHandler),
            (r"/", handlers.APDataHandler)
        ])

    def get_app(self):
        return self.app

    def run(self):
        self.app.listen(8887, address="0.0.0.0")

        jobs.CleanupJob(self.fingertip_service).start()
        jobs.StatusJob(self.fingertip_service, self.web_socket_service).start()

        ioloop.IOLoop.instance().start()
