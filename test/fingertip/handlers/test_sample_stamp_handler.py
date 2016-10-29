# -*- coding: utf-8 -*-
import json
import unittest
from unittest.mock import Mock

from tornado import web
from tornado.testing import AsyncHTTPTestCase

from exception import SampleException, DBException
from fingertip.handlers import APDataHandler, SampleStampHandler

from models import *


def correct_dict():
    return {
        "mac": "DC:EE:06:61:B0:3D",
        "location": {
            "x": 1,
            "y": 1,
            "z": -2
        }
    }

def error_dict():
    return {
        "mac": "DC:EE:06:61:B0:3D",
        "location": {
            "x": -1,
            "y": 1,
            "z": -2
        }
    }

def error_body(text):
    return ('{"status": "fail", "data": "' + text + '"}').encode('ascii')

OK = b'{"status": "success", "data": "ok"}'
DECODE_ERROR = error_body("Input is malformed; could not decode JSON object.")


# TODO test delete and options refactor, check service calls
class TestSampleStampHandler(AsyncHTTPTestCase):

    def get_app(self):
        self.sample_service = Mock()
        return web.Application([
            (r"/", SampleStampHandler, {"sample_service": self.sample_service})
        ])

    def test_post_successful(self):
        data = correct_dict()

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 200)

    def test_post_ap_data_wrong_json(self):
        json_data = 'abc'

        response = self.fetch(
                '/',
                method='POST',
                body=json_data)

        self.assertEqual(response.code, 400)
        self.sample_service.set_sample_stamp.assert_not_called()

    def test_post_schema_constraints_violated(self):
        data = error_dict()

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 400)
        self.sample_service.set_sample_stamp.assert_not_called()

    def test_post_ap_data_sample_exception(self):
        data = correct_dict()
        self.sample_service.set_sample_stamp = Mock(side_effect=SampleException("message"))

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 400)

if __name__ == '__main__':
    unittest.main()

