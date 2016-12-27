import os

import yaml

from db import AccessPointDAO
from db.map_dao import MapDAO


class StaticDataLoader(object):
    STATIC_DATA_DIR = os.path.join(os.getcwd(), "config_files", "static_data")
    MAPS_DIR = os.path.join(STATIC_DATA_DIR, "maps")
    ACCESS_POINTS_FILE = os.path.join(STATIC_DATA_DIR, "access_points.yml")

    def __init__(self):
        self.map_dao = MapDAO()
        self.access_point_dao = AccessPointDAO()

    def load(self):
        self.load_maps()
        self.load_access_points()

    def load_maps(self):
        print("\t cleaning maps")
        self.map_dao.collection.clear()
        print("\tloading maps")
        map_files = [name for name in os.listdir(self.MAPS_DIR) if name.endswith(".yml")]
        for filename in map_files:
            name = filename[0:-4]
            path = os.path.join(self.MAPS_DIR, filename)
            print("\t\tloading map {} from {}".format(name, path))
            raw_map = self.load_yaml(path)
            raw_map["name"] = name
            map_obj = self.map_dao.from_db_object(raw_map)
            self.map_dao.save(map_obj)

    def load_access_points(self):
        print("\t cleaning access_points")
        self.access_point_dao.collection.clear()
        print("\tloading access_points from {}".format(self.ACCESS_POINTS_FILE))
        raw_aps = self.load_yaml(self.ACCESS_POINTS_FILE)
        aps = list(map(self.access_point_dao.from_db_object, raw_aps))
        for ap in aps:
            self.access_point_dao.save(ap)

    @staticmethod
    def load_yaml(path):
        with open(path, "r") as datafile:
            return yaml.load(datafile)