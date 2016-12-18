# -*- coding: utf-8 -*-

from tornado import web

class Report2DHandler(web.RequestHandler):
    def get(self, id):
        self.render("report_2d.html")
