import pprint
import time
from multiprocessing import Process

import numpy as np

from ap_data_listener.app import App as ApDataListenerApp
from benchmark.engine_configs import configs
from config import config
from db import BenchmarkStampDAO, APDataDAO, PositionDAO
from db.base import Collection
from models import Time
from positioning.app import App as PositioningApp
from simulator import SimpleSimulator


def start_ap_listener():
    ap_data_listener_app = ApDataListenerApp()
    ap_data_listener_process = Process(target=ap_data_listener_app.run)
    ap_data_listener_process.start()
    return ap_data_listener_process

ap_data_dao = APDataDAO()
position_dao = PositionDAO()
benchmark_stamp_dao = BenchmarkStampDAO()
benchmark_reports_collection = Collection(config["db"]["collections"]["benchmark_report"])

benchmark_stamps = benchmark_stamp_dao.find()
samples = [(stamp, list(map(ap_data_dao.to_db_object, ap_data_dao.get_for_time_range(stamp.start_time, stamp.end_time)))) for stamp in benchmark_stamps]


def start_engine(config):
    positioning_app = PositioningApp(config)
    positioning_app.start_engine()
    positioning_app_process = Process(target=positioning_app.run)
    positioning_app_process.start()
    return positioning_app_process


def to_errors(positions, stamp):
    return np.array([pos.location.distance_from(stamp.location) for pos in positions])


def big_separator():
    print("=================================================================")


def small_separator():
    print("-----------------------------------------------------------------")


for engine_config in configs:
    start_time = Time()
    big_separator()
    print(engine_config)
    small_separator()
    partial_reports = []
    global_errors = []
    ap_data_listener_process = start_ap_listener()
    for stamp, ap_datas in samples:
        print(stamp.location)
        positioning_app = start_engine(engine_config)
        simulator = SimpleSimulator.create(ap_datas)
        start, simulation_end = simulator.run()
        time.sleep(5)
        positioning_app.terminate()
        end = Time()
        positions = position_dao.get_for_time_range(start, end)
        errors = to_errors(positions, stamp)
        partial_reports.append({
            "start": start.millis,
            "end": end.millis,
            "min_error": float(errors.min()),
            "max_error": float(errors.max()),
            "avg_error": float(errors.mean()),
            "std_error": float(errors.std()),
            "positions_number": len(positions),
            "real_location": benchmark_stamp_dao.to_db_object(stamp)["location"],
            "engine_positions": [position_dao.to_db_object(pos)["location"] for pos in positions],
            "errors": [float(e) for e in errors]
        })
        global_errors.extend(errors)
        small_separator()
        time.sleep(30)
    ap_data_listener_process.terminate()
    np_errors = np.array(global_errors)
    report = {"engine_config": engine_config,
              "start": start_time.millis,
              "end": Time().millis,
              "global_stats": {
                  "min_error": float(np_errors.min()),
                  "max_error": float(np_errors.max()),
                  "avg_error": float(np_errors.mean()),
                  "std_error": float(np_errors.std())
              },
              "partial_reports": partial_reports}

    benchmark_reports_collection.insert(report)
    copy = report.copy()
    copy.pop("partial_reports")
    pprint.pprint(copy)




