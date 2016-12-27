# -*- coding: utf-8 -*-
from models.exception import SampleException

from .base.base_db_model import BaseModel

from .primitives.mac import Mac
from .primitives.time import Time


class PathStamp(BaseModel):

    def __init__(self, mac, name):
        super().__init__()
        if type(mac) != Mac:
            raise ValueError("Argument mac must be type of models.Mac")
        if type(name) != str:
            raise ValueError("Argument mac must be of type str")

        self.mac = mac
        self.name = name
        self.start_time = Time()
        self.end_time = None

    def is_same(self, other):
        return other is not None and other.mac == self.mac and other.name == self.name

    def end(self):
        if self.end_time is not None:
            raise SampleException("Sample already ended")
        self.end_time = Time()
