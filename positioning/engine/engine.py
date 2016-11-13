# -*- coding: utf-8 -*-

import positioning.chains as chains
from positioning.engine.fingertips import Fingertips


class EngineException(Exception):
    def __init__(self, message):
        self.message = message


class Engine(object):
    CHAINS = {
        'beta': chains.Beta,
        'permutations': chains.PermutationsChain
    }

    def __init__(self, chain='alpha', **kwargs):
        if chain not in self.CHAINS.keys():
            raise EngineException("Unknown chain: {}".format(chain))
        self.chain = self.CHAINS[chain](**kwargs)
        self.fingertips = None
        self.specs = (chain, '1-nn')

    def calculate(self, *args):
        return self.chain.calculate(*args)

    def initialise(self, *args):
        self.fingertips = Fingertips(self.calculate(*args)[0])

    def localise(self, measures):
        return self.fingertips.localise(measures)
