import positioning.links.fetch as fetch
import positioning.links.transform as transform
from positioning.chains.base import Base


class LocalLinRegDataChain(Base):
    def links(self):
        return [
            fetch.FetchSamplesStamps,
            transform.ToFullSamples,
            transform.ToClustersOfNClosestSamples,
            transform.ToLinRegDataPerLocation
        ]