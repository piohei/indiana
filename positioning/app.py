# -*- coding: utf-8 -*-

import time
from threading import RLock

from tornado import web, ioloop

from config import config
from config import env
from db import APDataDAO, SampleStampDAO
from db.access_point_dao import AccessPointDAO
from helpers.utils import mac_regexp_dashes
from positioning.engine import Engine
from .handlers import *


class App:
    def __init__(self):
        self.global_lock = RLock()

        self.ap_data_dao = APDataDAO()
        self.sample_stamp_dao = SampleStampDAO()
        self.access_point_dao = AccessPointDAO()

        daos = {
            "ap_data_dao": self.ap_data_dao,
            "sample_stamp_dao": self.sample_stamp_dao,
            "access_point_dao": self.access_point_dao
        }

        # self.engine = Engine(strategy="FullLinearRegression", daos=daos)
        # self.engine = Engine(strategy="1-NN", daos=daos, strategy_config={"chain": "beta"})
        # self.engine = Engine(strategy="1-NN", daos=daos, strategy_config={"chain": "permutations", "ap_data_per_ap": 2})
        # self.engine = Engine(strategy="1-NN", daos=daos, strategy_config={"chain": "consecutive"})
        strategy = config["engine"]["strategy_name"]
        strategy_config = config["engine_config"].get("strategy_config", {})
        self.engine = Engine(strategy, daos, strategy_config)


        self.app = web.Application(handlers=[
            (r"/position/({})".format(mac_regexp_dashes()), PositionHandler, {
                    "ap_data_dao": self.ap_data_dao,
                    "engine": self.engine
                })
        ], debug=(env == 'development'))

    def get_app(self):
        return self.app

    def start_engine(self):
        start = time.perf_counter()
        self.engine.initialise()
        end = time.perf_counter()
        print("engine initialised in {}s".format(end-start))
        # self.print_engine_stats()

    def print_engine_stats(self):
        stats = self.engine.stats()
        print("fingertips statistics:")
        print("\tlocations\t\t\t\t\t{}".format(stats["locations"]))
        print("\tnumber of fingertips\t\t{}".format(stats["all"]))
        print("\tavg per location\t\t\t{}".format(stats["avg"]))
        print("\tmin and max per location\t{} - {}".format(stats["min"], stats["max"]))

    def run(self):
        self.start_engine()
        self.app.listen(8886, address="0.0.0.0")
        ioloop.IOLoop.instance().start()
