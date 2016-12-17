import numpy as np

from positioning.entities.fingerprint_data import FingerprintData
from positioning.links import Base


class ToVectorsWithStats(Base):
    def __init__(self, vectorisation, **kwargs):
        self.vectorisation = vectorisation

    def calculate(self, fingerprints, **kwargs):
        fingerprint_vectors = []
        locations = []
        counter = []

        for ft in fingerprints:
            counter.append(len(ft.list))
            for record in ft.list:
                fingerprint_vectors.append(self.vectorise(record))
                locations.append(ft.location)

        stats = self.prepare_stats(counter)
        matrix = FingerprintData(fingerprint_vectors, locations)

        return {"fingerprint_data": matrix, "fingerprint_stats": stats}

    def vectorise(self, record):
        return self.vectorisation.vectorise(record)

    @staticmethod
    def prepare_stats(counter):
        np_counter = np.array(counter)
        return {
            "locations": len(counter),
            "all": np_counter.sum(),
            'min': np_counter.min(),
            'max': np_counter.max(),
            'avg': np_counter.mean()
        }

