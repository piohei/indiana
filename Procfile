# Required services
rabbit: rabbitmq-server
mongo: mongod --config /etc/mongod.conf

# Applications
web:       sleep 5 && python3 -B -m web.runner 2>&1
fingertip: sleep 5 && python3 -B -m fingertip.runner 2>&1
