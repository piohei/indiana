from db.db import insert_into, db


class APDataDAO(object):
    @staticmethod
    def collection_name():
        return "ap_data"

    def save_dict(self, d):
        return insert_into(self.collection_name(), d)

    def count_entries_since(self, t):
        return db[self.collection_name()].count({'time': {'$gte': t}})
