# -*- coding: utf-8 -*-

import positioning.chains as chains


class EngineException(Exception):
    def __init__(self, message):
        self.message = message


class Engine:
    CHAINS = {
        'alpha': chains.Alpha,
        'permutations': chains.PermutationsChain
    }

    def __init__(self, sample_stamp_dao, rssi_measures_dao, chain=None):
        self.rssi_measures_dao = rssi_measures_dao
        self.sample_stamp_dao = sample_stamp_dao
        chain_id = chain if chain is not None else 'alpha'

        if chain_id not in self.CHAINS.keys():
            raise EngineException("Unknown chain: {}".format(chain_id))
        self.chain = self.CHAINS[chain_id](sample_stamp_dao, rssi_measures_dao)

    def calculate(self, *args):
        return self.CHAINS[self.chain]().calculate(*args)
