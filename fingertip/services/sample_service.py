# -*- coding: utf-8 -*-

from threading import RLock

from exception import SampleException
from models import APData, Mac, Time, RSSI, Signal


class SampleService(object):
    def __init__(self, ap_data_dao, sample_stamp_dao, lock=RLock()):
        self.sample_stamp_dao = sample_stamp_dao
        self.ap_data_dao = ap_data_dao
        self.current_sample_stamp = None
        self.lock = lock

    def set_sample_stamp(self, new_sample_stamp):
        with self.lock:
            if new_sample_stamp.is_same(self.current_sample_stamp):
                raise SampleException("same as current")
            if self.current_sample_stamp is not None:
                self.end_sample()
            self.current_sample_stamp = new_sample_stamp

    def end_sample(self):
        with self.lock:
            if self.current_sample_stamp is not None:
                try:
                    self.current_sample_stamp.end()
                    self.sample_stamp_dao.save(self.current_sample_stamp)
                finally:
                    self.current_sample_stamp = None
            else:
                raise SampleException("no current fingertip")

    def end_if_outdated(self):
        with self.lock:
            if self.current_sample_stamp is not None and self.current_sample_stamp.is_outdated():
                self.end_sample()

    def save_ap_data_for_sample(self, ap_data):
        self.ap_data_dao.save(ap_data)

    def get_status(self):
        with self.lock:
            if self.current_sample_stamp is None:
                return "no fingertip"

            count = self.ap_data_dao.count({
                'created_at': {
                    '$gt': self.current_sample_stamp.start_time.millis
                }
            })

            return "{}: collected {}".format(self.current_sample_stamp, count)

