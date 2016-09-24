from positioning.links.base import Base

class FetchSamplesStamps(Base):
    def __init__(self, sample_stamp_dao):
        super
        self.sample_stamp_dao = self.params['sample_stamp_dao']

    def calculate(self):
        return self.sample_stamp_dao.all()
