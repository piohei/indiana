import random
from collections import defaultdict

from models import Sample
from positioning.links import Base



class RandomNForEachAPInSample(Base):
    N = "nOfRandApData"
    def __init__(self, params={}):
        self.n = int(params[self.N])

    def filter(self, sample):
        if self.n > 0:
            grouped = {}
            for mac, ap_datas in sample.ap_data_by_mac_and_signal.items():
                grouped[mac] = random.sample(ap_datas, self.n)
            return Sample(sample.stamp, grouped)
        else:
            return sample

    def calculate(self, samples):
        return [list(map(self.filter, samples))]
