# -*- coding: utf-8 -*-
from .primitives.location import Location


class Fingertip(object):
    def __init__(self, location, ap_data_by_mac_and_signal):
        if type(location) != Location:
            raise ValueError("Argument location must be type of models.Location")

        self.location = location
        self.ap_data_by_mac_and_signal = ap_data_by_mac_and_signal

    def __str__(self, *args, **kwargs):
        return "Fingertip(location={}, ap_data_by_mac_and_signal={})".format(
                    self.location, self.ap_data_by_mac_and_signal
                )
