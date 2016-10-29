from db import APDataDAO
from models import APData, Mac, Time, Signal, RSSI

from pymongo import MongoClient

from config import config
from exception import DBException


client = MongoClient(config['db']['host'], config['db']['port'])
print('Connection to MongoDB {} created'.format(client.address))

db = client['indiana_db']

result = db['ap_data'].find({})
ap_data_dao = APDataDAO()

for ap_data_old in result:
    line = ap_data_old['apMac']
    router_mac = Mac(':'.join([line[i:i+2].lower() for i in range(0, len(line), 2)]))

    line = ap_data_old['data'][0]['clientMac']
    device_mac = Mac(':'.join([line[i:i+2].lower() for i in range(0, len(line), 2)]))

    created_at = Time(int(ap_data_old['time']))

    rssi1 = RSSI(float(ap_data_old['data'][0]['rss1'])) if 'rss1' in ap_data_old['data'][0].keys() else None
    rssi2 = RSSI(float(ap_data_old['data'][0]['rss2'])) if 'rss2' in ap_data_old['data'][0].keys() else None
    rssi3 = RSSI(float(ap_data_old['data'][0]['rss3'])) if 'rss3' in ap_data_old['data'][0].keys() else None

    rssis = {}
    if rssi1 is not None:
        rssis['1'] = rssi1
    if rssi2 is not None:
        rssis['2'] = rssi2
    if rssi3 is not None:
        rssis['3'] = rssi3

    signal = Signal(band='2.4', channel=int(ap_data_old['band']))

    ap_data = APData(
        router_mac=router_mac,
        device_mac=device_mac,
        created_at=created_at,
        rssis=rssis,
        signal=signal
    )
    ap_data_dao.save(ap_data)

