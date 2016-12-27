import json
from tornado_json.requesthandlers import APIHandler


class ReportsHandler(APIHandler):
    def initialize(self, benchmark_report_dao):
        self.benchmark_report_dao = benchmark_report_dao

    def get(self):
        result =  self.benchmark_report_dao.all(projection={
            "_id": False, "start": False, "end": False, "partial_reports": False
        })
        self.write(json.dumps(result))