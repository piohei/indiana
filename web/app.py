# -*- coding: utf-8 -*-

import os
from multiprocessing import RLock

from tornado import web, ioloop

from config import env, config
from db import AccessPointDAO, BenchmarkReportDAO, SampleStampDAO, APDataDAO, BenchmarkStampDAO, PathDAO
from db.map_dao import MapDAO
from web.handlers.api.api import API
from web.handlers.view.view import View
from web.handlers.websockets.websockets import Websockets
from web.jobs import CleanupJob, StatusJob
from web.services import SampleService, LogSocketsService, PathService


class App:
    def __init__(self):
        daos = self.init_daos()
        services = self.init_services()

        self.api = API(config, daos, services)
        self.view = View(config)
        self.websockets = Websockets(config, services)

        self.app = web.Application(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            debug=(env == 'development')
        )

        self.app.add_handlers(".*$", self.api.get_handlers(config))
        self.app.add_handlers(".*$", self.websockets.get_handlers(config))
        self.app.add_handlers(".*$", self.view.get_handlers(config))

        self.jobs = [
            CleanupJob(self.sample_service),
            StatusJob(self.sample_service, self.log_socket_service)
        ]

    def init_services(self):
        self.global_lock = RLock()
        self.sample_service = SampleService(self.ap_data_dao, self.sample_stamp_dao,
                                            self.benchmark_stamp_dao, self.global_lock)
        self.log_socket_service = LogSocketsService(self.global_lock)
        self.path_service = PathService(self.path_dao, self.global_lock)
        return {"sample_service": self.sample_service,
                "log_socket_service": self.log_socket_service,
                "path_sefvice": self.path_service}

    def init_daos(self):
        self.access_point_dao = AccessPointDAO()
        self.sample_stamp_dao = SampleStampDAO()
        self.benchmark_stamp_dao = BenchmarkStampDAO()
        self.benchmark_report_dao = BenchmarkReportDAO()
        self.ap_data_dao = APDataDAO()
        self.path_dao = PathDAO(self.ap_data_dao)
        self.map_dao = MapDAO()
        return {"access_point_dao": self.access_point_dao,
                "sample_stamp_dao": self.sample_stamp_dao,
                "benchmark_stamp_dao": self.benchmark_stamp_dao,
                "path_dao": self.path_dao,
                "ap_data_dao": self.ap_data_dao,
                "benchmark_report_dao": self.benchmark_report_dao,
                "map_dao": self.map_dao}

    def get_app(self):
        return self.app

    def start_jobs(self):
        for job in self.jobs:
            job.start()

    def run(self):
        self.app.listen(int(config["web"]["port"]), address="0.0.0.0")
        self.start_jobs()
        ioloop.IOLoop.instance().start()
