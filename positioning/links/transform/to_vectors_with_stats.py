import numpy as np

from positioning.entities.fingertip_vectors import FingertipVectors
from positioning.links import Base


class ToVectorsWithStats(Base):
    def __init__(self, vectorisation, **kwargs):
        self.vectorisation = vectorisation

    def calculate(self, fingertips, **kwargs):
        fingertip_vectors = []
        locations = []
        counter = []

        for ft in fingertips:
            counter.append(len(ft.list))
            for record in ft.list:
                fingertip_vectors.append(self.vectorise(record))
                locations.append(ft.location)

        stats = self.prepare_stats(counter)
        matrix = FingertipVectors(fingertip_vectors, locations)

        return {"fingertip_vectors": matrix, "fingertip_stats": stats}

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

