# -*- coding: utf-8 -*-

import os

from tornado import web, ioloop

from config import env, config
from db import AccessPointDAO, BenchmarkReportDAO, SampleStampDAO
from models import Map
from .handlers import *


class App:
    def __init__(self):
        self.access_point_dao    = AccessPointDAO()
        self.sample_stamp_dao    = SampleStampDAO()
        self.benchmark_report_dao = BenchmarkReportDAO()

        self.map_data = Map(config['map']['name'])

        self.app = web.Application(
            handlers=[
                (config["web"]["endpoints"]["position"], PositionHandler),
                (config["web"]["endpoints"]["visualisation3d"], Visualization3DHandler),
                (config["web"]["endpoints"]["visualisation2d"], Visualization2DHandler),
                (config["web"]["endpoints"]["fingerprint"], FingerprintHandler),
                (config["web"]["endpoints"]["path"], PathHandler),
                (config["web"]["endpoints"]["report2d"] + "/([^/]+)", Report2DHandler),
                (config["web"]["endpoints"]["report_map"] + "/([^/]+)", ReportMapHandler, {
                    'access_point_dao': self.access_point_dao,
                    'benchmark_report_dao': self.benchmark_report_dao,
                    'map_data': self.map_data
                }),
                (config["web"]["endpoints"]["map"], MapHandler, {
                    'access_point_dao': self.access_point_dao,
                    'sample_stamp_dao': self.sample_stamp_dao,
                    'map_data': self.map_data
                }),
                (config["web"]["endpoints"]["root"], RootHandler),
            ],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            debug=(env == 'development')
        )

    def get_app(self):
        return self.app

    def run(self):
        self.app.listen(int(config["web"]["port"]), address="0.0.0.0")

        ioloop.IOLoop.instance().start()
