from db.db import db
from db.base_dao import BaseDAO

from collections import defaultdict
from models import APData, Mac, Time, RSSI, Signal


class APDataDAO(BaseDAO):
    @staticmethod
    def collection_name():
        return 'ap_datas'

    def from_db_object(self, db_object):
        return APData(
            router_mac=Mac(db_object['router_mac']),
            device_mac=Mac(db_object['device_mac']),
            created_at=Time(int(db_object['created_at'])),
            rssis={ k: RSSI(float(v)) for k, v in db_object['rssis'].items() },
            signal=Signal(
                channel=int(db_object['signal']['channel']),
                band=db_object['signal']['band']
            ),
            _id=db_object['_id']
        )

    def to_db_object(self, ap_data):
        return {
            'router_mac': ap_data.router_mac.mac,
            'device_mac': ap_data.device_mac.mac,
            'created_at': ap_data.created_at.millis,
            'rssis': { k: v.dBm for k, v in ap_data.rssis.items() },
            'signal': {
                'channel': ap_data.signal.channel,
                'band': ap_data.signal.band
            },
            '_id': ap_data._id
        }

    def group_by_mac_and_signal_for_range(self, start_time, end_time):
        selected = self.find({
            'created_at': {
                '$gte': start_time.millis,
                '$lte': end_time.millis
            }
        })

        res = {}
        for ap_data in selected:
            if ap_data.router_mac not in res.keys():
                res[ap_data.router_mac] = {}
            if ap_data.signal not in res[ap_data.router_mac].keys():
                res[ap_data.router_mac][ap_data.signal] = []

            res[ap_data.router_mac][ap_data.signal].append(ap_data)

        return res

    def stats_group_by_mac_and_signal_for_range(self, start_time, end_time):
        selected = self.find({
            'created_at': {
                '$gte': start_time.millis,
                '$lte': end_time.millis
            }
        })

        grouped = {}
        for ap_data in selected:
            if ap_data.router_mac not in grouped.keys():
                grouped[ap_data.router_mac] = {}
            if ap_data.signal not in grouped[ap_data.router_mac].keys():
                grouped[ap_data.router_mac][ap_data.signal] = {}

            for k, v in ap_data.rssis.items():
                if k not in grouped[ap_data.router_mac][ap_data.signal].keys():
                    grouped[ap_data.router_mac][ap_data.signal][k] = []
                grouped[ap_data.router_mac][ap_data.signal][k].append(v)

        res = {}
        for router_mac, v1 in grouped.items():
            res[router_mac] = {}
            for signal, v2 in v1.items():
                res[router_mac][signal] = {}
                for k, v3 in v2.items():
                    values = list(map(lambda x: x.dBm, v3))
                    res[router_mac][signal][k] = {
                        'min': RSSI(min(values)),
                        'max': RSSI(max(values)),
                        'avg': RSSI(sum(values) / float(len(values)))
                    }

        return res

    def get_for_time_range(self, start_time, end_time, asc=True):
        return self.find(
                query={'created_at': {'$gte': start_time.millis, '$lte': end_time.millis}},
                sort=[('created_at', 1 if asc else -1)]
        )
