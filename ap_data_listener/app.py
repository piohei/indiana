# -*- coding: utf-8 -*-

from threading import RLock

from tornado import web, ioloop

from config import env
from db import APDataDAO
from .ap_data_handler import APDataHandler


class App:
    def __init__(self, config):
        self.global_lock = RLock()
        self.port = int(config["port"])

        self.ap_data_dao = APDataDAO()

        self.app = web.Application(handlers=[
            (config["endpoint"], APDataHandler, {
                    "ap_data_dao": self.ap_data_dao
                })
        ], debug=(env == 'development'))

    def get_app(self):
        return self.app

    def run(self):
        self.app.listen(self.port, address="0.0.0.0")
        ioloop.IOLoop.instance().start()
