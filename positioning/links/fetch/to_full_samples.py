from positioning.links.base import Base

from models.sample import Sample


class ToFullSamples(Base):
    def __init__(self, params={}):
        self.rssi_measure_dao = params['rssi_measure_dao']

    def to_sample(self, stamp):
        measures = self.rssi_measure_dao.grouped_timed_measures_for_range(
                start_time=stamp.start_time,
                end_time=stamp.end_time
        )
        return Sample(stamp, measures)

    def calculate(self, stamps):
        return [list(map(self.to_sample, stamps))]
