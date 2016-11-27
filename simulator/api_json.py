import requests

from config import config
from helpers.utils import raw_mac
from models import Time


class ApiJSON(object):
    API_URL = config["ap_data"]["host"] + ":" + config["ap_data"]["port"] + str(config["ap_data"]["endpoint"])

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
            self.__dict__["data"][0]["rss" + n] = v

    def __getattr__(self, item):
        return self.__dict__[item]

    def send(self):
        self.time = Time().millis
        res = requests.post(self.API_URL, json=self.__dict__)
        return res.status_code