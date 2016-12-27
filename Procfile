# Required services
#rabbit: rabbitmq-server
#mongo: mongod --config /etc/mongod.conf

# Applications
ap_data_listener: sleep 5 && python3 -B -m ap_data_listener.runner 2>&1
web:       sleep 5 && python3 -B -m web.runner 2>&1
fingerprint: sleep 5 && python3 -B -m fingerprint.runner 2>&1
positioning: sleep 5 && python3 -B -m positioning.runner 2>&1
