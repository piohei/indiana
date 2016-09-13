# -*- coding: utf-8 -*-

import positioning.chains as chains


class EngineException(Exception):
    def __init__(self, message):
        self.message = message


class Engine:
    CHAINS = {
      'alpha': chains.Alpha(),
    }

    def __init__(self, chain=None):
        self.chain = chain if chain is not None else 'alpha'

        if self.chain not in self.CHAINS.keys():
            raise EngineException("Unknown chain: {}".format(self.chain))

    def calculate(self, *args):
        return self.CHAINS[self.chain].calculate(*args)
