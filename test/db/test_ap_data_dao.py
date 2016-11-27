import unittest

from config import config
from db import APDataDAO
from db.base import collection
from test.factory import *


class TestAPDataDao(unittest.TestCase):
    ap_macs = [
        Mac('11:12:13:14:15:16'),
        Mac('21:22:23:24:25:26'),
        Mac('31:32:33:34:35:36'),
        Mac('41:42:43:44:45:46'),
        Mac('51:52:53:54:55:56')
    ]
    times = [
        Time(1),
        Time(2),
        Time(3),
        Time(4)
    ]
    rssis = [
        {'1': RSSI(-10)},
        {'1': RSSI(-20)},
        {'1': RSSI(-30)},
        {'1': RSSI(-40)}
    ]
    signals = [
        Signal(channel=1, band='2.4'),
        Signal(channel=2, band='2.4')
    ]

    def setUp(self):
        collection.client.drop_database(config["db"]["name"])
        self.under_test = APDataDAO()

    def load_fixtures(self):
        ap_datas = [ create_ap_data(signal=signal, created_at=time, rssis=rssi, router_mac=ap_mac)
                     for signal in self.signals
                     for ap_mac in self.ap_macs
                     for rssi   in self.rssis
                     for time   in self.times ]

        for ap_data in ap_datas:
            self.under_test.save(ap_data)

    def test_save(self):
        ap_data = create_ap_data()
        result = self.under_test.save(ap_data)

        self.assertTrue(result.acknowledged)

        self.assertEqual(1, self.under_test.count())
        self.assertEqual(ap_data, self.under_test.find()[0])

    def test_count_entries_since(self):
        def insert_at_time(t):
            ap_data = create_ap_data(created_at=t)
            self.under_test.save(ap_data)

        insert_at_time(Time(1))
        insert_at_time(Time(2))
        insert_at_time(Time(3))
        insert_at_time(Time(3))
        insert_at_time(Time(5))
        insert_at_time(Time(7))

        self.assertEqual(0, self.under_test.count({"created_at" : { "$gte": 8 }}))
        self.assertEqual(1, self.under_test.count({"created_at" : { "$gte": 7 }}))
        self.assertEqual(4, self.under_test.count({"created_at" : { "$gte": 3 }}))
        self.assertEqual(6, self.under_test.count({"created_at" : { "$gte": 0 }}))

