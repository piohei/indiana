# -*- coding: utf-8 -*-

from tornado import ioloop


class CleanupJob(ioloop.PeriodicCallback):
    CALLBACK_TIME = 30000

    def __init__(self, fingertip_service):
        super().__init__(self.callback, self.CALLBACK_TIME)
        self.service = fingertip_service

    def callback(self):
        self.service.end_if_outdated()
