# -*- coding: utf-8 -*-
from positioning.strategy import FullLinearRegressionStrategy, NearestNeighbourStrategy, NnWithLinearRegressionStrategy


class Engine(object):
    STRATEGIES = {
        "FullLinearRegression": FullLinearRegressionStrategy,
        "1-NN": NearestNeighbourStrategy,
        "1-NNWithLinearRegression": NnWithLinearRegressionStrategy
    }

    def __init__(self, strategy, daos,  strategy_config=()):
        config_dict = dict(strategy_config)
        if strategy not in self.STRATEGIES:
            raise ValueError("strategy '{}' not recognised".format(strategy))
        kwargs = daos.copy()
        kwargs.update(config_dict)
        self.specs = {"strategy": strategy, "config": config_dict}
        self.strategy = self.STRATEGIES[strategy](**kwargs)

    def initialise(self, **kwargs):
        self.strategy.initialise(**kwargs)

    def locate(self, measures):
        return self.strategy.locate(measures)

    def stats(self):
        return self.strategy.stats
