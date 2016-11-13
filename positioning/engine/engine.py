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
        self.access_point_dao = kwargs["access_point_dao"]
        if chain not in self.CHAINS.keys():
            raise EngineException("Unknown chain: {}".format(chain))
        self.chain = self.CHAINS[chain](**kwargs)
        self.fingertips = None
        self.specs = (chain, '1-nn')

    def calculate(self, **kwargs):
        return self.chain.calculate(**kwargs)

    def initialise(self, **kwargs):
        ap_macs_ordered = [ap.mac.mac for ap in self.access_point_dao.active()]
        fingertips_list = self.calculate(**kwargs)["fingertips"]
        self.fingertips = Fingertips(ap_macs_ordered, fingertips_list)

    def localise(self, measures):
        return self.fingertips.localise(measures)
