import unittest

import db.db as db
from config.config import config

from db.ap_data_dao import APDataDAO
from db.rssi_measure_dao import RSSIMeasureDAO
from models.rssi_measure import TimedRSSIMeasure


def ap_data_dict(rss1, time, band, apid):
    return {
        'data': [{
            'rss1': rss1,
            'rss2': rss1+1,
            'rss3': rss1+2,
            'clientMac': 'DCEE0661B03D'
        }],
        'time': time,
        'band': band,
        'apMac': str(apid)
    }


def timed_rss1(rss1, time):
    return TimedRSSIMeasure(rss1, rss1+1, rss1+2, time)


class TestRSSIMeasureDAO(unittest.TestCase):
    apids = [1, 2, 3, 4, 5]
    times = [1, 2, 3, 4]
    rss1s = [1, 2, 3, 4]
    bands = [1, 2]

    def setUp(self):
        db.client.drop_database(config["db"]["name"])
        self.under_test = RSSIMeasureDAO()

    def data_setup(self):
        ap_data_dao = APDataDAO()

        dicts = [ap_data_dict(rss1, time, band, apid)
                 for band in self.bands
                 for apid in self.apids
                 for rss1 in self.rss1s
                 for time in self.times]

        for dict in dicts:
            ap_data_dao.save_dict(dict)

    def expected_result(self, start, end):
        return {
            band: {
                str(apid): [
                    timed_rss1(rss1, time)
                    for rss1 in self.rss1s
                    for time in self.times
                    if start <= time <= end
                ]
                for apid in self.apids
            }
            for band in self.bands
        }

    def test_group(self):
        self.data_setup()
        self.assertDictEqual(self.expected_result(2, 4), self.under_test.grouped_timed_measures_for_range(2, 4))

