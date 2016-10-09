from positioning.links.base import Base

from models.sample import Sample


class ToFullSamples(Base):
    def __init__(self, params={}):
        self.ap_data_dao = params['ap_data_dao']

    def to_sample(self, stamp):
        grouped = self.ap_data_dao.group_by_mac_and_signal_for_range(
                start_time=stamp.start_time,
                end_time=stamp.end_time
        )
        return Sample(stamp, grouped)

    def calculate(self, stamps):
        return [list(map(self.to_sample, stamps))]
