import random

from positioning.entities import Sample
from positioning.links import Base


class RandomNForEachAPInSample(Base):
    def __init__(self, n_of_random_ap_data_from_each_ap, **kwargs):
        self.n = int(n_of_random_ap_data_from_each_ap)

    def filter(self, sample):
        if self.n > 0:
            grouped = {mac: random.sample(ap_datas, min(self.n, len(ap_datas)))
                       for mac, ap_datas in sample.ap_data_by_mac.items()}
            return Sample(sample.stamp, grouped)
        else:
            return sample

    def calculate(self, samples, **kwargs):
        return {"samples": list(map(self.filter, samples))}
