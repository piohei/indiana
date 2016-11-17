from positioning.chains import LocalLinRegDataChain
from positioning.computations.rssi_linear_regression import RssiLinearRegression
from positioning.computations.trilateration import Trilateration
from positioning.strategy import NearestNeighbourStrategy
from positioning.strategy.abstract_location_strategy import AbstractLocationStrategy


class NnWithLinearRegressionStrategy(AbstractLocationStrategy):
    def __init__(self, **kwargs):
        self.access_point_dao = kwargs["access_point_dao"]
        self.locations = {ap.mac.mac: ap.location for ap in self.access_point_dao.active()}
        self.linregs_per_location = None
        self.lin_reg_chain = LocalLinRegDataChain(**kwargs)
        self.trilateration = Trilateration()
        self.nn_strategy = NearestNeighbourStrategy(**kwargs)

    def initialise(self, **kwargs):
        self.nn_strategy.initialise(**kwargs)
        lin_reg_datas_per_location = self.lin_reg_chain.calculate(**kwargs)["lin_reg_data_per_location"]
        self.linregs_per_location = {}
        for loc_str, lin_reg_datas in lin_reg_datas_per_location.items():
            reg = RssiLinearRegression()
            reg.fit(lin_reg_datas)
            self.linregs_per_location[loc_str] = reg

    def locate(self, measures):
        loc = self.nn_strategy.locate(measures)
        dists = self.linregs_per_location[str(loc)].predict(measures)
        sorted_dists = list(sorted(dists.items(), key=lambda t: t[1]))
        closest = dict(sorted_dists[:min(100, len(sorted_dists))])
        return self.trilateration.locate(closest, self.locations)