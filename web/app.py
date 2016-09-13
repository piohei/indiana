# -*- coding: utf-8 -*-

from tornado import web, ioloop
import os

import handlers

class App:
    def __init__(self):
        self.app = web.Application([
                        (r"/", handlers.RootHandler),
                        (r"/visualization/3d", handlers.Visualization3DHandler),
                        (r"/visualization/2d", handlers.Visualization2DHandler),
                        (r"/fingertip", handlers.FingerTipHandler),
                        (r"/map", handlers.MapHandler),
                        (r"/websocket", handlers.SocketHandler)
                    ],
                    static_path=os.path.join(os.path.dirname(__file__), "static"),
                    template_path=os.path.join(os.path.dirname(__file__), "views"),
                    )

    def get_app(self):
        return self.app

    def run(self):
        self.app.listen(8888, address="0.0.0.0")

        ioloop.IOLoop.instance().start()
