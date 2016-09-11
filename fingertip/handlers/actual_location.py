# -*- coding: utf-8 -*-

from tornado_json import schema
from tornado_json.exceptions import APIError
from tornado_json.requesthandlers import APIHandler
from fingertip.services import FingertipException
from helpers.db import DBException


class ActualLocationHandler(APIHandler):
    def initialize(self, fingertip_service):
        super().initialize()
        self.fingertip_service = fingertip_service

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS, DELETE')

    # todo schema
    @schema.validate(input_schema={"type": "object"})
    def post(self):
        try:
            self.fingertip_service.set_fingertip(**(self.body))
        except FingertipException as e:
            self.set_status(400, reason=e.message)
        return "ok"

    def delete(self):
        try:
            self.fingertip_service.end_fingertip()
        except FingertipException as e:
            raise APIError(400, e.message)
        except DBException as e:
            raise APIError(500, e.message)
        self.success("ok")

    def options(self):
        self.set_status(204)
        self.finish()
