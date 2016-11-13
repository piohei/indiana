import random

from db.db import db

stamps = db["sample_stamps"].find(sort=[('start_time', 1)])

times = [(o['start_time'], o['start_time'] + 30 * 1000) for o in stamps]

ap_datas = [d
            for t in times
            for d in
            db['ap_datas'].find({'created_at': {'$gte': t[0], '$lte': t[1]}}, sort=[('created_at', 1)])]

ap_datas.sort(key=lambda x: x['created_at'])

timestamp = 0
for apd in ap_datas:
    apd.pop('_id')
    apd["created_at"] = timestamp
    timestamp += random.randint(860, 1000)
    db['path3'].insert_one(apd)
