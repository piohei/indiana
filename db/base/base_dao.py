from abc import ABCMeta, abstractmethod

from config import config
from db.base.collection import Collection


class BaseDAO(object, metaclass=ABCMeta):
    def __init__(self):
        collection_name = config["db"]["collections"][self.entity()]
        self.collection = Collection(collection_name)
        print("Connection to MongoDB {} created for {}".format(self.collection.client.address, self.__class__.__name__))

    @abstractmethod
    def from_db_object(self, db_object):
        pass

    @abstractmethod
    def to_db_object(self, object):
        pass

    @abstractmethod
    def entity(self):
        pass

    def find(self, query=None, **kwargs):
        return list(map(self.from_db_object, self.collection.find(query, **kwargs)))

    def all(self, **kwargs):
        return self.find(query={}, **kwargs)

    def count(self, query=None):
        return self.collection.count(query)

    def save(self, object):
        return self.collection.insert(self.to_db_object(object))
