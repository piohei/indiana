from positioning.chains.base import Base

import positioning.links.fetch as fetch
import positioning.links.collect as collect
import positioning.links.transform as transform

class Beta(Base):
    def links(self):
        return [
            fetch.FetchSamplesStamps,
            transform.ToFullSamples,
            collect.AverageRssis
        ]
