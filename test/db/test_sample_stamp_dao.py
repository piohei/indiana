import unittest

import db.db as db
from config.config import config
from db.sample_stamp_dao import SampleStampDAO

from models import *
from test.mocks import *


class TestSampleStampDao(unittest.TestCase):
    def setUp(self):
        db.client.drop_database(config['db']['name'])
        self.under_test = SampleStampDAO()
        self.sample_stamps = {
            '1': create_sample_stamp(location=Location(1, 0, 0)),
            '2': create_sample_stamp(location=Location(2, 0, 0)),
            '3': create_sample_stamp(location=Location(3, 0, 0)),
            '4': create_sample_stamp(location=Location(4, 0, 0)),
        }

    def checked_insert(self, sample_stamp):
        result = self.under_test.save(sample_stamp)

        self.assertTrue(result.acknowledged)
        self.assertEqual(0, result.matched_count)
        self.assertEqual(0, result.modified_count)
        self.assertIsNotNone(result.upserted_id)

    def checked_update(self, sample_stamp):
        result = self.under_test.save(sample_stamp)

        self.assertTrue(result.acknowledged)
        self.assertEqual(1, result.matched_count)
        self.assertEqual(1, result.modified_count)
        self.assertIsNone(result.upserted_id)

    def assertStartTimeForLocation(self, x, time):
        cursor = db.db[self.coll_name].find({'location': loc(x)})
        self.assertEqual(1, cursor.count())
        self.assertEqual(time, cursor[0]['start_time'])

    def test_insert_no_repetitions(self):
        self.checked_insert(self.sample_stamps['1'])
        self.checked_insert(self.sample_stamps['2'])
        self.checked_insert(self.sample_stamps['3'])
        self.checked_insert(self.sample_stamps['4'])

        self.assertEqual(4, self.under_test.count())

    def test_insert_repetitions(self):
        self.checked_insert(self.sample_stamps['1'])
        self.checked_insert(self.sample_stamps['2'])
        self.checked_insert(self.sample_stamps['3'])
        self.checked_insert(self.sample_stamps['4'])

        self.sample_stamps['3'].start_time = Time(7)
        self.checked_update(self.sample_stamps['3'])

        self.sample_stamps['3'].start_time = Time(9)
        self.checked_update(self.sample_stamps['3'])

        self.sample_stamps['4'].start_time = Time(12)
        self.checked_update(self.sample_stamps['4'])

        self.assertEqual(4, self.under_test.count())

        sample_stamp = self.under_test.find({'location': {'x': 3, 'y': 0, 'z': 0}})[0]
        self.assertEqual(sample_stamp.start_time, Time(9))

        sample_stamp = self.under_test.find({'location': {'x': 4, 'y': 0, 'z': 0}})[0]
        self.assertEqual(sample_stamp.start_time, Time(12))

    def test_find_maps_correctly(self):
        self.under_test.save(self.sample_stamps['1'])
        self.under_test.save(self.sample_stamps['2'])

        result1 = self.under_test.find({'location': {'x': 1, 'y': 0, 'z': 0}})
        self.assertEqual(1, len(result1))
        self.assertEqual(self.sample_stamps['1'], result1[0])

        result2 = self.under_test.all()
        self.assertEqual(2, len(result2))
        self.assertEqual(self.sample_stamps['1'], result2[0])
        self.assertEqual(self.sample_stamps['2'], result2[1])



