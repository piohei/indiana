#!/usr/bin/env python
import pika
import sys
import json
import time

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Location

loc1 = Location(3, 1, 0)
loc2 = Location(6, 1, 0)
loc3 = Location(3, 3, 0)

locations = []

for i in range(5):
    x = loc1.x + float(i) / 5 * (loc2.x - loc1.x)
    y = loc1.y + float(i) / 5 * (loc2.y - loc1.y)
    locations.append(Location(x, y, 0))
for i in range(5):
    x = loc2.x + float(i) / 5 * (loc3.x - loc2.x)
    y = loc2.y + float(i) / 5 * (loc3.y - loc2.y)
    locations.append(Location(x, y, 0))
for i in range(5):
    x = loc3.x + float(i) / 5 * (loc1.x - loc3.x)
    y = loc3.y + float(i) / 5 * (loc1.y - loc3.y)
    locations.append(Location(x, y, 0))

mac = '11:12:13:14:15:16'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='positions',
                         exchange_type='topic')

routing_key = "positions.{}".format(mac.replace(':', '_'))

while True:
    for loc in locations:
        message = loc.to_db_object
        channel.basic_publish(exchange='positions',
                              routing_key=routing_key,
                              body=json.dumps(loc.to_db_object()))
        print("waiting... ({0})".format(loc.to_db_object()))
        time.sleep(1)

connection.close()
