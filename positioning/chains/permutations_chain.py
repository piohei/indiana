from positioning.chains.base import Base

import positioning.links as links


class PermutationsChain(Base):
    def links(self):
        return [
            links.FetchSamplesStamps,
            links.ToFullSamples,
            links.Permutations
        ]
