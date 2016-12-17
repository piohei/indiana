# -*- coding: utf-8 -*-

from threading import RLock

from tornado import web, ioloop

from config import env, config
from db import APDataDAO, PathDAO, SampleStampDAO
from db.benchmark_stamp_dao import BenchmarkStampDAO
from .handlers import *
from .jobs import *
from .services import *


class App:
    def __init__(self):
        self.global_lock = RLock()

        self.ap_data_dao = APDataDAO()
        self.sample_stamp_dao = SampleStampDAO()
        self.benchmark_stamp_dao = BenchmarkStampDAO()
        self.path_dao = PathDAO(self.ap_data_dao)

        self.sample_service = SampleService(self.ap_data_dao, self.sample_stamp_dao,
                                            self.benchmark_stamp_dao, self.global_lock)
        self.web_socket_service = WebSocketService(self.global_lock)
        self.path_service = PathService(self.path_dao, self.global_lock)

        self.app = web.Application(handlers=[
            (config["fingertip"]["endpoints"]["sample_stamp"], SampleStampHandler, {
                    "sample_service": self.sample_service
                }),
            (config["fingertip"]["endpoints"]["benchmark_stamp"], BenchmarkStampHandler, {
                    "sample_service": self.sample_service
                }),
            (config["fingertip"]["endpoints"]["status"], SocketHandler, {
                    "web_socket_service": self.web_socket_service
                }),
            (config["fingertip"]["endpoints"]["path"], PathHandler, {
                    "path_service": self.path_service
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
        self.app.listen(int(config["fingertip"]["port"]), address="0.0.0.0")
        self.start_jobs()
        ioloop.IOLoop.instance().start()
