from positioning.entities import Fingerprint
from positioning.links.collect.collector import Collector


class Permutations(Collector):
    def permutate(self, source_dict, keys_left):
        if not keys_left:
            return [{}]
        else:
            ap_mac, *tail = keys_left
            partial_results = self.permutate(source_dict, tail)
            apdatas = source_dict[ap_mac]
            return [
                self.functional_add(ap_mac, apdata.rssis, partial)
                for apdata in apdatas
                for partial in partial_results
                ]

    def permutations_for_macs(self, macs_to_rssis):
        return self.permutate(macs_to_rssis, macs_to_rssis.keys())

    def to_fingerprint(self, sample):
        permutations = self.permutations_for_macs(sample.ap_data_by_mac)
        return Fingerprint(sample.location(), permutations)

    @staticmethod
    def functional_add(key, value, dictionary):
        new = dict(dictionary)
        new[key] = value
        return new