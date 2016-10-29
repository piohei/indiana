from positioning.links.base import Base

class FetchSamplesStamps(Base):
    def __init__(self, params={}):
        self.sample_stamp_dao = params['sample_stamp_dao']

    def calculate(self):
        return [self.sample_stamp_dao.all()]
