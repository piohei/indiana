from db.base import Collection


class PathDAO(object):
    def __init__(self, ap_data_dao):
        self.ap_data_dao = ap_data_dao

    def save(self, path_stamp):
        path_collection = Collection(path_stamp.name)
        ap_data_for_path = self.ap_data_dao.get_for_time_range(
            path_stamp.start_time, path_stamp.end_time,
            query={'device_mac': str(path_stamp.mac)}
        )
        count = len(ap_data_for_path)
        for ap_data in ap_data_for_path:
            ap_data_dict = self.ap_data_dao.to_db_object(ap_data)
            ap_data_dict.pop("_id", None)
            path_collection.insert(ap_data_dict)
        return "gathered {} for path {}".format(count, path_stamp.name)

    @staticmethod
    def fetch_path(path_name):
        return list(Collection(path_name).find(sort=[('created_at', 1)]))
