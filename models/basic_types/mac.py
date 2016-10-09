# -*- coding: utf-8 -*-
import re
from helpers.utils import mac_regexp


class Mac(object):
    def __init__(self, mac):
        if type(mac) != str:
            raise ValueError('Argument mac must be string')
        if re.search(mac_regexp(), mac) is None:
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
