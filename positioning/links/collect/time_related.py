import itertools

from positioning.entities import Fingertip
from positioning.links.collect.collector import Collector


class TimeRelated(Collector):
    def to_fingertip(self, sample):
        joined = itertools.chain(*list(sample.ap_data_by_mac.values()))
        ordered = sorted(joined, key=lambda apd: apd.created_at.millis, reverse=True)
        aps_number = len(sample.ap_data_by_mac)
        fingertips = []
        current = {}
        for apd in ordered:
            if apd.router_mac.mac not in current:
                current[apd.router_mac.mac] = apd.rssis
                if len(current) == aps_number:
                    fingertips.append(current)
                    current = {}
        return Fingertip(sample.location(), fingertips)
