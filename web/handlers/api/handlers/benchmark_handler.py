from tornado_json.exceptions import APIError
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema

from web.services.benchmark_service import BenchmarkException


class BenchmarkHandler(APIHandler):
    def initialize(self, benchmark_service):
        self.benchmark_service = benchmark_service

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with, content-type')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

    @schema.validate(output_schema={"type": "string"})
    def post(self):
        try:
            self.benchmark_service.start_new_benchmark()
        except BenchmarkException as e:
            raise APIError(400, e.message)
        return "ok"

    def delete(self):
        try:
            self.benchmark_service.kill_current_benchmark()
        except BenchmarkException as e:
            raise APIError(400, e.message)
        self.success("ok")

    @schema.validate(output_schema={"type": "string"})
    def get(self):
        return self.benchmark_service.get_status()