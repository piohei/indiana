import numpy as np
from scipy.spatial.distance import euclidean

from models.primitives.rssi import RSSI


class Fingertips(object):
    def __init__(self, fingertip_list):
        vectors = []
        classes = []

        ap_macs = list(sorted(fingertip_list[0].list[0].keys()))
        self.order = ap_macs

        for ft in fingertip_list:
            for record in ft.list:
                vectors.append(self.vectorise(record))
                classes.append(ft.location)

        self.vectors = np.array(vectors)
        self.classes = np.array(classes)

    def vectorise(self, measures):
        return np.array([
            measures.get(ap, {}).get(rssi, RSSI(0)).dBm
            for ap in self.order
            for rssi in ["1", "2", "3"]
        ])

    def localise(self, measures):
        measures_vector = self.vectorise(measures)
        dists = np.array([euclidean(v, measures_vector) for v in self.vectors])
        return self.classes[dists.argmin()]

