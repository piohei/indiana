from pymongo import MongoClient

import config

db = MongoClient(config.DB_HOST, config.DB_PORT).indiana_db


class DbException(Exception):
    def __init__(self, message):
        self.message = message

def assert_acknowledged(result):
    if not result.acknowledged:
        raise DbException("Db operation unsuccessful")
    return result

def insert_into(collection, obj_dictionary):
    return assert_acknowledged(collection.insert_one(obj_dictionary))


def save_fingertip(fingertip):
    return assert_acknowledged(db.fingertips.replace_one(
        filter={
            "location.x": fingertip.location["x"],
            "location.y": fingertip.location["y"],
            "location.z": fingertip.location["z"]
        },
        replacement=fingertip.to_dict(),
        upsert=True
    ))


def save_ap_data(ap_data_dict):
    return insert_into(db.ap_data, ap_data_dict)


def count_ap_data_entries_since(start_time):
    return db.ap_data.count({"time": {"$gt": start_time}})



