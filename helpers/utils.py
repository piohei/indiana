# -*- coding: utf-8 -*-


def functional_add(key, value, dictionary):
    new = dict(dictionary)
    new[key] = value
    return new

def mac_regexp():
    return r'^[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}:' \
           r'[a-fA-F0-9]{2}$'

def mac_regexp_dashes():
    return r'^[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}-' \
           r'[a-fA-F0-9]{2}$'

def correct_mac(mac):
    return ':'.join([mac[i:i+2].lower() for i in range(0, len(mac), 2)])
