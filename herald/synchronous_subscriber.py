import pika
import json
from queue import Queue, Empty
from threading import Thread

from config import config

from .rabbit import connection
from .base_subscriber import BaseSubscriber


class SynchronousSubscriber(BaseSubscriber):
    def __init__(self, key):
        BaseSubscriber.__init__(self, key)
        self.queue = Queue()

    def callback(self, message):
        self.queue.put(message)

    def get(self, timeout=60):
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            return None
