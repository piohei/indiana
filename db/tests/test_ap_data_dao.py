import unittest
import db.db as db
from config.config import config
from db.ap_data_dao import APDataDAO

class TestAPDataDao(unittest.TestCase):
    def setUp(self):
        db.client.drop_database(config["db"]["name"])
        self.under_test = APDataDAO()

    def test_save_dict(self):
        dictionary = {"key": "anything as we save jasons"}
        result = self.under_test.save_dict(dictionary)

        self.assertTrue(result.acknowledged)
        in_db = db.db[APDataDAO.collection_name()].find()