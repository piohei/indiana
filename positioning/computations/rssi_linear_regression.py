from collections import defaultdict

import numpy as np
import sklearn.linear_model as sk


class RssiLinearRegression(object):
    def __init__(self):
        self.As = defaultdict(dict)
        self.ns = defaultdict(dict)

    def fit_one(self, lin_reg_datas):
        linreg = sk.LinearRegression()
        dists = np.array([lrd.distance_from_ap for lrd in lin_reg_datas])
        rssis = np.array([lrd.dbms for lrd in lin_reg_datas])
        log_dists = np.log10(dists)
        xs = log_dists * (-10)
        linreg.fit(xs.reshape(-1, 1), rssis)
        return linreg.coef_[0], linreg.intercept_

    def fit(self, lin_reg_datas):
        for mac, rssi_datas in lin_reg_datas.items():
            for rssi, datas in rssi_datas.items():
                n, A = self.fit_one(datas)
                self.As[mac][rssi] = A
                self.ns[mac][rssi] = n

    def predict(self, measures):
        dists = defaultdict(list)
        for mac, rssis in measures.items():
            for key, rssi in rssis.items():
                if self.has_data_for(mac, key):
                    prediction = self.predict_one(mac, key, rssi.dBm)
                    if prediction**2 < 12.5**2 + 33**2:
                        dists[mac].append(prediction)
        res = {}
        for mac, dists_list in dists.items():
            res[mac] = np.array(dists_list).mean()
        return res

    def predict_one(self, mac, rssi, dbms):
        A = self.As[mac][rssi]
        n = self.ns[mac][rssi]
        exponent = (dbms - A)/(-10*n)
        return np.power(10, exponent)

    def has_data_for(self, mac, rssi):
        return mac in self.As and rssi in self.As[mac]



