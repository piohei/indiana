class Sample(object):
    def __init__(self, stamp, ap_data_by_band_and_mac):
        self.ap_data_by_band_and_mac = ap_data_by_band_and_mac
        self.stamp = stamp

    def get_measure_for(self, band, mac):
        return self.ap_data_by_band_and_mac[band][mac]

    def location(self):
        return self.stamp.location
