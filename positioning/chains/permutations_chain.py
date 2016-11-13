from positioning.chains.base import Base

import positioning.links.fetch as fetch
import positioning.links.filter as filter
import positioning.links.collect as collect
import positioning.links.transform as transform


class PermutationsChain(Base):
    def links(self):
        return [
            fetch.FetchSamplesStamps,
            transform.ToFullSamples,
            filter.RandomNForEachAPInSample,
            collect.Permutations
        ]
