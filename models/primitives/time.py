# -*- coding: utf-8 -*-
import time as oryg_time


class Time(object):
    def __init__(self, millis=None):
        if millis is not None and type(millis) != int:
            raise ValueError('Argument millis must be int')

        self.millis = millis if millis is not None else int(round(oryg_time.time() * 1000))

    def __str__(self, *args, **kwargs):
        seconds = int(self.millis / 1000)
        millis = self.millis - seconds * 1000

        time_s = oryg_time.strftime('%Y-%m-%d %H:%M:%S', oryg_time.gmtime(seconds))

        return '{}.{} UTC'.format(time_s, millis)

    def __repr__(self):
        return '"{}"'.format(str(self))

    def __eq__(self, other):
        return self.millis == other.millis

    def __hash__(self):
        return hash(self.millis)
