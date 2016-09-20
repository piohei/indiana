class FetchLocationSamples(object):
    def __init__(self, sample_stamp_dao):
        self.sample_stamp_dao = sample_stamp_dao

    def calculate(self):
        return self.sample_stamp_dao.all()
