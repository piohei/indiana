# -*- coding: utf-8 -*-

import os

from tornado import web, ioloop

from config import env, config
from db import AccessPointDAO, BenchmarkReportDAO, SampleStampDAO
from db.map_dao import MapDAO
from web.handlers import views, ws
from web.handlers.api import API


class App:
    def __init__(self):
        self.access_point_dao    = AccessPointDAO()
        self.sample_stamp_dao    = SampleStampDAO()
        self.benchmark_report_dao = BenchmarkReportDAO()
        self.map_dao = MapDAO()

        daos = {"access_point_dao": self.access_point_dao,
                "sample_stamp_dao": self.sample_stamp_dao,
                "benchmark_report_dao": self.benchmark_report_dao,
                "map_dao": self.map_dao}

        self.api = API(config, daos)

        self.map_data = self.map_dao.find_by_name(config['map']['name'])

        self.app = web.Application(
            handlers=[
                (config["web"]["endpoints"]["position"], ws.PositionHandler),
                (config["web"]["endpoints"]["visualisation3d"], views.Visualization3DHandler),
                (config["web"]["endpoints"]["visualisation2d"], views.Visualization2DHandler),
                (config["web"]["endpoints"]["fingerprint"], views.FingerprintHandler),
                (config["web"]["endpoints"]["path"], views.PathHandler),
                (config["web"]["endpoints"]["report2d"] + "/([^/]+)", views.Report2DHandler),
                # (config["web"]["endpoints"]["report_map"] + "/([^/]+)", api.ReportMapHandler, {
                #     'access_point_dao': self.access_point_dao,
                #     'benchmark_report_dao': self.benchmark_report_dao,
                #     'map_data': self.map_data
                # }),
                # (config["web"]["endpoints"]["map"], api.MapHandler, {
                #     'access_point_dao': self.access_point_dao,
                #     'sample_stamp_dao': self.sample_stamp_dao,
                #     'map_data': self.map_data
                # }),
                (config["web"]["endpoints"]["root"], views.RootHandler),
            ],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            debug=(env == 'development')
        )

        self.app.add_handlers(".*$".format(config["web"]["routes"]["api"]["prefix"]), self.api.get_handlers(config))

    def get_app(self):
        return self.app

    def run(self):
        self.app.listen(int(config["web"]["port"]), address="0.0.0.0")

        ioloop.IOLoop.instance().start()
