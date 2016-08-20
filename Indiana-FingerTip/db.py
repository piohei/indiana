from pymongo import MongoClient

db = MongoClient('52.42.120.42', 27017).indiana_db


class DbException(Exception):
    def __init__(self, message):
        self.message = message


def insert_into(collection, obj_dictionary):
    inserted = collection.insert_one(obj_dictionary)
    if not inserted.acknowledged:
        raise DbException("not inserted")
    return inserted


def save_fingertip(fingertip):
    return insert_into(db.fingertips, fingertip.to_dict())


def save_ap_data(ap_data_dict):
    return insert_into(db.ap_data, ap_data_dict)


def count_ap_data_entries_since(start_time):
    return db.ap_data.count({"time": {"$gt": start_time}})



