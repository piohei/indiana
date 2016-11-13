from positioning.chains.base import Base

import positioning.links as links
import positioning.links.collect as collect

class Beta(Base):
    def links(self):
        return [
            links.FetchSamplesStamps,
            links.ToFullSamples,
            collect.AverageRssis
        ]
