# -*- coding: utf-8 -*-

from wrapt import synchronized
from tornado import web

class ActualLocationHandler(web.RequestHandler):
    def post(self):
        try:
            fingertip_service.set_fingertip(**(self.body))
        except FingertipException as e:
            self.set_status(400, reason=e.message)

    def delete(self):
        try:
            fingertip_service.end_fingertip()
        except FingertipException as e:
            self.set_status(400, reason=e.message)
        except DbException as e:
            self.set_status(500, reason=e.message)

    def options(self):
        self.set_status(204)
        self.finish()
