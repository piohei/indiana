# -*- coding: utf-8 -*-


class RSSI(object):
    def __init__(self, dBm):
        if type(dBm) != int and type(dBm) != float:
            raise ValueError('Argument dBm must be float or int')
        if float(dBm) > 0:
            raise ValueError('Argument dBm must zero or less')

        self.dBm = float(dBm)

    def __str__(self, *args, **kwargs):
        return '{} dBm'.format(self.dBm)

    def __repr__(self):
        return '"{}"'.format(str(self))

    def __eq__(self, other):
        return self.dBm == other.dBm

    def __hash__(self):
        return hash(self.dBm)
