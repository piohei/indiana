# -*- coding: utf-8 -*-

from threading import RLock

from models.exception import SampleException


class SampleService(object):
    def __init__(self, ap_data_dao, sample_stamp_dao, benchmark_stamp_dao, lock=RLock()):
        self.benchmark_stamp_dao = benchmark_stamp_dao
        self.sample_stamp_dao = sample_stamp_dao
        self.ap_data_dao = ap_data_dao
        self.current_stamp = None
        self.lock = lock
        self.current_stamp_dao = None

    def set_benchmark_stamp(self, new_benchmark_stamp):
        with self.lock:
            self.current_stamp_dao = self.benchmark_stamp_dao
            self.set_as_current(new_benchmark_stamp)

    def set_sample_stamp(self, new_sample_stamp):
        with self.lock:
            self.current_stamp_dao = self.sample_stamp_dao
            self.set_as_current(new_sample_stamp)

    def set_as_current(self, new_stamp):
        with self.lock:
            if new_stamp.is_same(self.current_stamp):
                raise SampleException("same as current")
            if self.current_stamp is not None:
                self.end_sample()
            self.current_stamp = new_stamp

    def end_sample(self):
        with self.lock:
            if self.current_stamp is not None:
                try:
                    self.current_stamp.end()
                    self.current_stamp_dao.save(self.current_stamp)
                finally:
                    self.current_stamp = None
                    self.current_stamp_dao = None
            else:
                raise SampleException("no stamp")

    def end_if_outdated(self):
        with self.lock:
            if self.current_stamp is not None and self.current_stamp.is_outdated():
                self.end_sample()

    def get_status(self):
        with self.lock:
            if self.current_stamp is None:
                return "no stamp"

            count = self.ap_data_dao.count({
                'created_at': {
                    '$gt': self.current_stamp.start_time.millis
                }
            })

            return "{}: collected {}".format(self.current_stamp, count)

