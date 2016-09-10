# -*- coding: utf-8 -*-

import chaines

class EngineException(Exception):
    def __init__(self, message):
        self.message = message
        
class Engine:
    CHAINES = {
      'alpha': chaines.Alpha(),
    }

    def __init__(self, chain=None):
        self.chain = chain if chain is not None else 'alpha'

        if self.chain not in self.CHAINES.keys():
            raise EngineException("Uknown chain: {}".format(self.chain))

    def calculate(self, *args):
        return self.CHAINES[self.chain].calculate(*args)
