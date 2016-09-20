# -*- coding: utf-8 -*-
from unittest.mock import Mock

from tornado import web

from exception.exception import SampleException, DBException
from fingertip.handlers import APDataHandler
from . import context

import unittest
from tornado.testing import AsyncHTTPTestCase, get_unused_port
import json
import pprint

import fingertip
from helpers import utils


def correct_dict():
    return {
        'data': [{
            'rss1': -64,
            'rss2': -61,
            'rss3': -69,
            'clientMac': 'DCEE0661B03D'
        }],
        'time': utils.millis(),
        'band': 2,
        'apMac': 'F8E71E290500'
    }


def empty_data():
    return {
        'data': [],
        'time': utils.millis(),
        'band': 2,
        'apMac': 'F8E71E290500'
    }


def error_body(text):
    return ('{"status": "fail", "data": "' + text + '"}').encode('ascii')

OK = b'{"status": "success", "data": "ok"}'
DECODE_ERROR = error_body("Input is malformed; could not decode JSON object.")


class TestAPDataHandler(AsyncHTTPTestCase):

    def get_app(self):
        self.sample_service = Mock()
        return web.Application([
            (r"/", APDataHandler, {"sample_service": self.sample_service})
        ])

    def test_post_ap_data_successful(self):
        data = correct_dict()

        response = self.fetch(
            '/',
            method='POST',
            body=json.dumps(data))

        self.assertEqual(response.code, 200)
        self.assertEqual(OK, response.body)
        self.sample_service.save_ap_data_for_sample.assert_called_once_with(data)

    def test_post_ap_data_wrong_json(self):
        json_data = 'abc'

        response = self.fetch(
            '/',
            method='POST',
            body=json_data)

        self.assertEqual(response.code, 400)
        self.assertEqual(DECODE_ERROR, response.body)
        self.sample_service.save_ap_data_for_sample.assert_not_called()

    def test_post_ap_data_empty(self):
        data = empty_data()

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 400)
        self.assertEqual(error_body('empty data'), response.body)
        self.sample_service.save_ap_data_for_sample.assert_not_called()

    def test_post_ap_data_sample_exception(self):
        data = correct_dict()
        self.sample_service.save_ap_data_for_sample = Mock(side_effect=SampleException("message"))

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 400)
        self.assertEqual(error_body('message'), response.body)
        self.sample_service.save_ap_data_for_sample.assert_called_once_with(data)

    def test_post_ap_data_db_exception(self):
        data = correct_dict()
        self.sample_service.save_ap_data_for_sample = Mock(side_effect=DBException("message"))

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 500)
        self.assertEqual(error_body('message'), response.body)
        self.sample_service.save_ap_data_for_sample.assert_called_once_with(data)

if __name__ == '__main__':
    unittest.main()
