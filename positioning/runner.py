# -*- coding: utf-8 -*-

from config import config
from positioning.app import App


def run(engine_id):
    app = App(config["engine"], engine_id)
    app.start_engine()
    app.run()
