import pika
import json
from queue import Queue, Empty
from threading import Thread

from config import config

from .rabbit import connection
from .base_subscriber import BaseSubscriber


class AsynchronousSubscriber(BaseSubscriber):
    def __init__(self, key, callback):
        BaseSubscriber.__init__(self, key)
        self.user_callback = callback

    def callback(self, message):
        self.user_callback(message)
