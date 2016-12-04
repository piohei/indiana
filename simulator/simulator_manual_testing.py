import os

from tornado import web, ioloop
from tornado_json import schema
from tornado_json.requesthandlers import APIHandler

from models.primitives.time import Time
from simulator.path_simulator import CycledPathSimulator

TEST_DATA = [
    {"rssis": {"1": 1, "3": -78}, "router_mac": "2c:5d:93:0c:8a:60", "created_at": 0,
     "device_mac": "dc:ee:06:61:b0:3d", "signal": {"channel": 2, "band": "2.4"}},
    {"rssis": {"1": 2, "2": -107}, "router_mac": "f8:e7:1e:29:08:f0", "created_at": 10,
     "device_mac": "dc:ee:06:61:b0:3d", "signal": {"channel": 2, "band": "2.4"}},
    {"rssis": {"1": 3, }, "router_mac": "f8:e7:1e:29:08:f0", "created_at": 20,
     "device_mac": "dc:ee:06:61:b0:3d", "signal": {"channel": 2, "band": "2.4"}},
    {"rssis": {"1": 4, "2": -75, }, "router_mac": "f8:e7:1e:29:0e:e0", "created_at": 30,
     "device_mac": "dc:ee:06:61:b0:3d", "signal": {"channel": 2, "band": "2.4"}},
    {"rssis": {"1": 5, "3": -82}, "router_mac": "2c:5d:93:0c:8a:60", "created_at": 40,
     "device_mac": "dc:ee:06:61:b0:3d", "signal": {"channel": 2, "band": "2.4"}},
    {"rssis": {"1": 6}, "router_mac": "f8:e7:1e:29:08:f0", "created_at": 50,
     "device_mac": "dc:ee:06:61:b0:3d", "signal": {"channel": 2, "band": "2.4"}},
    {"rssis": {"1": 7, "2": -75, "3": -81}, "router_mac": "f8:e7:1e:29:0e:e0", "created_at": 60,
     "device_mac": "dc:ee:06:61:b0:3d", "signal": {"channel": 2, "band": "2.4"}}
]


class MockPathDao:
    @staticmethod
    def fetch_path(name):
        print("fetching " + name)
        return TEST_DATA


class TestLoggingHandler(APIHandler):
    RECEIVED = 0
    PREV_TIME = None
    LAST_RECEIVED_REAL_TIME = None

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
        receiving_time = Time()
        TestLoggingHandler.RECEIVED += 1
        timestamps_dif = 0
        real_time_dif = 0
        this_time = Time(millis=self.body["time"])
        if TestLoggingHandler.PREV_TIME is not None:
            timestamps_dif = this_time.millis - TestLoggingHandler.PREV_TIME.millis
        TestLoggingHandler.PREV_TIME = this_time
        if TestLoggingHandler.LAST_RECEIVED_REAL_TIME is not None:
            real_time_dif = receiving_time.millis - TestLoggingHandler.LAST_RECEIVED_REAL_TIME.millis
        TestLoggingHandler.LAST_RECEIVED_REAL_TIME = receiving_time
        print("received {}, timestamps diff:{}, real time diff: {}, id: {}".format(
                TestLoggingHandler.RECEIVED, timestamps_dif, real_time_dif, self.body["data"][0]["rss1"]))


app = web.Application(handlers=[
    (r"/", TestLoggingHandler)
])

newpid = os.fork()
if newpid == 0:
    CycledPathSimulator("path1", MockPathDao()).run()
else:
    app.listen(8889, address="0.0.0.0")
    ioloop.IOLoop.instance().start()
