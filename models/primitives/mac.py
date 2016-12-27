# -*- coding: utf-8 -*-
import re


class Mac(object):
    REGEXP = r'^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$'

    def __init__(self, mac):
        if type(mac) != str:
            raise ValueError('Argument mac must be string')
        if re.search(self.REGEXP, mac) is None:
            raise ValueError('Argument mac must be valid mac')

        self.mac = mac.lower()

    def __str__(self, *args, **kwargs):
        return self.mac

    def __repr__(self):
        return '"{}"'.format(str(self))

    def __eq__(self, other):
        return self.mac == other.mac

    def __hash__(self):
        return hash(self.mac)

    @classmethod
    def correct(cls, mac):
        return cls(':'.join([mac[i:i+2].lower() for i in range(0, len(mac), 2)]))

    @staticmethod
    def raw(mac):
        return mac.replace(":", "").upper()
