# -*- coding: utf-8 -*-

from threading import RLock
from tornado import web, ioloop

import fingertip.handlers as handlers
import fingertip.services as services
import fingertip.jobs as jobs

import db


class App:
    def __init__(self):
        self.global_lock = RLock()

        self.ap_data_dao = db.APDataDAO()
        self.sample_stamp_dao = db.SampleStampDAO()

        self.sample_service = services.SampleService(self.ap_data_dao, self.sample_stamp_dao, self.global_lock)
        self.web_socket_service = services.WebSocketService(self.global_lock)

        self.app = web.Application([
            (r"/actual_location", handlers.SampleStampHandler, {"sample_service": self.sample_service}),
            (r"/status", handlers.SocketHandler, {"web_socket_service": self.web_socket_service}),
            (r"/", handlers.APDataHandler, {"sample_service": self.sample_service})
        ])

        self.jobs = [
            jobs.CleanupJob(self.sample_service),
            jobs.StatusJob(self.sample_service, self.web_socket_service)
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
