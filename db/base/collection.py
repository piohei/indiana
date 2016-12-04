# -*- coding: utf-8 -*-

from pymongo import MongoClient

from config import config
from exception import DBException


class Collection(object):
    def __init__(self, collection_name):
        self.name = collection_name
        self.client = MongoClient(config['db']['host'], config['db']['port'])
        self.db = self.client[config['db']['name']]
        self.collection = self.db[collection_name]

    @staticmethod
    def assert_acknowledged(result):
        if not result.acknowledged:
            raise DBException("Db operation unsuccessful")
        return result

    def count(self, query=None):
        return self.collection.count(query)

    def find(self, query=None, **kwargs):
        return self.collection.find(query if query is not None else {}, **kwargs)

    def replace_one(self, filter, replacement, upsert=True):
        return self.assert_acknowledged(
                self.collection.replace_one(filter=filter, replacement=replacement, upsert=upsert)
        )

    def insert(self, obj_dictionary):
        return self.assert_acknowledged(
                self.collection.insert_one(obj_dictionary)
        )
