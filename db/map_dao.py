from db.base import BaseDAO
from db.base.db_exception import DBException
from models import Location, Map


class MapDAO(BaseDAO):
    def entity(self):
        return "map"

    def from_db_object(self, db_object):
        floor = [self.parse_point(point) for point in db_object['floor_polygon']]
        walls = [[self.parse_point(wall[0]), self.parse_point(wall[1])] for wall in db_object['walls']]
        name = db_object["name"]
        _id = db_object.get("_id")
        return Map(name, floor, walls, _id)

    def to_db_object(self, object):
        return {
            "name": object.name,
            "floor_polygon": [{"x": loc.x, "y": loc.y, "z": loc.z} for loc in object.floor],
            "walls": [
                [{"x": wall[0].x, "y": wall[0].y, "z": wall[0].z}, {"x": wall[1].x, "y": wall[1].y, "z": wall[1].z}]
                for wall in object.walls]
        }

    def find_by_name(self, name):
        ret = self.find({"name": name})
        if len(ret) == 1:
            return ret[0]
        else:
            raise DBException("invalid name")

    @staticmethod
    def parse_point(point):
        return Location(
                float(point["x"]),
                float(point["y"]),
                float(point["z"])
        )