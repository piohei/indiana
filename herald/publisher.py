import pika
import json

from config import config

from .rabbit import connection


class Publisher(object):
    def __init__(self, key):
        self.key = key
        self.connection = connection()
        self.channel = self.connection.channel()

    def publish(self, message):
        self.channel.exchange_declare(
            exchange=config['rabbit']['name'],
            exchange_type='topic'
        )

        message = json.dumps(message)

        self.channel.basic_publish(
            exchange=config['rabbit']['name'],
            routing_key=self.key,
            body=message
        )

    def destroy(self):
        self.connection.close()
