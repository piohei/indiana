import unittest
import db.db as db
from config.config import config
from db.ap_data_dao import APDataDAO

class TestAPDataDao(unittest.TestCase):
    def setUp(self):
        db.client.drop_database(config["db"]["name"])
        self.under_test = APDataDAO()

    def test_save_dict(self):
        dictionary = {"time": 1}
        result = self.under_test.save_dict(dictionary)

        self.assertTrue(result.acknowledged)

        cursor = db.db[APDataDAO.collection_name()].find()
        self.assertEqual(1, cursor.count())
        self.assertDictEqual(dictionary, cursor[0])

    def test_count_entries_since(self):
        def insert_at_time(t):
            db.db[APDataDAO.collection_name()].insert_one({"time": t})
        insert_at_time(1)
        insert_at_time(2)
        insert_at_time(3)
        insert_at_time(3)
        insert_at_time(5)
        insert_at_time(7)

        self.assertEqual(0, self.under_test.count_entries_since(8))
        self.assertEqual(1, self.under_test.count_entries_since(7))
        self.assertEqual(4, self.under_test.count_entries_since(3))
        self.assertEqual(6, self.under_test.count_entries_since(0))
