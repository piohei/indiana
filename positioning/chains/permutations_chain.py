from positioning.links.permutations import Permutations
from positioning.links.fetch.fetch_sample_stamps import FetchSamplesStamps
from positioning.links.fetch.to_full_samples import ToFullSamples


class PermutationsChain(object):
    def __init__(self, sample_stamp_dao, rssi_measures_dao):
        self.rssi_measures_dao = rssi_measures_dao
        self.sample_stamp_dao = sample_stamp_dao

    def calculate(self):
        stamps = FetchSamplesStamps(self.sample_stamp_dao).calculate()
        samples = ToFullSamples(self.rssi_measures_dao).calculate(stamps)
        return Permutations().calculate(samples)
