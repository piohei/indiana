# -*- coding: utf-8 -*-

from positioning.app import App


def run(config, engine_id):
    app = App(config, engine_id)
    app.start_engine()
    app.run()
