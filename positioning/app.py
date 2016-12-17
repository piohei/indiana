# -*- coding: utf-8 -*-

import time
from collections import defaultdict
from threading import RLock

from db import APDataDAO, SampleStampDAO, AccessPointDAO, PositionDAO
from messaging import Publisher
from models import Time, Position, Mac
from positioning.engine import Engine


class App:
    def __init__(self, engine_config):
        self.global_lock = RLock()

        self.ap_data_dao = APDataDAO()
        self.sample_stamp_dao = SampleStampDAO()
        self.access_point_dao = AccessPointDAO()
        self.position_dao = PositionDAO()

        daos = {
            "ap_data_dao": self.ap_data_dao,
            "sample_stamp_dao": self.sample_stamp_dao,
            "access_point_dao": self.access_point_dao
        }

        strategy = engine_config["strategy_name"]
        strategy_config = engine_config.get("strategy_config", {})
        self.engine = Engine(strategy, daos, strategy_config)
        self.publisher = Publisher("positions")

    def start_engine(self):
        start = time.perf_counter()
        self.engine.initialise()
        end = time.perf_counter()
        print("engine initialised in {}s".format(end-start))

    def make_measures(self, apdatas):
        measures = defaultdict(dict)

        for apdata in apdatas:
            grouped = measures[apdata.device_mac.mac]
            if apdata.router_mac.mac not in grouped:
                grouped[apdata.router_mac.mac] = apdata.rssis

        return measures

    def locate(self):
        start = time.perf_counter()
        measures = self.fetch_measures()
        end = time.perf_counter()
        print("{} measures fetched in {}s".format(len(measures), end-start))
        for device_mac, measure in measures.items():
            if len(measure) >= 3:
                start = time.perf_counter()
                res = self.engine.locate(measure)
                end = time.perf_counter()
                print("engine localised {} in {}s".format(device_mac, end-start))
                self.publisher.publish({"mac": device_mac, "location": res.to_db_object()})
                self.position_dao.save(Position(Mac(device_mac), res))

    def fetch_measures(self):
        end = Time()
        start = Time(end.millis - 30 * 1000)
        apdatas = self.ap_data_dao.get_for_time_range(start, end, asc=False)
        measures = self.make_measures(apdatas)
        return measures

    def run(self):
        while True:
            time.sleep(5)
            self.locate()
