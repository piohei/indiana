# -*- coding: utf-8 -*-

import pika

from config import config


def connection():
    return pika.BlockingConnection(pika.ConnectionParameters(
            host=config['rabbit']['host'],
            port=config['rabbit']['port']
        ))
