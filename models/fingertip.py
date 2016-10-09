# -*- coding: utf-8 -*-
from .basic_types.location import Location


class Fingertip(object):
    def __init__(self, location, measure_for_band_and_mac):
        if type(location) != Location:
            raise ValueError("Argument location must be type of models.Location")

        self.location = location
        self.measure_for_band_and_mac = measure_for_band_and_mac

    def __str__(self, *args, **kwargs):
        return "Fingertip[location={}, measure_for_band_and_mac={}]".format(
                    self.location, self.measure_for_band_and_mac
                )
