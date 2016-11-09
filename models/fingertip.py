# -*- coding: utf-8 -*-
from .base.base_model import BaseModel

from .primitives.location import Location


class Fingertip(BaseModel):
    def __init__(self, location, _list):
        if type(location) != Location:
            raise ValueError("Argument location must be type of models.Location")

        self.location = location
        self.list = _list

    def __str__(self, *args, **kwargs):
        return "Fingertip(location={}, ist={})".format(
                    self.location, self.list
                )
