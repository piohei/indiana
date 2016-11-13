from positioning.links.base import Base

class FetchSamplesStamps(Base):
    def __init__(self, sample_stamp_dao, **kwargs):
        self.sample_stamp_dao = sample_stamp_dao

    def calculate(self):
        return {"sample_stamps": self.sample_stamp_dao.all()}
