from collections import defaultdict

from positioning.entities.lin_reg_data import LinRegData
from positioning.links import Base


class ToLinRegData(Base):
    def __init__(self, access_point_dao, **kwargs):
        self.active_aps_locations = {ap.mac.mac: ap.location for ap in access_point_dao.active()}

    def to_lin_reg_datas(self, ap_mac, ap_datas, sample):
        res = {}
        ap_location = self.active_aps_locations[ap_mac]
        distance_from_ap = ap_location.distnace_from(sample.location())
        return [LinRegData(distance_from_ap, ap_data.rssis) for ap_data in ap_datas]

    def calculate(self, samples, **kwargs):
        lin_reg_datas = defaultdict(lambda: defaultdict(list))
        for sample in samples:
            for ap_mac, ap_datas in sample.ap_data_by_mac.items():
                ap_location = self.active_aps_locations[ap_mac]
                distance_from_ap = ap_location.distnace_from(sample.location())
                for ap_data in ap_datas:
                    for rssi in ap_data.rssis:
                        lin_reg_datas[ap_mac][rssi].append(LinRegData(distance_from_ap, ap_data.rssis[rssi].dBm))

        return {"lin_reg_datas": lin_reg_datas}

