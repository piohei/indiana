# -*- coding: utf-8 -*-

from ap_data_listener.app import App
from config import config

app = App(config["ap_data"])

# if __name__ == "__main__":
#     app.run()
app.run()
