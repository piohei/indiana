from tornado.web import RequestHandler

from web.modules.handlers_module import HandlersModule


class View(HandlersModule):
    def module(self):
        return "view"

    def rendering_handler(self, view):
        class Handler(RequestHandler):
            def get(self, *args):
                self.render(view + ".html")
        return Handler

    def get_handlers(self, config):
        return [
            (self.prefix + self.endpoints["visualisation3d"], self.rendering_handler("visualization_3d")),
            (self.prefix + self.endpoints["visualisation2d"], self.rendering_handler("visualization_2d")),
            (self.prefix + self.endpoints["fingerprint"], self.rendering_handler("fingerprint")),
            (self.prefix + self.endpoints["path"], self.rendering_handler("path")),
            (self.prefix + self.endpoints["report2d"] + "/([^/]+)", self.rendering_handler("report_2d")),
            (self.prefix + self.endpoints["root"], self.rendering_handler("index"))
        ]