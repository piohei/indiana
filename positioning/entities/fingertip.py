# -*- coding: utf-8 -*-
from models.primitives.location import Location


class Fingertip(object):
    def __init__(self, location, _list):
        if type(location) != Location:
            raise ValueError("Argument location must be type of models.Location")
        self.location = location
        self.list = _list

    def __str__(self, *args, **kwargs):
        return "Fingertip(location={}, list={})".format(
                self.location, self.list
        )
