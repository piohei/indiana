# -*- coding: utf-8 -*-

from threading import RLock

from exception.exception import SampleException
from helpers.utils import millis
from models import SampleStamp, APData


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
                self.current_sample_stamp.end_time = millis()
                try:
                    self.sample_stamp_dao.save(self.current_sample_stamp)
                finally:
                    self.current_sample_stamp = None
            else:
                raise SampleException("no current fingertip")

    def end_if_outdated(self):
        with self.lock:
            if self.current_sample_stamp and self.current_sample_stamp.is_outdated():
                self.end_sample()

    def save_ap_data_for_sample(self, ap_data_dict):
        stamp = self.current_sample_stamp
        if stamp is None or stamp.is_outdated():
            raise SampleException("sample stamp gone or outdated")
        self.ap_data_dao.save_dict(ap_data_dict)

    def get_status(self):
        with self.lock:
            if self.current_sample_stamp is None:
                return "no fingertip"
            count = self.ap_data_dao.count_entries_since(self.current_sample_stamp.start_time)
            return "{}: collected {}".format(self.current_sample_stamp, count)

