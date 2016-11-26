from itertools import cycle
from sys import argv

from db import PathDAO
from simulator.api_json import ApiJSON
from simulator.simulator_step import SimulatorStep


class SimulatorCycledPath(object):
    def __init__(self, steps):
        self.sent = 0
        self.steps = steps

    @classmethod
    def create(cls, jsons):
        there_and_back_again = cls.create_returning(jsons)
        intervals = cls.count_intervals(there_and_back_again)
        return cls(list(map(SimulatorStep, zip(there_and_back_again, intervals))))

    @classmethod
    def create_returning(cls, jsons):
        api_jsons = list(map(ApiJSON, jsons))
        return api_jsons + api_jsons[-2:0:-1]

    @classmethod
    def count_intervals(cls, path):
        times = [item.time for item in path]
        return list(map(lambda t: abs(t[1] - t[0])/20,  zip(times, reversed(times))))

    def run_cycled(self):
        for step in cycle(self.steps):
            result = step.simulate_step()
            if result == 200:
                self.sent += 1
                print(self.sent)
            else:
                print("error " + result)


class CycledPathSimulator(object):
    def __init__(self, collection_name, path_dao):
        self.path_name = collection_name
        self.path_dao = path_dao
        self.path = self.prepare()
        print(ApiJSON.API_URL)

    def fetch(self):
        return self.path_dao.fetch_path(self.path_name)

    def prepare(self):
        return SimulatorCycledPath.create(self.fetch())

    def run(self):
        self.path.run_cycled()


if __name__ == '__main__':
    CycledPathSimulator(argv[1], PathDAO()).run()



