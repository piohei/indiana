import datetime
import math
import time

import requests

from domain import Location, APData

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
loc2 = Location(20, 30, 0)
loc3 = Location(15, 20, 0)

locations = []

for i in range(5):
    x = loc1.x + float(i) / 5 * (loc2.x - loc1.x)
    y = loc1.y + float(i) / 5 * (loc2.y - loc1.y)
    locations.append(Location(x, y, 0))
for i in range(5):
    x = loc2.x + float(i) / 5 * (loc3.x - loc2.x)
    y = loc2.y + float(i) / 5 * (loc3.y - loc2.y)
    locations.append(Location(x, y, 0))
for i in range(5):
    x = loc3.x + float(i) / 5 * (loc1.x - loc3.x)
    y = loc3.y + float(i) / 5 * (loc1.y - loc3.y)
    locations.append(Location(x, y, 0))

mac = '11:12:13:14:15:16'

while True:
    for loc in locations:
        requests.post(base_url + 'location/' + mac, json=loc.to_dict())
        print("waiting... ({0})".format(loc.to_dict()))
        time.sleep(1)
