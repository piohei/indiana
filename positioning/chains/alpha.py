# -*- coding: utf-8 -*-
from positioning.chains.base import Base

import positioning.links as links


class Alpha(Base):
    def links(self):
        return [
          links.PassArgs,
          links.PassArgs
        ]
