import numpy as np


class FingerprintData(object):
    def __init__(self, fingerprints, locations):
        self.locations = np.array(locations)
        self.fingerprints = np.array(fingerprints)

    def map(self, fun, *args):
        return np.array([fun(item, *args) for item in self.fingerprints])

    def location(self, idx):
        return self.locations[idx]
