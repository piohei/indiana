from db.base_dao import BaseDAO
from models.access_point import AccessPoint
from models.primitives.location import Location
from models.primitives.mac import Mac


class AccessPointDAO(BaseDAO):
    @staticmethod
    def collection_name():
        return 'access_points'

    def from_db_object(self, db_object):
        return AccessPoint(
            number=db_object["number"],
            name=db_object["name"],
            location=Location(
                x=db_object["location"]["x"],
                y=db_object["location"]["y"],
                z=db_object["location"]["z"]
            ),
            mac=Mac(db_object["mac"]),
            active=bool(db_object["active"]),
            _id=db_object["_id"]
        )

    def to_db_object(self, ap):
        return {
            'number': ap.number,
            'name': ap.name,
            'location': {
                'x': ap.location.x,
                'y': ap.location.y,
                'z': ap.location.z
            },
            'mac': ap.mac.mac,
            'active': ap.active,
            '_id': ap._id
        }

    def find(self, query={}, **kwargs):
        if 'sort' not in kwargs:
            return super().find(query, sort=[("number", 1)], **kwargs)
        return super().find(query, **kwargs)

    def active(self):
        return self.find({'active': True})

