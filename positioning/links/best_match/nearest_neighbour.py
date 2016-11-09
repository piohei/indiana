from positioning.links.base import Base

import math

from positioning.links.fingertips import Fingertips


class NN(Base):
    def __init__(self, params={}):
        self.measures = params['measures']

    def calculate(self, fingertip_list):
        fingertips = Fingertips(fingertip_list)

        return fingertips.localise(self.measures)




