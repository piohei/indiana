# -*- coding: utf-8 -*-
from .base.base_db_model import BaseDBModel

from .primitives.mac import Mac
from .primitives.location import Location
from .primitives.time import Time


class Position(BaseDBModel):
    def __init__(self, mac, location, created_at=None, _id=None):
        BaseDBModel.__init__(self, _id)
        if type(mac) != Mac:
            raise ValueError("Argument mac must be type of models.Mac")
        if type(location) != Location:
            raise ValueError("Argument location must be type of models.Location")
        if created_at is not None and type(created_at) != Time:
            raise ValueError("Argument created_at must be type of models.Time")

        self.mac = mac
        self.location = location
        self.created_at = created_at if created_at is not None else Time()

    def __str__(self, *args, **kwargs):
        return "Position(id={}, mac={}, location={}, created_at={})".format(
                    self._id, self.mac, self.location, self.created_at
                )
