# -*- coding: utf-8 -*-

import positioning.chains as chains


class EngineException(Exception):
    def __init__(self, message):
        self.message = message


class Engine(object):
    CHAINS = {
        'alpha': chains.Alpha,
        'beta': chains.Beta,
        'permutations': chains.PermutationsChain
    }

    def __init__(self, chain='alpha', params={}):
        if chain not in self.CHAINS.keys():
            raise EngineException("Unknown chain: {}".format(chain))
        self.chain = self.CHAINS[chain](params)
        self.fingertips = None
        self.specs = (chain, '1-nn')

    def calculate(self, *args):
        return self.chain.calculate(*args)

    def initialise(self, *args):
        self.fingertips = self.calculate(*args)
