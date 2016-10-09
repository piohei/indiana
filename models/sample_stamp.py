# -*- coding: utf-8 -*-
from exception.exception import SampleException

from .location import Location
from .mac import Mac
from .time import Time


class SampleStamp(object):
    VALIDITY_PERIOD = 300000

    def __init__(self, mac, location, start_time=None, end_time=None, **ignored):
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

    @staticmethod
    def from_db_object(db_object):
        return SampleStamp(
            mac=Mac.from_db_object(db_object["mac"]),
            location=Location.from_db_object(db_object["location"]),
            start_time=Time.from_db_object(db_object["start_time"]) if db_object["start_time"] is not None else None,
            end_time=Time.from_db_object(db_object["end_time"]) if db_object["end_time"] is not None else None
        )

    def to_db_object(self):
        return {
            "mac": self.mac.to_db_object(),
            "location": self.location.to_db_object(),
            "start_time": self.start_time.to_db_object() if self.start_time is not None else None,
            "end_time": self.end_time.to_db_object() if self.end_time is not None else None
        }

    def __str__(self):
        return "SampleStamp[mac={} location={} time=({} - {})]".format(
                    self.mac, self.location, self.start_time, self.end_time
                )

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
