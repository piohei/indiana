# -*- coding: utf-8 -*-

from tornado import web

class FingerTipHandler(web.RequestHandler):
    def get(self):
        self.render("fingertip.html")
