# -*- coding: utf-8 -*-

from tornado import web

class RootHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")
