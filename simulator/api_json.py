import requests

from config import config
from models import Time, Mac


class ApiJSON(object):
    API_URL = config["ap_data"]["host"] + ":" + str(config["ap_data"]["port"]) + str(config["ap_data"]["endpoint"])

    def __init__(self, db_obj, mac=None):
        self.__dict__.update({
            "data": [
                {
                    "clientMac": Mac.raw(db_obj["device_mac"] if mac is None else mac)
                }
            ],
            "apMac": Mac.raw(db_obj["router_mac"]),
            "time": db_obj["created_at"],
            "band": db_obj["signal"]["channel"]
        })

        for n, v in db_obj["rssis"].items():
            self.__dict__["data"][0]["rss" + n] = v

    def __getattr__(self, item):
        return self.__dict__[item]

    def send(self):
        self.time = Time().millis
        res = requests.post(self.API_URL, json=self.__dict__)
        return res.status_code