# -*- coding: utf-8 -*-
from exception.exception import SampleException

from .base import BaseDBModel

from .primitives.location import Location
from .primitives.mac import Mac
from .primitives.time import Time


class SampleStamp(BaseDBModel):
    VALIDITY_PERIOD = 300000

    def __init__(self, mac, location, start_time=None, end_time=None, _id=None):
        BaseDBModel.__init__(self, _id)
        if type(mac) != Mac:
            raise ValueError("Argument mac must be type of models.Mac")
        if type(location) != Location:
            raise ValueError("Argument location must be type of models.Location")
        if start_time is not None and type(start_time) != Time:
            raise ValueError("Argument start_time must be type of models.Time")
        if end_time is not None and type(end_time) != Time:
            raise ValueError("Argument end_time must be type of models.Time")

        self.mac = mac
        self.location = location
        self.start_time = start_time if start_time is not None else Time()
        self.end_time = end_time

    def is_outdated(self):
        return Time() > (self.start_time + self.VALIDITY_PERIOD)

    def is_same(self, other):
        return other is not None and self.location == other.location \
               and self.mac == other.mac

    def end(self):
        if self.end_time is not None:
            raise SampleException("Sample already ended")
        self.end_time = Time()

    def __str__(self):
        return "SampleStamp[id={} mac={} location={} time=({} - {})]".format(
                    self._id, self.mac, self.location, self.start_time, self.end_time
                )
