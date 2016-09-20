from models.sample import Sample


class ToFullSamples(object):
    def __init__(self, rssi_measure_dao):
        self.rssi_measure_dao = rssi_measure_dao

    def to_sample(self, stamp):
        measures = self.rssi_measure_dao.grouped_time_measures_for_range(
                start_time=stamp.start_time,
                end_time=stamp.end_time
        )
        return Sample(stamp, measures)

    def calculate(self, stamps):
        return list(map(self.to_sample, stamps))
