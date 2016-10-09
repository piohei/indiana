from positioning.links.base import Base

from models.sample import Sample


class AddRSSIStatsToSamples(Base):
    def __init__(self, params={}):
        self.ap_data_dao = params['ap_data_dao']

    def to_sample(self, stamp):
        measures = self.ap_data_dao.stats_group_by_mac_and_signal_for_range(
                start_time=stamp.start_time,
                end_time=stamp.end_time
        )
        return Sample(stamp, measures)

    def calculate(self, stamps):
        return [list(map(self.to_sample, stamps))]
