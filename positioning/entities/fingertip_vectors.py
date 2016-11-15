import numpy as np


class FingertipVectors(object):
    def __init__(self, fingertips, locations):
        self.locations = np.array(locations)
        self.fingertips = np.array(fingertips)

    def map(self, fun, *args):
        return np.array([fun(item, *args) for item in self.fingertips])

    def location(self, idx):
        return self.locations[idx]
