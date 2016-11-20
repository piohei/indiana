from db.base_dao import BaseDAO
from models import Position, Mac, Location, Time


class PositionDAO(BaseDAO):
    @staticmethod
    def collection_name():
        return 'positions'

    def from_db_object(self, db_object):
        return Position(
            mac=Mac(db_object['mac']),
            location=Location(
                x=db_object['location']['x'],
                y=db_object['location']['y'],
                z=db_object['location']['z']
            ),
            created_at=Time(int(db_object['created_at'])),
            _id=db_object['_id']
        )

    def to_db_object(self, position):
        return {
            'mac': position.mac.mac,
            'location': {
                'x': position.location.x,
                'y': position.location.y,
                'z': position.location.z
            },
            'created_at': position.created_at.millis,
            '_id': position._id
        }
