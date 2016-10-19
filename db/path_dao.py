from db.db import find, db
from . import APDataDAO

class PathDAO(object):
    def save(self, path_stamp):
        ap_data_for_path = find(APDataDAO.collection_name(), {
            'created_at': {
                '$gte': path_stamp.start_time.millis,
                '$lte': path_stamp.end_time.millis
            },
            'device_mac': str(path_stamp.mac)
        })
        count = ap_data_for_path.count()
        for ap_data_dict in ap_data_for_path:
            ap_data_dict.pop("_id", None)
            db[path_stamp.name].insert_one(ap_data_dict)
        return "gathered {} for path {}".format(count, path_stamp.name)

