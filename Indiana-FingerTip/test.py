import requests

from utils import millis


def create_ap_data():
    return {
        "data": {
            "rss1": -64,
            "rss2": -61,
            "rss3": -69,
            "clientMac": "DCEE0661B03D"
        },
        "time": millis(),
        "band": 2,
        "apMac": "F8E71E290500"
    }


def send_ap_data():
    response = requests.post("http://127.0.0.1:8887", json=create_ap_data())
    print("{}:{}".format(response.status_code, response.json()))


