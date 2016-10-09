# -*- coding: utf-8 -*-
from .time import Time
from .rssi_measure import RSSIMeasure


class TimedRSSIMeasure(RSSIMeasure):
    def __init__(self, rssi1, rssi2, rssi3, time):
        super().__init__(rssi1, rssi2, rssi3)

        if type(time) != Time:
            raise ValueError("Argument time must be type of models.Time")

        self.time = time

    def to_rssi_measure(self):
        return RSSIMeasure(self.rssi1, self.rssi2, self.rssi3)

    @staticmethod
    def from_db_object(db_object):
        return RSSIMeasure(
            rssi1=RSSI.form_db_object(db_object["rssi1"]),
            rssi2=RSSI.form_db_object(db_object["rssi2"]),
            rssi3=RSSI.form_db_object(db_object["rssi3"]),
            time=Time.from_db_object(db_object["time"])
        )

    def to_db_object(self):
        return {
            "rssi1": self.rssi1.to_db_object(),
            "rssi2": self.rssi2.to_db_object(),
            "rssi3": self.rssi3.to_db_object(),
            "time": self.time.to_db_object(),
        }

    def __str__(self):
        return "({}, {}, {}, {})".format(self.rssi1, self.rssi2, self.rssi3, self.time)
