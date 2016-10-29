# -*- coding: utf-8 -*-
from positioning.links.base import Base

class PassArgs(Base):
    def calculate(self, *args):
        return args
