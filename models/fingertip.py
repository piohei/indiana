# -*- coding: utf-8 -*-

from helpers.utils import millis
from helpers import db


class Fingertip(object):
    VALIDITY_PERIOD = 300000

    def __init__(self, mac='', x=0, y=0, z=0, **kwargs):
        self.mac = mac
        self.location = kwargs['location'] if 'location' in kwargs \
            else {'x': float(x), 'y': float(y), 'z': float(z)}
        self.start_time = kwargs['start_time'] if 'start_time' in kwargs else millis()
        self.end_time = kwargs['end_time'] if 'end_time' in kwargs else None

    def is_outdated(self):
        return millis() > (self.start_time + self.VALIDITY_PERIOD)

    def is_same(self, other):
        return other is not None and self.location == other.location \
               and self.mac == other.mac

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "Fingertip[mac={} location=[{}; {}; {}]]". \
            format(self.mac, self.location['x'],
                   self.location['y'], self.location['z'])

    @staticmethod
    def collection_name():
        return "fingertips"

    def save(self):
        db.insert_into(self.collection_name(), self.to_dict())

    @classmethod
    def find_all(cls):
        return map(lambda f: Fingertip(**f), db.find(cls.collection_name()))
