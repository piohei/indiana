# -*- coding: utf-8 -*-
from .sample_stamp import SampleStamp


class Sample(object):
    def __init__(self, stamp, ap_data_by_band_and_mac):
        if type(stamp) != SampleStamp:
            raise ValueError("Argument stamp must be type of models.SampleStamp")

        self.ap_data_by_band_and_mac = ap_data_by_band_and_mac
        self.stamp = stamp

    def get_measure_for(self, band, mac):
        return self.ap_data_by_band_and_mac[band][mac]

    def location(self):
        return self.stamp.location

    def __str__(self, *args, **kwargs):
        return "Sample[stamp={}, ap_data_by_band_and_mac={}]".format(
                    self.stamp, self.ap_data_by_band_and_mac
                )
