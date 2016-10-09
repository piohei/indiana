from db.db import db, find, count, insert_into


class BaseDAO(object):
    @staticmethod
    def collection_name():
        raise NotImplementedError

    def from_db_object(self, db_object):
        raise NotImplementedError

    def to_db_object(self, object):
        raise NotImplementedError

    def find(self, query):
        return list(map(self.from_db_object, find(self.collection_name(), query)))

    def all(self):
        return self.find(query={})

    def count(self, query):
        return count(self.collection_name(), query)

    def save(self, object):
        return insert_into(self.collection_name(), self.to_db_object(object))
