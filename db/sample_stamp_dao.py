from db.db import replace_one
from db.base_dao import BaseDAO
from models import SampleStamp, Mac, Location, Time


class SampleStampDAO(BaseDAO):
    @staticmethod
    def collection_name():
        return 'sample_stamps'

    def from_db_object(self, db_object):
        return SampleStamp(
            mac=Mac(db_object['mac']),
            location=Location(
                x=db_object['location']['x'],
                y=db_object['location']['y'],
                z=db_object['location']['z']
            ),
            start_time=Time(int(db_object['start_time'])),
            end_time=Time(int(db_object['end_time'])),
            _id=db_object['_id']
        )

    def to_db_object(self, sample_stamp):
        return {
            'mac': sample_stamp.mac.mac,
            'location': {
                'x': sample_stamp.location.x,
                'y': sample_stamp.location.y,
                'z': sample_stamp.location.z
            },
            'start_time': sample_stamp.start_time.millis,
            'end_time': sample_stamp.end_time.millis,
            '_id': sample_stamp._id
        }

    def save(self, sample_stamp):
        return replace_one(
                collection=self.collection_name(),
                filter={
                    'location.x': sample_stamp.location.x,
                    'location.y': sample_stamp.location.y,
                    'location.z': sample_stamp.location.z
                },
                replacement=self.to_db_object(sample_stamp)
        )
