# -*- coding: utf-8 -*-
from positioning.chains.base import Base
from positioning.links.pass_args import PassArgs


class Alpha(Base):
    def links(self):
        return [
          PassArgs,
          PassArgs
        ]
