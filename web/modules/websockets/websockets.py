from web.modules.handlers_module import HandlersModule
from web.modules.websockets.handlers import *


class Websockets(HandlersModule):
    def module(self):
        return "websockets"

    def get_handlers(self, config):
        return [
            (self.prefix + self.endpoints["position"], PositionHandler)
        ]