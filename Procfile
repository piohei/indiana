# Required services
rabbit: rabbitmq-server
mongo: mongod --config /etc/mongod.conf

# Applications
web:       sleep 5 && python3 -B -m web.runner
fingertip: sleep 5 && python3 -B -m fingertip.runner
