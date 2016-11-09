import random
from collections import defaultdict

from positioning.links.base import Base

from models.sample import Sample

LIMIT = 2


class ToFullSamples(Base):
    def __init__(self, params={}):
        self.ap_data_dao = params['ap_data_dao']

    def to_sample(self, stamp):
        ap_datas = self.ap_data_dao.get_for_time_range(stamp.start_time, stamp.end_time, asc=False)
        grouped = defaultdict(list)
        for ap_data in ap_datas:
            l = grouped[ap_data.router_mac.mac]
            if len(l) < LIMIT:
                l.append(ap_data)
        return Sample(stamp, grouped)

    def calculate(self, stamps):
        return [list(map(self.to_sample, stamps))]
