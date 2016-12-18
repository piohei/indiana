# -*- coding: utf-8 -*-

from ap_data_listener.app import App
from config import config


def run(listener_index):
    app = App(config["ap_data"][listener_index])
    app.run()
