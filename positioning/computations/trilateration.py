import numpy as np
from scipy.optimize import *

from models import Location


class Trilateration(object):
    def locate(self, dists, positions, start_pos=(3, 5)):
        pos_mtrx, dists_squared = self.matrices(dists, positions)
        size = len(dists_squared)
        start_pos = np.array(start_pos)

        def fun(xs):
            xys = np.array([[xs[0], xs[1], -2]] * size)
            dif = pos_mtrx - xys
            squared_sum = np.square(dif).sum(1)
            return np.abs((squared_sum - dists_squared)).sum()

        res = minimize(fun, start_pos, bounds=[(0, 33), (0, 12)])
        print(res)
        return Location(float(res.x[0]), float(res.x[1]), -2.0)

    def matrices(self, dists, positions):
        dists_squared = []
        positions_mtrx = []
        for mac, dist in dists.items():
            dists_squared.append(dist**2)
            location = positions[mac]
            positions_mtrx.append([location.x, location.y, location.z])
        return np.array(positions_mtrx), np.array(dists_squared)

