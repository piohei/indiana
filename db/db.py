# -*- coding: utf-8 -*-

from pymongo import MongoClient

from config.config import config
from exception.exception import DBException

client = MongoClient(config['db']['host'], config['db']['port'])
print("Connection to MongoDB {} created".format(client.address))

db = client[config['db']['name']]


def assert_acknowledged(result):
    if not result.acknowledged:
        raise DBException("Db operation unsuccessful")
    return result


def insert_into(collection, obj_dictionary):
    return assert_acknowledged(
               db[collection].insert_one(obj_dictionary)
           )


def replace_one(collection, filter, replacement, upsert=True):
    return assert_acknowledged(
               db[collection].replace_one(
                   filter=filter, replacement=replacement, upsert=upsert
               )
           )


def find(collection, query={}):
    return db[collection].find(query)


def count(collection, query={}):
    return db[collection].count(query)


def group(collection, key, condition={}, initial={}, reduce=None, finalize=None):
    return db[collection].group(key=key, condition=condition, initial=initial, reduce=reduce, finalize=finalize)


