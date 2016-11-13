from positioning.chains.base import Base

import positioning.links as links
import positioning.links.filter.random_n_for_each_ap as filter


class PermutationsChain(Base):
    def links(self):
        return [
            links.FetchSamplesStamps,
            links.ToFullSamples,
            filter.RandomNForEachAPInSample,
            links.Permutations
        ]
