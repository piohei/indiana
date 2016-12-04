# -*- coding: utf-8 -*-

from fingertip.handlers.base_stamp_handler import BaseStampHandler


class BenchmarkStampHandler(BaseStampHandler):
    def set_stamp(self, sample):
        self.sample_service.set_benchmark_stamp(sample)
