# -*- coding: utf-8 -*-

from threading import RLock

from tornado import web, ioloop

from config import env
from db import APDataDAO, PathDAO
from db.benchmark_stamp_dao import BenchmarkStampDAO
from .handlers import *
from .jobs import *
from .services import *


class App:
    def __init__(self):
        self.global_lock = RLock()

        self.ap_data_dao = APDataDAO()
        # self.sample_stamp_dao = SampleStampDAO()
        self.sample_stamp_dao = BenchmarkStampDAO()
        self.path_dao = PathDAO()


        self.sample_service = SampleService(self.ap_data_dao, self.sample_stamp_dao, self.global_lock)
        self.web_socket_service = WebSocketService(self.global_lock)
        self.path_service = PathService(self.path_dao, self.global_lock)

        self.app = web.Application(handlers=[
            (r"/actual_location", SampleStampHandler, {
                    "sample_service": self.sample_service
                }),
            (r"/status", SocketHandler, {
                    "web_socket_service": self.web_socket_service
                }),
            (r"/path", PathHandler, {
                    "path_service": self.path_service
                }),
            (r"/", APDataHandler, {
                    "sample_service": self.sample_service
                })
        ], debug=(env == 'development'))

        self.jobs = [
            CleanupJob(self.sample_service),
            StatusJob(self.sample_service, self.web_socket_service)
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
