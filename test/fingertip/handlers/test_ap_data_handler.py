# -*- coding: utf-8 -*-
import json
import unittest
from unittest.mock import Mock

from tornado import web
from tornado.testing import AsyncHTTPTestCase

from exception import SampleException, DBException
from fingertip.handlers import APDataHandler
from models import *


def correct_dict():
    return {
        'data': [{
            'rss1': -64,
            'rss2': -61,
            'rss3': -69,
            'clientMac': 'DCEE0661B03D'
        }],
        'time': 10,
        'band': 2,
        'apMac': 'F8E71E290500'
    }


def empty_data():
    return {
        'data': [],
        'time': 10,
        'band': 2,
        'apMac': 'F8E71E290500'
    }

# TODO refactor
class TestAPDataHandler(AsyncHTTPTestCase):

    def get_app(self):
        self.sample_service = Mock()
        return web.Application([
            (r"/", APDataHandler, {"sample_service": self.sample_service})
        ])

    def check_ap_data(self, ap_data):
        self.assertEqual(ap_data.router_mac, Mac("F8:E7:1E:29:05:00"))
        self.assertEqual(ap_data.device_mac, Mac("DC:EE:06:61:B0:3D"))
        self.assertEqual(ap_data.created_at, Time(10))
        self.assertEqual(ap_data.signal, Signal(band='2.4', channel=2))
        self.assertEqual(ap_data.rssis, {
                '1': RSSI(-64),
                '2': RSSI(-61),
                '3': RSSI(-69)
            })

    def test_post_ap_data_successful(self):
        data = correct_dict()

        response = self.fetch(
            '/',
            method='POST',
            body=json.dumps(data))

        self.assertEqual(response.code, 200)
        self.assertEqual(1, self.sample_service.save_ap_data_for_sample.call_count)
        created_ap_data = self.sample_service.save_ap_data_for_sample.call_args[0][0]
        self.check_ap_data(created_ap_data)

    def test_post_ap_data_wrong_json(self):
        json_data = 'abc'

        response = self.fetch(
            '/',
            method='POST',
            body=json_data)

        self.assertEqual(response.code, 400)
        self.sample_service.save_ap_data_for_sample.assert_not_called()

    def test_post_ap_data_empty(self):
        data = empty_data()

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 400)
        self.sample_service.save_ap_data_for_sample.assert_not_called()

    def test_post_ap_data_sample_exception(self):
        data = correct_dict()
        self.sample_service.save_ap_data_for_sample = Mock(side_effect=SampleException("message"))

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 400)
        self.assertEqual(1, self.sample_service.save_ap_data_for_sample.call_count)
        created_ap_data = self.sample_service.save_ap_data_for_sample.call_args[0][0]
        self.check_ap_data(created_ap_data)

    def test_post_ap_data_db_exception(self):
        data = correct_dict()
        self.sample_service.save_ap_data_for_sample = Mock(side_effect=DBException("message"))

        response = self.fetch(
                '/',
                method='POST',
                body=json.dumps(data))

        self.assertEqual(response.code, 500)
        self.assertEqual(1, self.sample_service.save_ap_data_for_sample.call_count)
        created_ap_data = self.sample_service.save_ap_data_for_sample.call_args[0][0]
        self.check_ap_data(created_ap_data)

if __name__ == '__main__':
    unittest.main()
