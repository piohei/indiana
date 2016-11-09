from positioning.links.base import Base

import math

class BestMatchAlpha(Base):
    def __init__(self, params={}):
        self.measures = params['measures']

    def calculate(self, samples):
        best_sample = samples[0]
        best_error = float("inf")


        for sample in samples:
            err = 0
            for mac in self.measures.keys():
                for signal in self.measures[mac].keys():
                    if len(self.measures[mac][signal]) == 0:
                        continue
                    diff = sample.get_measure_for(mac, signal)["1"]["avg"].dBm - self.measures[mac][signal]["1"]["avg"].dBm
                    err += pow(diff, 2)

            if err < best_error:
                best_sample = sample
                best_error = err

        return best_sample.location()


