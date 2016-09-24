from positioning.chains.base import Base

from positioning.links.permutations import Permutations
from positioning.links.fetch.fetch_sample_stamps import FetchSamplesStamps
from positioning.links.fetch.to_full_samples import ToFullSamples


class PermutationsChain(Base):
    def links(self):
        return [
            FetchSamplesStamps,
            ToFullSamples,
            Permutations
        ]
