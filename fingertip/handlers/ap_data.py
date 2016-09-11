# -*- coding: utf-8 -*-

from tornado_json import schema
from tornado_json.exceptions import APIError, api_assert
from tornado_json.requesthandlers import APIHandler
from helpers.db import DBException
from models.ap_data import APData


class APDataHandler(APIHandler):
    def initialize(self, fingertip_service):
        self.fingertip_service = fingertip_service

    # todo schema
    @schema.validate(input_schema={"type": "object"})
    def post(self):
        current_fingertip = self.fingertip.service.current_fingertip

        api_assert(current_fingertip is not None and not current_fingertip.is_outdated(), 400, "fingertip gone or outdated")

        api_assert(self.body["data"], 400, "empty data")

        try:
            APData(self.body).save()
        except DBException as e:
            raise APIError(500, e.message)
        return "ok"
