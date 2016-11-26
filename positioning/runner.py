# -*- coding: utf-8 -*-

from config import config
from positioning.app import App

app = App(config["engine"])

# if __name__ == "__main__":
#     app.start_engine()
#     app.run()
app.start_engine()
app.run()
