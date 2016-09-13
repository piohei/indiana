# -*- coding: utf-8 -*-

from threading import RLock
from tornado import web, ioloop

import fingertip.handlers as handlers
import fingertip.services as services
import fingertip.jobs as jobs


class App:
    def __init__(self):
        self.global_lock = RLock()

        self.fingertip_service = services.FingertipService(self.global_lock)
        self.web_socket_service = services.WebSocketService(self.global_lock)

        self.app = web.Application([
            (r"/actual_location", handlers.ActualLocationHandler, {"fingertip_service": self.fingertip_service}),
            (r"/status", handlers.SocketHandler, {"web_socket_service": self.web_socket_service}),
            (r"/", handlers.APDataHandler, {"web_socket_service": self.web_socket_service})
        ])

        self.jobs = [
            jobs.CleanupJob(self.fingertip_service),
            jobs.StatusJob(self.fingertip_service, self.web_socket_service)
        ]

    def get_app(self):
        return self.app

    def start_jobs(self):
        for job in self.jobs:
            job.start()

    def run(self):
        self.app.listen(8887, address="0.0.0.0")
        self.start_jobs()
        ioloop.IOLoop.instance().start()
