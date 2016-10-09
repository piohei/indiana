# -*- coding: utf-8 -*-
from .sample_stamp import SampleStamp


class Sample(object):
    def __init__(self, stamp, ap_data_by_mac_and_signal):
        if type(stamp) != SampleStamp:
            raise ValueError("Argument stamp must be type of models.SampleStamp")

        self.ap_data_by_mac_and_signal = ap_data_by_mac_and_signal
        self.stamp = stamp

    def get_measure_for(self, mac, signal):
        return self.ap_data_by_mac_and_signal[mac][signal]

    def location(self):
        return self.stamp.location

    def __str__(self, *args, **kwargs):
        return "Sample[stamp={}, ap_data_by_mac_and_signal={}]".format(
                    self.stamp, self.ap_data_by_mac_and_signal
                )
