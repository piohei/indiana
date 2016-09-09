# -*- coding: utf-8 -*-

from tornado import ioloop

class StatusJob(ioloop.PeriodicCallback):
    CALLBACK_TIME = 10000

    def __init__(self, fingertip_service, ws_service):
        super().__init__(self.callback, self.CALLBACK_TIME)
        self.fingertip_service = fingertip_service
        self.ws_service = ws_service

    def callback(self):
        status = self.fingertip_service.get_status()
        self.ws_service.broadcast(status)
