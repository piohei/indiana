# -*- coding: utf-8 -*-

from tornado_json import schema
from tornado_json.exceptions import APIError, api_assert
from tornado_json.requesthandlers import APIHandler
from exception.exception import DBException, SampleException


class APDataHandler(APIHandler):
    def initialize(self, sample_service):
        self.sample_service = sample_service

    @schema.validate(input_schema={
        "type": "object",
        "properties": {
            "apMac": {"type": "string"},
            "time": {"type": "number"},
            "band": {
                "type": "number",
                "minimum": 0
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "clientMac": {"type": "string"},
                        "rss1": {"type": "number"},
                        "rss2": {"type": "number"},
                        "rss3": {"type": "number"}
                    }
                }
            }
        },
        "required": ["apMac", "time", "band", "data"]
    })
    def post(self):
        api_assert(self.body["data"], 400, "empty data")

        try:
            self.sample_service.save_ap_data_for_sample(self.body)
        except SampleException as e:
            raise APIError(400, e.message)
        except DBException as e:
            raise APIError(500, e.message)
        return "ok"
