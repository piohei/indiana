from db.base import StampDAO


class SampleStampDAO(StampDAO):
    def entity(self):
        return "sample_stamp"
