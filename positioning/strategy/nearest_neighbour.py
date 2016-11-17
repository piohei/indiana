from scipy.spatial.distance import euclidean

from models import APData
from positioning import chains
from positioning.strategy.abstract_location_strategy import AbstractLocationStrategy
from positioning.vectorisation.by_mac_and_rssi import VectorisationByMacAndRssi


class NearestNeighbourStrategy(AbstractLocationStrategy):
    CHAINS = {
        'beta': chains.Beta,
        'permutations': chains.PermutationsChain,
        'consecutive': chains.ConsecutiveChain
    }

    def __init__(self, chain, **kwargs):
        self.vectorisation = self.create_vectorisation(**kwargs)
        if chain not in self.CHAINS.keys():
            raise ValueError("Incompatible chain: {}".format(chain))
        self.chain = self.CHAINS[chain](vectorisation=self.vectorisation, **kwargs)
        self.fingertip_vectors = self.stats = None

    def initialise(self, **kwargs):
        result = self.chain.calculate(**kwargs)
        self.fingertip_vectors = result["fingertip_vectors"]
        self.stats = result["fingertip_stats"]

    def locate(self, measures):
        measures_vector = self.vectorisation.vectorise(measures)
        distances = self.fingertip_vectors.map(euclidean, measures_vector)
        return self.fingertip_vectors.location(distances.argmin())

    @staticmethod
    def create_vectorisation(access_point_dao, **kwargs):
        macs_order = [ap.mac.mac for ap in access_point_dao.active()]
        rssis_order = APData.RSSIS_KEYS
        return VectorisationByMacAndRssi(macs_order, rssis_order)
