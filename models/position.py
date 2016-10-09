# -*- coding: utf-8 -*-
from .basic_types.mac import Mac
from .basic_types.location import Location
from .basic_types.time import Time


class Position(object):
    def __init__(self, mac, location, created_at=None):
        if type(mac) != Mac:
            raise ValueError("Argument mac must be type of models.Mac")
        if type(location) != Location:
            raise ValueError("Argument location must be type of models.Location")
        if created_at is not None and type(time) != Time:
            raise ValueError("Argument created_at must be type of models.Time")

        self.mac = mac
        self.location = location
        self.created_at = created_at if created_at is not None else Time()

    def __str__(self, *args, **kwargs):
        return "Position(mac={}, location={}, created_at={})".format(
                    self.mac, self.location, self.created_at
                )
