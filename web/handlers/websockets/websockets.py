from web.handlers.handlers_module import HandlersModule
from web.handlers.websockets.handlers import *
from web.handlers.websockets.handlers.status_handler import StatusHandler


class Websockets(HandlersModule):
    def __init__(self, config, services):
        super().__init__(config)
        self.log_socket_service = services["log_socket_service"]

    def module(self):
        return "websockets"

    def handlers_specs(self):
        return [
            ("position", PositionHandler),
            ("status", StatusHandler, {
                "web_socket_service": self.log_socket_service
            })
        ]