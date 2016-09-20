from db.db import find, replace_one
from models import SampleStamp


class SampleStampDAO(object):
    @staticmethod
    def collection_name():
        return "sample_stamps"

    def save(self, sample_stamp):
        return replace_one(
                collection=self.collection_name(),
                filter={
                    'location.x': sample_stamp.location.x,
                    'location.y': sample_stamp.location.y,
                    'location.z': sample_stamp.location.z
                },
                replacement=sample_stamp.to_dict()
        )

    def find(self, query):
        return map(SampleStamp, find(self.collection_name(), query))

    def all(self):
        return self.find(query={})
