from models import Time
from simulator.api_json import ApiJSON
from simulator.simulator_step import SimulatorStep


class SimpleSimulator(object):
    def __init__(self, steps):
        self.sent = 0
        self.steps = steps

    @classmethod
    def create(cls, ap_datas):
        jsons = list(map(ApiJSON, ap_datas))
        intervals = cls.create_intervals(jsons)
        return cls(map(SimulatorStep, zip(jsons, intervals)))

    @classmethod
    def create_intervals(cls, jsons):
        times = [item.time for item in jsons]
        next_times = times[1:] + times[-1]
        return list(map(lambda t: t[1] - t[0], zip(times, next_times)))

    def run(self):
        start = Time()
        for step in self.steps:
            result = step.simulate_step()
            if result == 200:
                self.sent += 1
            else:
                print("error " + result)
        end = Time()
        print("simulator sent {} jsons successfully".format(self.sent))
        return start.millis, end.millis
