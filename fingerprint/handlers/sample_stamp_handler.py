# -*- coding: utf-8 -*-

from fingerprint.handlers.base_stamp_handler import BaseStampHandler


class SampleStampHandler(BaseStampHandler):
    def set_stamp(self, sample):
        self.sample_service.set_sample_stamp(sample)
