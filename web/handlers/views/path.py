# -*- coding: utf-8 -*-

from tornado import web

class PathHandler(web.RequestHandler):
    def get(self):
        self.render("path.html")
