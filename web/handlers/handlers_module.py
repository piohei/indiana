from abc import ABCMeta, abstractmethod


class HandlersModule(object, metaclass=ABCMeta):
    def __init__(self, config):
        module = config["web"]["routes"][self.module()]
        self.prefix = module["prefix"]
        self.endpoints = module["endpoints"]

    def get_handlers(self):
        return self.only_defined_handlers(self.handlers_specs())

    @abstractmethod
    def handlers_specs(self):
        pass

    @abstractmethod
    def module(self):
        pass

    def only_defined_handlers(self, handlers_specs):
        return [
            self.to_full_spec(*handler_spec)
            for handler_spec in handlers_specs if self.is_defined(handler_spec[0])
        ]

    def is_defined(self, handler_id):
        return handler_id in self.endpoints

    def to_full_spec(self, handler_id, handler, inject=None):
        full_endpoint = self.prefix + self.endpoints[handler_id]
        if inject is None:
            return (full_endpoint, handler)
        else:
            return (full_endpoint, handler, inject)


