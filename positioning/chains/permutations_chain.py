import positioning.links.collect as collect
import positioning.links.fetch as fetch
import positioning.links.filter as filter
import positioning.links.transform as transform
from positioning.chains.base import Base


class PermutationsChain(Base):
    def links(self):
        return [
            fetch.FetchSamplesStamps,
            transform.ToFullSamples,
            filter.RandomNForEachAPInSample,
            collect.Permutations,
            transform.ToVectorsWithStats
        ]
