# -*- coding: utf-8 -*-

from threading import RLock

from fingerprint.exception.sample_exception import SampleException


class PathService(object):
    def __init__(self, path_dao, lock=RLock()):
        self.path_dao = path_dao
        self.current_path_stamp = None
        self.lock = lock

    def set_path_stamp(self, new_path_stamp):
        with self.lock:
            if new_path_stamp.is_same(self.current_path_stamp):
                raise SampleException("same as current")
            if self.current_path_stamp is not None:
                self.end_path()
            self.current_path_stamp = new_path_stamp

    def end_path(self):
        result = None
        with self.lock:
            if self.current_path_stamp is not None:
                try:
                    self.current_path_stamp.end()
                    result = self.path_dao.save(self.current_path_stamp)
                finally:
                    self.current_path_stamp = None
                    return result
            else:
                raise SampleException("no current path")

