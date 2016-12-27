import requests

from config import config
from models import Time, Mac


class ApiJSON(object):
    AP_DATA_LISTENER_IDX = config["simulator"]["ap_data_listener_index"]
    HOST = config["ap_data"][AP_DATA_LISTENER_IDX]["host"]
    PORT = str(config["ap_data"][AP_DATA_LISTENER_IDX]["port"])
    ENDPOINT = str(config["ap_data"][AP_DATA_LISTENER_IDX]["endpoint"])
    API_URL = HOST + ":" + PORT + ENDPOINT

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