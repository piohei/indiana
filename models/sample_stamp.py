# -*- coding: utf-8 -*-
from exception.exception import SampleException
from helpers.utils import millis
from models.location import Location


class SampleStamp(object):
    VALIDITY_PERIOD = 300000

    def __init__(self, mac, location, start_time=None, end_time=None, **ignored):
        self.mac = mac
        self.location = Location(**location)
        self.start_time = start_time if start_time is not None else millis()
        self.end_time = end_time

    def is_outdated(self):
        return millis() > (self.start_time + self.VALIDITY_PERIOD)

    def is_same(self, other):
        return other is not None and self.location == other.location \
               and self.mac == other.mac

    def end(self):
        if self.end_time is not None:
            raise SampleException("Sample already ended")
        self.end_time = millis()

    def to_dict(self):
        d = dict(self.__dict__)
        d["location"] = self.location.to_dict()
        return d

    def __str__(self):
        return "Sample[{} {}]".format(self.mac, self.location)

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
