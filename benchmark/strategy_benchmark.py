import time
from multiprocessing import Process

import numpy as np

from benchmark.benchmark_logger import BenchmarkLogger
from config import config
from db import BenchmarkStampDAO, APDataDAO, PositionDAO, BenchmarkReportDAO
from models import Time
from positioning.runner import run as run_positioning
from simulator import SimpleSimulator


class StrategyBenchmark(object):
    def __init__(self):
        self.benchmark_stamp_dao = BenchmarkStampDAO()
        self.benchmark_report_dao = BenchmarkReportDAO()
        self.position_dao = PositionDAO()
        self.logger = BenchmarkLogger()
        self.configs = self.create_configs()
        self.samples = self.create_samples()
        self.partial_reports = None
        self.global_errors = None

    @staticmethod
    def create_configs():
        cfgs = [c.copy() for c in config["benchmark"]["configs"]]
        for c in cfgs:
            c.update(config["benchmark"]["common_config"])
        return cfgs

    def create_samples(self):
        ap_data_dao = APDataDAO()
        benchmark_stamps = self.benchmark_stamp_dao.all()
        samples_objects = [(s, ap_data_dao.get_for_time_range(s.start_time, s.end_time)) for s in benchmark_stamps]
        return [(s, list(map(ap_data_dao.to_db_object, apdatas))) for s, apdatas in samples_objects]

    @staticmethod
    def start_engine(engine_cfg):
        positioning_app_process = Process(target=run_positioning, args=(engine_cfg, 0))
        positioning_app_process.start()
        time.sleep(5)
        return positioning_app_process

    @staticmethod
    def to_errors(positions, stamp):
        return np.array([pos.location.distance_from(stamp.location) for pos in positions])

    def run(self):
        for engine_config in self.configs:
            start_time = Time()
            self.logger.print_engine_config(engine_config)
            self.clear_reports_data()
            for stamp, ap_datas in self.samples:
                end, start = self.simulate(ap_datas, engine_config)
                positions = self.position_dao.get_for_time_range(start, end, query={"mac": stamp.mac.mac})
                self.add_partial_report(end, positions, stamp, start)
                time.sleep(20)
            report = self.create_report(engine_config, start_time)
            self.benchmark_report_dao.save(report)
            self.logger.print_report(report)

    def create_report(self, engine_config, start_time):
        np_errors = np.array(self.global_errors)
        report = {"engine_config": engine_config,
                  "start": start_time.millis,
                  "end": Time().millis,
                  "global_stats": {
                      "min_error": float(np_errors.min()),
                      "max_error": float(np_errors.max()),
                      "avg_error": float(np_errors.mean()),
                      "std_error": float(np_errors.std())
                  },
                  "partial_reports": self.partial_reports}
        return report

    def add_partial_report(self, end, positions, stamp, start):
        errors = self.to_errors(positions, stamp)
        self.partial_reports.append({
            "start": start.millis,
            "end": end.millis,
            "min_error": float(errors.min()),
            "max_error": float(errors.max()),
            "avg_error": float(errors.mean()),
            "std_error": float(errors.std()),
            "positions_number": len(positions),
            "real_location": self.benchmark_stamp_dao.to_db_object(stamp)["location"],
            "engine_positions": [self.position_dao.to_db_object(pos)["location"] for pos in positions],
            "errors": [float(e) for e in errors]
        })
        self.global_errors.extend(errors)

    def clear_reports_data(self):
        self.partial_reports = []
        self.global_errors = []

    def simulate(self, ap_datas, engine_config):
        positioning_app = self.start_engine(engine_config)
        simulator = SimpleSimulator.create(ap_datas)
        start, simulation_end = simulator.run()
        time.sleep(5)
        positioning_app.terminate()
        end = Time()
        return end, start
