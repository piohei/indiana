# -*- coding: utf-8 -*-

from tornado import web

class Visualization2DHandler(web.RequestHandler):
    def get(self):
        self.render("visualization_2d.html")
