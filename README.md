# Indiana

Web application:
* Tornado
* visualization (2D or 3D)

Engine:
* python

AP SENT DATA:
(device mac, router mac, timestamp, rssi, channel)

# Installation
You need to install python3 and bower (npm install -g bower) first. Then run:

1. `pip3 install -r requirements.txt`
2. `cd web && bower install`

or just run `make init`

Then copy configuration file. Use: `cp config/development.yml.example config/developmnet.yml`

# Run

`make run`

# Test

`make test`

# Place to change mac for visualization
https://github.com/maveron58/indiana/blob/positioning_framework/web/static/js/visualization.js#L449
