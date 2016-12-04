import positioning.links.fetch as fetch
import positioning.links.transform as transform
from positioning.chains.base import Base


class FullLinRegDataChain(Base):
    def links(self):
        return [
            fetch.FetchSamplesStamps,
            transform.ToFullSamples,
            transform.ToLinRegData
        ]