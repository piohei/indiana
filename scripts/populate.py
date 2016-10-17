import datetime
import math

import requests

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Location

n = 1
A = 0


class Device(object):
    def __init__(self, mac, location):
        self.MAC = mac
        self.location = location

class Router(Device):
    def __init__(self, mac, location, channel):
        super().__init__(mac, location)
        self.channel = channel

    @staticmethod
    def count_rssi(d):
        return -10*n*math.log(d, 10) + A

    def get_ap_data(self, device):
        distance = self.location.distnace_from(device.location)
        rssi = self.count_rssi(distance)
        timestamp = datetime.datetime.now().timestamp()
        return APData(device.MAC, self.MAC, timestamp, rssi, self.channel)


base_url = 'http://localhost:8886/'
url = base_url + 'location/'

loc1 = Location(15, 25, 0)
loc2 = Location(20, 28, 0)
loc3 = Location(46, -28, 0)

mac1 = '11:12:13:14:15:16'
mac2 = '11:12:13:14:15:17'
mac3 = '11:12:13:14:15:18'

dev1 = Device(mac1, loc1)
dev2 = Device(mac2, loc2)
dev3 = Device(mac3, loc3)

requests.post(url + mac1, json=loc1.to_dict())
requests.post(url + mac2, json=loc2.to_dict())
requests.post(url + mac3, json=loc3.to_dict())


ap1 = Router("192.168.0.1", Location(10, 10, 0), 4)
ap2 = Router("192.168.0.2", Location(30, 35, 0), 4)
ap3 = Router("192.168.0.3", Location(50, -40, 0), 4)

url = base_url + 'ap_data'

requests.post(url, json=ap1.get_ap_data(dev1).to_dict())
requests.post(url, json=ap1.get_ap_data(dev2).to_dict())
requests.post(url, json=ap1.get_ap_data(dev3).to_dict())
requests.post(url, json=ap2.get_ap_data(dev1).to_dict())
requests.post(url, json=ap2.get_ap_data(dev2).to_dict())
requests.post(url, json=ap2.get_ap_data(dev3).to_dict())
requests.post(url, json=ap3.get_ap_data(dev1).to_dict())
requests.post(url, json=ap3.get_ap_data(dev2).to_dict())
requests.post(url, json=ap3.get_ap_data(dev3).to_dict())
