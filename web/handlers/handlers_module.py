from abc import ABCMeta, abstractmethod


class HandlersModule(object, metaclass=ABCMeta):
    def __init__(self, config):
        module = config["web"]["routes"][self.module()]
        self.prefix = module["prefix"]
        self.endpoints = module["endpoints"]

    @abstractmethod
    def get_handlers(self, config):
        pass

    @abstractmethod
    def module(self):
        pass