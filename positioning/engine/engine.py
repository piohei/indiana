# -*- coding: utf-8 -*-

import positioning.chains as chains


class EngineException(Exception):
    def __init__(self, message):
        self.message = message


class Engine(object):
    CHAINS = {
        'alpha': chains.Alpha,
        'permutations': chains.PermutationsChain
    }

    def __init__(self, chain='alpha', params={}):
        if chain not in self.CHAINS.keys():
            raise EngineException("Unknown chain: {}".format(chain))
        self.chain = self.CHAINS[chain](params)

    def calculate(self, *args):
        return self.chain.calculate(*args)
