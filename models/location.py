# -*- coding: utf-8 -*-
import math


class Location(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def distnace_from(self, loc):
        return math.sqrt(
                   math.pow(self.x - loc.x, 2) + \
                   math.pow(self.y - loc.y, 2) + \
                   math.pow(self.z - loc.z, 2)
               )

    def to_dict(self):
        return dict(self.__dict__)

    def __str__(self, *args, **kwargs):
        return "Location[{}; {}; {}]".format(self.x, self.y, self.z)
