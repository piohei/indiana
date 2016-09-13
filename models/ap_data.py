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

    @staticmethod
    def collection_name():
        return 'ap_data'

    def save(self):
        return db.insert_into(self.collection_name(), self.to_dict())

    def to_dict(self):
        return self.__dict__

    def __str__(self, *args, **kwargs):
        return "APData[device_MAC={}, router_MAC={}, rssi={}, channel={}, t={}]".format(
                self.device_MAC, self.router_MAC, self.rssi, self.channel, self.timestamp)

    @classmethod
    def count_entries_since(cls, t):
        db.count(cls.collection_name(), {'time': {'$gt': t}})

    @classmethod
    def group_for_fingertip(cls, fingertip):
        return db.group(
            collection=cls.collection_name(),
            key=["apMac", "band"],
            condition={
                "time": {
                    "$gte": fingertip.start_time,
                    "$lte": fingertip.end_time
                }
            },
            initial={"ap_data": []},
            reduce="function(curr, result) {"
                       "var o = curr.data[0];"
                       "var mapped = {rss1: o.rss1, rss2: o.rss2, rss3: o.rss3, time: curr.time};"
                       "result.ap_data.push(mapped);"
                   "}"
        )
