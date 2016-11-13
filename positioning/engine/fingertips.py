import numpy as np
from scipy.spatial.distance import euclidean

from models import APData
from models.primitives.rssi import RSSI


class Fingertips(object):
    def __init__(self, ap_macs, fingertip_list):
        vectors = []
        classes = []
        counter = []

        self.order = ap_macs

        for ft in fingertip_list:
            counter.append(len(ft.list))
            for record in ft.list:
                vectors.append(self.vectorise(record))
                classes.append(ft.location)

        self.vectors = np.array(vectors)
        self.classes = np.array(classes)
        self.stats = self.prepare_stats(counter)

    def vectorise(self, measures):
        return np.array([
            measures.get(ap, {}).get(rssi, RSSI(0)).dBm
            for ap in self.order
            for rssi in APData.RSSIS_KEYS
        ])

    def localise(self, measures):
        measures_vector = self.vectorise(measures)
        dists = np.array([euclidean(v, measures_vector) for v in self.vectors])
        return self.classes[dists.argmin()]

    def prepare_stats(self, counter):
        np_counter = np.array(counter)
        return {
            "locations": len(counter),
            "all": np_counter.sum(),
            'min': np_counter.min(),
            'max': np_counter.max(),
            'avg': np_counter.mean()
        }

