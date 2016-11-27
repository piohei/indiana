import random

from config import config
from db.base.collection import Collection

stamps_collection_name = config["db"]["collections"]["sample_stamp"]
apdatas_collection_name = config["db"]["collections"]["ap_data"]
path_collection = Collection("path3")

ap_datas = Collection(apdatas_collection_name)

stamps = Collection(stamps_collection_name).find(sort=[('start_time', 1)])

times = [(o['start_time'], o['start_time'] + 30 * 1000) for o in stamps]

ap_datas = [d
            for t in times
            for d in
            ap_datas.find({'created_at': {'$gte': t[0], '$lte': t[1]}}, sort=[('created_at', 1)])]

ap_datas.sort(key=lambda x: x['created_at'])

timestamp = 0
for apd in ap_datas:
    apd.pop('_id')
    apd["created_at"] = timestamp
    timestamp += random.randint(860, 1000)
    path_collection.insert(apd)
