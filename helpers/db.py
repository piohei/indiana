# -*- coding: utf-8 -*-

from pymongo import MongoClient
import config

db = MongoClient(config.DB_HOST, config.DB_PORT)[config.DB_NAME]


class DBException(Exception):
    def __init__(self, message):
        self.message = message


def assert_acknowledged(result):
    if not result.acknowledged:
        raise DBException("Db operation unsuccessful")
    return result

def insert_into(collection, obj_dictionary):
    return assert_acknowledged(
               db[collection].insert_one(obj_dictionary)
           )

def replace_one(collection, filter={}, replacement={}, upsert=True):
    return assert_acknowledged(
               db[collection].replace_one(
                   filter=filter, replacement=replacement, upsert=upsert
               )
           )

def count(collection, filter={}):
    return db[collection].count(filter)
