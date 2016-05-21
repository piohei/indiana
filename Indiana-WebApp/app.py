import time

from tornado import web, websocket, ioloop, gen


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("static/index.html")


ide = 1


class SocketHandler(websocket.WebSocketHandler):
    @gen.engine
    def open(self):
        i = 0
        global ide
        this_id = ide
        ide += 1
        while not self._on_close_called:
            self.write_message("{}:{}".format(i, this_id))
            i += 1
            yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 1)


if __name__ == "__main__":
    app = web.Application([
        (r"/", IndexHandler),
        (r"/static/(.*)", web.StaticFileHandler, {"path": "./static"}),
        (r"/websocket", SocketHandler)
    ])
    app.listen(8888)
    ioloop.IOLoop.instance().start()
