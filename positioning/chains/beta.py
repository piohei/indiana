import positioning.links.collect as collect
import positioning.links.fetch as fetch
import positioning.links.transform as transform
from positioning.chains.base import Base


class Beta(Base):
    def links(self):
        return [
            fetch.FetchSamplesStamps,
            transform.ToFullSamples,
            collect.AverageRssis,
            transform.ToVectorsWithStats
        ]
