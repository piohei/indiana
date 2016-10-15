import pika
import json
from queue import Queue, Empty
from threading import Thread

from config import config

from .rabbit import connection


class Subscriber(object):
    def __init__(self, key):
        self.key = key
        self.connection = connection()
        self.channel = self.connection.channel()
        self.queue = Queue()
        self.thread = Thread(target = self.channel.start_consuming)

    def start(self):
        self.channel.exchange_declare(
            exchange=config['rabbit']['name'],
            exchange_type='topic'
        )

        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(
            exchange=config['rabbit']['name'],
            queue=queue_name,
            routing_key=self.key
        )

        self.channel.basic_consume(
            lambda c, m, p, b: self.callback(c, m, p, b),
            queue=queue_name,
            no_ack=True
        )

        self.thread.start()

    def stop(self):
        # stop_consuming method must be call within same thread as
        # start_consuming was called
        self.connection.add_timeout(0, lambda: self.channel.stop_consuming())
        if self.thread.isAlive():
            self.thread.join()

    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode("utf-8"))
        self.queue.put(message)

    def get(self, timeout=60):
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            return None

    def destroy(self):
        self.connection.close()
