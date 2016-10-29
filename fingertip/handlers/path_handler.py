# -*- coding: utf-8 -*-

from tornado_json import schema
from tornado_json.exceptions import APIError
from tornado_json.requesthandlers import APIHandler

from exception import DBException, SampleException
from models import PathStamp, Mac


class PathHandler(APIHandler):
    def initialize(self, path_service):
        super().initialize()
        self.path_service = path_service

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with, content-type')
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS, DELETE')

    @schema.validate(input_schema={
        'type': 'object',
        'properties': {
            'mac': {'type': 'string'},
            'name': {'type': 'string'}
        },
        'required': ['mac', 'name']
    })
    def post(self):
        try:
            sample = PathStamp(
                mac=Mac(self.body['mac']),
                name=self.body["name"]
            )
            self.path_service.set_path_stamp(sample)
        except SampleException as e:
            raise APIError(400, e.message)
        return 'ok'

    def delete(self):
        try:
            result = self.path_service.end_path()
        except SampleException as e:
            raise APIError(400, e.message)
        except DBException as e:
            raise APIError(500, e.message)
        self.success(result)

    def options(self):
        self.set_status(204)
        self.finish()
