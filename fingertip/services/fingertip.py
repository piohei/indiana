# -*- coding: utf-8 -*-

from threading import RLock

class FingertipException(Exception):
    def __init__(self, message):
        self.message = message


class FingertipService(object):
    def __init__(self, lock=RLock()):
        self.current_fingertip = None
        self.lock = lock

    def set_fingertip(self, mac="", x=0, y=0, z=0):
        with self.lock:
            new_fingertip = models.Fingertip(mac, x, y, z)
            if new_fingertip.is_same(self.current_fingertip):
                raise FingertipException("same as current")
            if self.current_fingertip is not None:
                self.end_fingertip()
            self.current_fingertip = new_fingertip

    def end_fingertip(self):
        with self.lock:
            if self.current_fingertip is not None:
                self.current_fingertip.end_time = millis()
                try:
                    self.current_fingertip.save()
                finally:
                    self.current_fingertip = None
            else:
                raise FingertipException("no current fingertip")

    def end_if_outdated(self):
        with self.lock:
            if self.current_fingertip and self.current_fingertip.is_outdated():
                self.end_fingertip()

    def get_status(self):
        with self.lock:
            if self.current_fingertip is None:
                return "no fingertip"
            count = models.ap_data.count_entries_since(self.current_fingertip.start_time)
            return "{}: collected {}".format(self.current_fingertip, count)

service = FingertipService()
