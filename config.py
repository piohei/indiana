# -*- coding: utf-8 -*-

import os
import yaml

env = None
try:
  env = os.environ['INDIANA_ENV']
except KeyError as e:
  env = 'development'

if env not in ['development', 'test']:
  raise Exception("Unknown environment: {}".format(env))

config_path = os.path.abspath(
                os.path.join(
                  os.path.dirname(__file__), 'config', "{}.yml".format(env)
                )
              )

config = None
with open(config_path, 'r') as ymlfile:
    config = yaml.load(ymlfile)
