from db.base import StampDAO


class BenchmarkStampDAO(StampDAO):
    def entity(self):
        return "benchmark_stamp"
