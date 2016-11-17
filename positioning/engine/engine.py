# -*- coding: utf-8 -*-

from positioning.strategy.full_linear_regression import FullLinearRegressionStrategy


class Engine(object):
    def __init__(self, **kwargs):
        self.strategy = FullLinearRegressionStrategy(**kwargs)
        # self.strategy = NearestNeighbourStrategy(**kwargs)

    def initialise(self, **kwargs):
        self.strategy.initialise(**kwargs)

    def localise(self, measures):
        return self.strategy.localise(measures)

    def stats(self):
        return self.strategy.stats
