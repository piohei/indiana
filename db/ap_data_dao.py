from db.base_dao import BaseDAO

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

    def get_for_time_range(self, start_time, end_time, asc=True):
        return self.find(
                query={'created_at': {'$gte': start_time.millis, '$lte': end_time.millis}},
                sort=[('created_at', 1 if asc else -1)]
        )
