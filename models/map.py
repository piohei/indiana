import os

import yaml

from .primitives.location import Location


class Map(object):
    def __init__(self, name):
        self.name = name
        self.load()

    def load(self):
        map_path = os.path.abspath(
            os.path.join(
                os.getcwd(), "config_files", "static_data", "maps", "{}.yml".format(self.name)
            )
        )

        data = None
        with open(map_path, 'r') as ymlfile:
            data = yaml.load(ymlfile)

        self.floor = []
        for raw_point in data['floor']['polygon']:
            self.floor.append(self.parse_point(raw_point))

        self.walls = []
        for wall in data['walls']['sections']:
            self.walls.append([
                self.parse_point(wall[0]),
                self.parse_point(wall[1])
            ])

    def parse_point(self, line):
        raw_x, raw_y, raw_z = line.split()
        return Location(
            float(raw_x),
            float(raw_y),
            float(raw_z)
        )

    def __str__(self):
        return "Map(name={})".format(self.name)
