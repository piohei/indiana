# Indiana

Web application:
* Tornado (python)
* THREE.js (javascript)

Engine:
* Tornado (python)

AP SENT DATA:
(device mac, router mac, timestamp, rssi, channel)

# Installation
You need to install python3 and bower (npm install -g bower) first. Then run:

1. `pip3 install -r requirements.txt`
1. `npm install`
1. `npm run build`
1. `cd web && bower install`

or just run `make init`

Then copy configuration file. Use: `cp config/development.yml.example config/developmnet.yml`

# Development

For javascript visualization module development babel and browserify are used.

You can use `npm run watch` to automatically build visualization js module.

# Run

`make run`

# Test

`make test`
