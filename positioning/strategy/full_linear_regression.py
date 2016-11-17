from positioning.chains import FullLinRegDataChain
from positioning.computations.rssi_linear_regression import RssiLinearRegression
from positioning.computations.trilateration import Trilateration


class FullLinearRegressionStrategy(object):
    def __init__(self, **kwargs):
        self.linreg = RssiLinearRegression()
        self.access_point_dao = kwargs["access_point_dao"]
        self.locations = {ap.mac.mac: ap.location for ap in self.access_point_dao.active()}
        self.chain = FullLinRegDataChain(**kwargs)
        self.As = None
        self.ns = None
        self.trilateration = Trilateration()

    def initialise(self, **kwargs):
        lin_reg_datas = self.chain.calculate(**kwargs)["lin_reg_datas"]
        self.linreg.fit(lin_reg_datas)

    def localise(self, measures):
        dists = self.linreg.predict(measures)
        return self.trilateration.locate(dists, self.locations)
