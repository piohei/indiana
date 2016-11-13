# -*- coding: utf-8 -*-

from threading import RLock

import time
from tornado import web, ioloop

from config import env
from positioning.engine import Engine
from positioning.links.filter.random_n_for_each_ap import RandomNForEachAPInSample

from .handlers import *

from db import APDataDAO, SampleStampDAO

from helpers.utils import mac_regexp_dashes


class App:
    def __init__(self):
        self.global_lock = RLock()

        self.ap_data_dao = APDataDAO()
        self.sample_stamp_dao = SampleStampDAO()

        self.engine = Engine(chain='permutations', params={
            'ap_data_dao': self.ap_data_dao,
            'sample_stamp_dao': self.sample_stamp_dao,
            RandomNForEachAPInSample.N: 2
        })

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
        self.print_engine_stats()

    def print_engine_stats(self):
        stats = self.engine.fingertips.stats
        print("fingertips statistics:")
        print("\tlocations\t\t\t\t\t{}".format(stats["locations"]))
        print("\tnumber of fingertips\t\t{}".format(stats["all"]))
        print("\tavg per location\t\t\t{}".format(stats["avg"]))
        print("\tmin and max per location\t{} - {}".format(stats["min"], stats["max"]))

    def run(self):
        self.start_engine()
        self.app.listen(8886, address="0.0.0.0")
        ioloop.IOLoop.instance().start()
