#!/bin/bash
./node_modules/babel-cli/bin/babel.js js -d babel_generated
./node_modules/browserify/bin/cmd.js babel_generated/main.js -t babelify --outfile web/static/js/main.js
