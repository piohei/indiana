# -*- coding: utf-8 -*-

import time


def millis():
    return int(round(time.time() * 1000))


def functional_add(key, value, dictionary):
    new = dict(dictionary)
    new[key] = value
    return new
