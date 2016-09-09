# -*- coding: utf-8 -*-

from helpers import db

class APData(object):
    def __init__(self, device_MAC='', router_MAC='', timestamp='', rssi=0,
                 channel=-1, tuple=None, dictionary=None):
        if tuple is not None:
            device_MAC = tuple[0]
            router_MAC = tuple[1]
            timestamp = tuple[2]
            rssi=tuple[3]
            channel = tuple[4]
        elif dictionary is not None:
            device_MAC = dictionary['device_MAC']
            router_MAC = dictionary['router_MAC']
            timestamp = dictionary['timestamp']
            rssi = dictionary['rssi']
            channel = dictionary['channel']

        self.device_MAC = device_MAC
        self.router_MAC = router_MAC
        self.timestamp = timestamp
        self.rssi = rssi
        self.channel = channel

    def collection_name(self):
        return 'ap_data'

    def save(self):
        return db.insert_into(self.collection_name(), self.to_dict())

    def to_dict(self):
        return self.__dict__

    def __str__(self, *args, **kwargs):
        return "APData[device_MAC={}, router_MAC={}, rssi={}, channel={}, t={}]". \
                    format(self.device_MAC, self.router_MAC, self.rssi,
                           self.channel, self.timestamp)

def count_entries_since(t):
    db.count({'time': {'$gt': start_time}})
