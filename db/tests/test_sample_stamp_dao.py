import unittest

import db.db as db
from config.config import config
from db.sample_stamp_dao import SampleStampDAO
from helpers.test_utils import loc, stamp


class TestSampleStampDao(unittest.TestCase):

    def setUp(self):
        db.client.drop_database(config["db"]["name"])
        self.under_test = SampleStampDAO()
        self.coll_name = SampleStampDAO.collection_name()

    def save(self, x, time=1):
        return self.under_test.save(stamp(loc(x), time))

    def checked_insert(self, x):
        result = self.save(x)
        self.assertTrue(result.acknowledged)
        self.assertEqual(0, result.matched_count)
        self.assertEqual(0, result.modified_count)
        self.assertIsNotNone(result.upserted_id)

    def checked_replace(self, x, time):
        result = self.save(x, time)
        self.assertTrue(result.acknowledged)
        self.assertEqual(1, result.matched_count)
        self.assertEqual(1, result.modified_count)
        self.assertIsNone(result.upserted_id)

    def assertSize(self, size):
        self.assertEqual(size, db.db[self.coll_name].find().count())

    def assertStartTimeForLocation(self, x, time):
        cursor = db.db[self.coll_name].find({"location": loc(x)})
        self.assertEqual(1, cursor.count())
        self.assertEqual(time, cursor[0]["start_time"])

    def test_insert_no_repetitions(self):
        self.checked_insert(1)
        self.checked_insert(2)
        self.checked_insert(3)
        self.checked_insert(4)

        self.assertSize(4)

    def test_insert_repetitions(self):
        self.checked_insert(1)
        self.checked_insert(2)
        self.checked_insert(3)
        self.checked_insert(4)

        self.checked_replace(3, 7)
        self.checked_replace(3, 9)
        self.checked_replace(4, 12)

        self.assertSize(4)
        self.assertStartTimeForLocation(3, 9)
        self.assertStartTimeForLocation(4, 12)

    def test_find_maps_correctly(self):
        stamp1 = stamp(loc(1))
        stamp2 = stamp(loc(2))

        self.under_test.save(stamp1)
        self.under_test.save(stamp2)

        result1 = self.under_test.find({"location": loc(1)})
        self.assertEqual(1, len(result1))
        self.assertEqual(stamp1, result1[0])

        result2 = self.under_test.all()
        self.assertEqual(2, len(result2))
        self.assertEqual(stamp1, result2[0])
        self.assertEqual(stamp2, result2[1])



