from db import SampleStampDAO
from models import SampleStamp, Mac, Time, Location

from pymongo import MongoClient

from config.config import config
from exception.exception import DBException


client = MongoClient(config['db']['host'], config['db']['port'])
print('Connection to MongoDB {} created'.format(client.address))

db = client['indiana_db']

result = db['sample_stamps'].find({})
sample_stamp_dao = SampleStampDAO()

for sample_stamp_old in result:
    mac = Mac(sample_stamp_old['mac'])
    location = Location(
        x=float(sample_stamp_old['location']['x']),
        y=float(sample_stamp_old['location']['y']),
        z=float(sample_stamp_old['location']['z'])
    )
    start_time = Time(int(sample_stamp_old['start_time']))
    end_time = Time(int(sample_stamp_old['end_time']))

    sample_stamp = SampleStamp(
        mac=mac,
        location=location,
        start_time=start_time,
        end_time=end_time
    )
    sample_stamp_dao.save(sample_stamp)

