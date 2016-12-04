from abc import ABCMeta

from db.base.base_dao import BaseDAO


class TimedDAO(BaseDAO, metaclass=ABCMeta):
    def get_for_time_range(self, start_time, end_time, asc=True, query=None):
        timed_query = {'created_at': {'$gte': start_time.millis, '$lte': end_time.millis}}
        timed_query.update(query if query is not None else {})
        return self.find(
                query=timed_query,
                sort=[('created_at', 1 if asc else -1)]
        )