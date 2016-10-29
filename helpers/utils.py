# -*- coding: utf-8 -*-
import random


def functional_add(key, value, dictionary):
    new = dict(dictionary)
    new[key] = value
    return new


def mac_regexp():
    return r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}'


def mac_regexp_dashes():
    return r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}'


def correct_mac(mac):
    return ':'.join([mac[i:i+2].lower() for i in range(0, len(mac), 2)])


def generate_id():
    return ''.join(random.choice("abcdef0123456789") for _ in range(24))


def deep_eq_dict(a, b):
    if a.keys() != b.keys():
        return False

    for k in a.keys():
        if type(k) == dict:
            if not deep_eq_dict(a, b):
                return False
        else:
            if a != b:
                return False

    return True
