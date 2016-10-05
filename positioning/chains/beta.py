from positioning.chains.base import Base

import positioning.links as links


class Beta(Base):
    def links(self):
        return [
            links.FetchSamplesStamps,
            links.AddRSSIStatsToSamples,
            links.BestMatchAlpha
        ]
