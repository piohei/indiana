# -*- coding: utf-8 -*-

from tornado import web

class FingerprintHandler(web.RequestHandler):
    def get(self):
        self.render("fingerprint.html")
