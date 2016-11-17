# -*- coding: utf-8 -*-
import math


class Location(object):
    def __init__(self, x, y, z):
        if type(x) != int and type(x) != float:
            raise ValueError("Argument x must be float or int")
        if type(y) != int and type(y) != float:
            raise ValueError("Argument y must be float or int")
        if type(z) != int and type(z) != float:
            raise ValueError("Argument z must be float or int")

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def distance_from(self, loc):
        return math.sqrt(
                   math.pow(self.x - loc.x, 2) + \
                   math.pow(self.y - loc.y, 2) + \
                   math.pow(self.z - loc.z, 2)
               )

    @staticmethod
    def from_db_object(db_object):
        return Location(
            x=db_object["x"],
            y=db_object["y"],
            z=db_object["z"]
        )

    def to_db_object(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

    def __str__(self, *args, **kwargs):
        return "Location[{}; {}; {}]".format(self.x, self.y, self.z)

    def __repr__(self):
        return '"{}"'.format(str(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(str(self))
