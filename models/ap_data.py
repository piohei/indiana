# -*- coding: utf-8 -*-
from .mac import Mac
from .time import Time
from .rssi import RSSI
from .signal import Signal


class APData(object):
    def __init__(self, router_mac, device_mac, created_at, rssis, signal):
        if type(router_mac) != Mac:
            raise ValueError('Argument router_mac must be type of models.Mac')
        if type(device_mac) != Mac:
            raise ValueError('Argument device_mac must be type of models.Mac')
        if type(created_at) != Time:
            raise ValueError('Argument created_at must be type of models.Time')
        wrong_value = False
        for k in rssis.keys():
            if type(rssis[k]) != RSSI:
                wrong_value = True
                break
        if type(rssis) != dict or len(rssis) < 1 or wrong_value:
            raise ValueError('Argument rssi must be type of nonempty dict of models.RSSI')
        if type(signal) != Signal:
            raise ValueError('Argument signal must be type of models.Signal')

        self.router_mac = router_mac
        self.device_mac = device_mac
        self.created_at = created_at
        self.rssis = rssis
        self.signal = signal

    def __str__(self, *args, **kwargs):
        rssis = ', '.join(list(map(lambda k: str(k) + ': ' + str(self.rssis[k]), self.rssis.keys())))
        return 'APData(router_mac={}, device_mac={}, rssis=[{}], singal={}, created_at={})'.format(
                self.router_mac, self.device_mac, rssis, self.signal, self.created_at)
