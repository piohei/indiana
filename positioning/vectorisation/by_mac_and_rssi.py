import numpy as np

from models.primitives.rssi import RSSI


class VectorisationByMacAndRssi(object):
    def __init__(self, macs_order, rssi_order):
        self.rssi_order = rssi_order
        self.macs_order = macs_order

    def vectorise(self, measures):
        return np.array([self.scalarise(measures, ap, rssi)
                         for ap in self.macs_order
                         for rssi in self.rssi_order])

    def scalarise(self, measures, mac, rssi):
        return measures.get(mac, {}).get(rssi, RSSI(0)).dBm
