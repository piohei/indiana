# -*- coding: utf-8 -*-

from threading import RLock
from tornado import web, ioloop

from config.config import env

import fingertip.handlers as handlers
import fingertip.services as services
import fingertip.jobs as jobs

from db.db import db
from db.ap_data_dao import APDataDAO
from db.sample_stamp_dao import SampleStampDAO
from db.rssi_measure_dao import RSSIMeasureDAO

from helpers.utils import mac_regexp_dashes


class App:
    def __init__(self):
        self.global_lock = RLock()

        self.ap_data_dao = APDataDAO()
        self.sample_stamp_dao = SampleStampDAO()
        self.rssi_measure_dao = RSSIMeasureDAO()

        self.sample_service = services.SampleService(self.ap_data_dao, self.sample_stamp_dao, self.global_lock)
        self.web_socket_service = services.WebSocketService(self.global_lock)

        self.app = web.Application(handlers=[
            (r"/position/" + mac_regexp_dashes(), handlers.PositionHandler, {
                    "ap_data_dao": self.ap_data_dao,
                    "sample_stamp_dao": self.sample_stamp_dao,
                    "rssi_measure_dao": self.rssi_measure_dao
                }),
            (r"/actual_location", handlers.SampleStampHandler, {
                    "sample_service": self.sample_service
                }),
            (r"/status", handlers.SocketHandler, {
                    "web_socket_service": self.web_socket_service
                }),
            (r"/", handlers.APDataHandler, {
                    "sample_service": self.sample_service
                })
        ], debug=(env == 'development'))

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
