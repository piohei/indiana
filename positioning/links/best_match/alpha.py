from positioning.links.base import Base

import math

class BestMatchAlpha(Base):
    def __init__(self, params={}):
        self.measures = params['measures']

    def calculate(self, samples):
        best_sample = samples[0]
        best_error = math.inf

        for sample in samples:
            err = 0
            for band in self.measures.keys():
                for mac in self.measures[band].keys():
                    if not self.measures[band][mac]["rssi1"]:
                        continue
                    diff = sample.get_measure_for(2, mac)["rssi1"]["avg"] - self.measures[band][mac]["rssi1"]
                    err += pow(diff, 2)

            if err < best_error:
                best_sample = sample
                best_error = err

        return best_sample.location()


