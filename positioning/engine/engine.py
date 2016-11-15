# -*- coding: utf-8 -*-

from positioning.strategy.nearest_neighbour import NearestNeighbourStrategy


class Engine(object):
    def __init__(self, **kwargs):
        self.strategy = NearestNeighbourStrategy(**kwargs)

    def initialise(self, **kwargs):
        self.strategy.initialise(**kwargs)

    def localise(self, measures):
        return self.strategy.localise(measures)

    def stats(self):
        return self.strategy.stats
