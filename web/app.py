# -*- coding: utf-8 -*-

from tornado import web, ioloop
import os

from config import env, config
from helpers.utils import mac_regexp_dashes

from db import AccessPointDAO, SampleStampDAO
from models import Map

from .handlers import *

class App:
    def __init__(self):
        self.access_point_dao = AccessPointDAO()
        self.sample_stamp_dao = SampleStampDAO()

        self.map_data = Map(config['map']['name'])

        self.app = web.Application(
            handlers=[
                (r"/position/({})".format(mac_regexp_dashes()), PositionHandler),
                (r"/visualization/3d", Visualization3DHandler),
                (r"/visualization/2d", Visualization2DHandler),
                (r"/fingertip", FingerTipHandler),
                (r"/path", PathHandler),
                (r"/map", MapHandler, {
                    'access_point_dao': self.access_point_dao,
                    'sample_stamp_dao': self.sample_stamp_dao,
                    'map_data': self.map_data
                }),
                (r"/", RootHandler),
            ],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            debug=(env == 'development')
        )

    def get_app(self):
        return self.app

    def run(self):
        self.app.listen(8888, address="0.0.0.0")

        ioloop.IOLoop.instance().start()
