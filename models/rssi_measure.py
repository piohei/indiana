# -*- coding: utf-8 -*-
from .rssi import RSSI


class RSSIMeasure(object):
    def __init__(self, rssi1=None, rssi2=None, rssi3=None):
        if rssi1 is not None and type(rssi1) != RSSI:
            raise ValueError("Argument rssi1 must be type of models.RSSI")
        if rssi2 is not None and type(rssi2) != RSSI:
            raise ValueError("Argument rssi2 must be type of models.RSSI")
        if rssi3 is not None and type(rssi3) != RSSI:
            raise ValueError("Argument rssi3 must be type of models.RSSI")

        self.rssi1 = rssi1
        self.rssi2 = rssi2
        self.rssi3 = rssi3

    @staticmethod
    def from_db_object(db_object):
        return RSSIMeasure(
            rssi1=RSSI.form_db_object(db_object["rssi1"]),
            rssi2=RSSI.form_db_object(db_object["rssi2"]),
            rssi3=RSSI.form_db_object(db_object["rssi3"])
        )

    def to_db_object(self):
        return {
            "rssi1": self.rssi1.to_db_object(),
            "rssi2": self.rssi2.to_db_object(),
            "rssi3": self.rssi3.to_db_object()
        }

    def __str__(self):
        return "({}, {}, {})".format(self.rssi1, self.rssi2, self.rssi3)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
