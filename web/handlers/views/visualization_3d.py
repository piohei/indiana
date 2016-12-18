# -*- coding: utf-8 -*-

from tornado import web

class Visualization3DHandler(web.RequestHandler):
    def get(self):
        self.render("visualization_3d.html")
