# -*- coding: utf-8 -*-

from . import context

import unittest
from tornado.testing import AsyncHTTPTestCase
import json
import pprint

import fingertip
from helpers import utils

app = fingertip.App()

class TestHandlerBase(AsyncHTTPTestCase):
    def get_app(self):
        return app.get_app()

    def test_post_ap_data_successful(self):
        json_data = json.dumps({
            'data': {
                'rss1': -64,
                'rss2': -61,
                'rss3': -69,
                'clientMac': 'DCEE0661B03D'
            },
            'time': utils.millis(),
            'band': 2,
            'apMac': 'F8E71E290500'
        })

        response = self.fetch(
            '/',
            method='POST',
            body=json_data)

        pprint.pprint(response)
        # On successful, response is expected to return 200
        self.assertEqual(response.code, 200)

    def test_post_ap_data_wrong_json(self):
        json_data = 'abc'

        response = self.fetch(
            '/',
            method='POST',
            body=json_data)

        pprint.pprint(response)
        # On wrong JSON, response is expected to return 400
        self.assertEqual(response.code, 400)
        self.assertEqual(response.reason, 'Error parsing JSON.')

if __name__ == '__main__':
    unittest.main()
