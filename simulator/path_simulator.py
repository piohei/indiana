import requests
from time import sleep
from itertools import cycle
from sys import argv

from helpers.utils import raw_mac
from models.primitives.time import Time
from config import config
from db import PathDAO


class ApiJSON(object):
    API_URL = config["ap_data"]["endpoint"]

    def __init__(self, db_obj):
        self.__dict__.update({
            "data": [
                {
                    "clientMac": raw_mac(db_obj["device_mac"])
                }
            ],
            "apMac": raw_mac(db_obj["router_mac"]),
            "time": db_obj["created_at"],
            "band": db_obj["signal"]["channel"]
        })

        for n, v in db_obj["rssis"].items():
            self.__dict__["data"]["rss" + n] = v

    def __getattr__(self, item):
        return self.__dict__[item]

    def send(self):
        self.time = Time().millis
        requests.post(self.API_URL, json=self.__dict__)


class SimulatorPathStep(object):
    def __init__(self, api_json, break_millis):
        self.break_millis = break_millis
        self.api_json = api_json

    def simulate_step(self):
        self.api_json.send()
        sleep(self.break_millis / 1000)
        

class SimulatorPath(object):
    def __init__(self, steps):
        self.steps = steps

    @classmethod
    def create(cls, api_jsons):
        there_and_back_again = cls.create_returning(api_jsons)
        intervals = cls.count_intervals(there_and_back_again)
        return cls(list(map(SimulatorPathStep, zip(there_and_back_again, intervals))))

    @classmethod
    def create_returning(cls, api_jsons):
        return api_jsons + api_jsons[-2:0:-1]

    @classmethod
    def count_intervals(cls, path):
        return list(map(lambda a, b: abs(a-b),  zip(path, reversed(path))))

    def run_cycled(self):
        for step in cycle(self.steps):
            step.simulate_step()


class Simulator(object):
    def __init__(self, collection_name, path_dao):
        self.path_name = collection_name
        self.path_dao = path_dao
        self.path = self.prepare()

    def fetch(self):
        return self.path_dao.fetch_path(self.path_name)

    def prepare(self):
        return SimulatorPath.create(self.fetch())

    def run(self):
        self.path.run_cycled()


if __name__ == '__main__':
    Simulator(PathDAO(), argv[1]).run()



