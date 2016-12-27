from multiprocessing import Process
from threading import RLock

import requests

from benchmark.runner import run as run_benchmark
from config import config
from models import Time


class BenchmarkException(Exception):
    def __init__(self, message):
        self.message = message


class BenchmarkService(object):
    def __init__(self):
        self.current_benchmark = None
        self.lock = RLock()
        self.apdata_listener_url = self.get_url_from_config()
        self.benchmark_start_time = None

    def get_url_from_config(self):
        idx = config["simulator"]["ap_data_listener_index"]
        listener = config["ap_data"][idx]
        return "{}:{}{}".format(listener["host"], listener["port"], listener["endpoint"])

    def check_current_benchmark_inactive(self):
        with self.lock:
            return self.current_benchmark is None or not self.current_benchmark.is_alive()

    def kill_current_benchmark(self):
        with self.lock:
            if self.check_current_benchmark_inactive():
                raise BenchmarkException("no current benchmark")
            try:
                self.current_benchmark.terminate()
                self.current_benchmark.join(2)
                if self.current_benchmark.is_alive():
                    raise BenchmarkException("Benchmark terminated unsuccesfully")
            finally:
                self.current_benchmark = None

    def start_new_benchmark(self):
        with self.lock:
            if not self.check_current_benchmark_inactive():
                raise BenchmarkException("Benchmark already in progress")
            self.ping_listener()
            self.current_benchmark = Process(target=run_benchmark)
            self.current_benchmark.start()
            self.benchmark_start_time = Time()

    def ping_listener(self):
        res = requests.options(self.apdata_listener_url)
        if res.status_code != 204:
            raise BenchmarkException("APData Listener for benchmark unavailable")

    def get_status(self):
        if not self.check_current_benchmark_inactive():
            return "Benchmark runnung since {}".format(self.benchmark_start_time)
        else:
            return "no current benchmark"
