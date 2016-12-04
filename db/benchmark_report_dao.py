from db.base import BaseDAO


class BenchmarkReportDAO(BaseDAO):
    def entity(self):
        return "benchmark_report"

    def from_db_object(self, db_object):
        return db_object

    def to_db_object(self, db_object):
        return db_object
