from .base_subscriber import BaseSubscriber


class AsynchronousSubscriber(BaseSubscriber):
    def __init__(self, key, callback):
        BaseSubscriber.__init__(self, key)
        self.user_callback = callback

    def callback(self, message):
        self.user_callback(message)
