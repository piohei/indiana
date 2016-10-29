from positioning.links.base import Base

from collections import defaultdict

from helpers.utils import functional_add
from models.fingertip import Fingertip


class Permutations(Base):

    def permutate(self, source_dict, keys_left):
        if not keys_left:
            return [{}]
        else:
            ap_mac, *tail = keys_left
            partial_results = self.permutate(source_dict, tail)
            rssis = source_dict[ap_mac]
            return [
                (functional_add(ap_mac, rssi.to_rssi_measure(), partial)
                for rssi in rssis)
                for partial in partial_results
            ]

    def permutations_for_macs(self, macs_to_rssis):
        return self.permutate(macs_to_rssis, macs_to_rssis.keys())

    def calculate(self, samples):
        return [
            Fingertip(
                sample.location(),
                {
                    signal: self.permutations_for_macs(macs_to_rssis)
                    for signal, macs_to_rssis in sample.ap_data_by_mac_and_signal.items()
                }
            ) for sample in samples
        ]


