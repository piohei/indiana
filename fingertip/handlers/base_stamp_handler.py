from abc import abstractmethod, ABCMeta

from tornado_json import schema
from tornado_json.exceptions import APIError
from tornado_json.requesthandlers import APIHandler

from exception import SampleException, DBException
from models import SampleStamp, Mac, Location


class BaseStampHandler(APIHandler, metaclass=ABCMeta):
    def initialize(self, sample_service):
        super().initialize()
        self.sample_service = sample_service

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with, content-type')
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS, DELETE')

    @schema.validate(input_schema={
        'type': 'object',
        'properties': {
            'mac': {'type': 'string'},
            'location': {
                'type': 'object',
                'properties': {
                    'x': {
                        'type': 'number',
                        'minimum': 0
                    },
                    'y': {
                        'type': 'number',
                        'minimum': 0
                    },
                    'z': {'type': 'number'}
                },
                'required': ['x', 'y', 'z']
            }
        },
        'required': ['mac', 'location']
    })
    def post(self):
        try:
            sample = SampleStamp(
                mac=Mac(self.body['mac']),
                location=Location(
                    x=self.body['location']['x'],
                    y=self.body['location']['y'],
                    z=self.body['location']['z']
                )
            )

            self.set_stamp(sample)
        except SampleException as e:
            raise APIError(400, e.message)
        return 'ok'

    @abstractmethod
    def set_stamp(self, sample):
        pass

    def delete(self):
        try:
            self.sample_service.end_sample()
        except SampleException as e:
            raise APIError(400, e.message)
        except DBException as e:
            raise APIError(500, e.message)
        self.success('ok')

    def options(self):
        self.set_status(204)
        self.finish()