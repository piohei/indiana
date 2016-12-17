import itertools

from positioning.entities import Fingerprint
from positioning.links.collect.collector import Collector


class TimeRelated(Collector):
    def to_fingerprint(self, sample):
        joined = itertools.chain(*list(sample.ap_data_by_mac.values()))
        ordered = sorted(joined, key=lambda apd: apd.created_at.millis, reverse=True)
        aps_number = len(sample.ap_data_by_mac)
        fingerprints = []
        current = {}
        for apd in ordered:
            if apd.router_mac.mac not in current:
                current[apd.router_mac.mac] = apd.rssis
                if len(current) == aps_number:
                    fingerprints.append(current)
                    current = {}
        return Fingerprint(sample.location(), fingerprints)
