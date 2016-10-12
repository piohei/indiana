# -*- coding: utf-8 -*-

from tornado_json import schema
from tornado_json.exceptions import APIError, api_assert
from tornado_json.requesthandlers import APIHandler

from exception.exception import DBException, SampleException
from helpers.utils import correct_mac
from models import APData, Mac, RSSI, Time, Signal


class APDataHandler(APIHandler):
    def initialize(self, sample_service):
        self.sample_service = sample_service

    @schema.validate(input_schema={
        'type': 'object',
        'properties': {
            'apMac': {'type': 'string'},
            'time': {'type': 'number'},
            'band': {
                'type': 'number',
                'minimum': 0
            },
            'data': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'clientMac': {'type': 'string'},
                        'rss1': {'type': 'number'},
                        'rss2': {'type': 'number'},
                        'rss3': {'type': 'number'}
                    }
                }
            }
        },
        'required': ['apMac', 'time', 'band', 'data']
    })
    def post(self):
        api_assert(self.body['data'], 400, 'empty data')

        try:
            ap_datas = []

            router_mac = correct_mac(self.body['apMac'])
            signal = Signal(band='2.4', channel=self.body['band'])
            created_at = Time(int(self.body['time']))

            for item in self.body['data']['items']:
                device_mac = correct_mac(item['clientMac'])
                rssis = {}
                if item['rss1'] is not None:
                    rssis['1'] = RSSI(float(item['rss1']))
                if item['rss2'] is not None:
                    rssis['2'] = RSSI(float(item['rss2']))
                if item['rss3'] is not None:
                    rssis['3'] = RSSI(float(item['rss3']))

                if len(rssis) > 0:
                    ap_datas.append(APData(
                        router_mac=router_mac,
                        device_mac=device_mac,
                        created_at=created_at,
                        rssis=rssis,
                        signal=signal
                    ))

            for ap_data in ap_datas:
                self.sample_service.save_ap_data_for_sample(ap_data)
        except SampleException as e:
            raise APIError(400, e.message)
        except DBException as e:
            raise APIError(500, e.message)
        return 'ok'
