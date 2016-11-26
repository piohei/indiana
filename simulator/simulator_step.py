from time import sleep


class SimulatorStep(object):
    def __init__(self, tup):
        api_json, break_millis = tup
        self.break_millis = break_millis
        self.api_json = api_json

    def simulate_step(self):
        res = self.api_json.send()
        sleep(self.break_millis / 1000)
        return res