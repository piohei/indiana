import numpy as np

from models import Fingertip, RSSI, APData
from positioning.links.collect.collector import Collector


class AverageRssis(Collector):
    def to_fingertip(self, sample):
        averages = self.get_averages(sample.ap_data_by_mac)
        return Fingertip(sample.location(), [averages])

    def get_averages(self, ap_data_by_mac):
        return {mac: self.to_avg_ap_data_rssis(ap_datas)
                for mac, ap_datas in ap_data_by_mac.items()}

    def to_avg_ap_data_rssis(self, ap_datas):
        rssis = {}
        for rssi in APData.RSSIS_KEYS:
            values = self.to_present_rssi_dbms(ap_datas, rssi)
            if len(values) > 0:
                rssis[rssi] = RSSI(float(np.array(values).mean()))
        return rssis

    def to_present_rssi_dbms(self, ap_datas, rssi):
        return [ap_data.rssis[rssi].dBm for ap_data in ap_datas if rssi in ap_data.rssis]
