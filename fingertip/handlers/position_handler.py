# -*- coding: utf-8 -*-

from tornado_json import schema
from tornado_json.requesthandlers import APIHandler
from collections import defaultdict

from models import Time, Mac, Signal, RSSI
from positioning.engine import Engine

from herald import Publisher


class PositionHandler(APIHandler):
    def initialize(self, ap_data_dao, sample_stamp_dao):
        super().initialize()
        self.ap_data_dao = ap_data_dao
        self.sample_stamp_dao = sample_stamp_dao

    @schema.validate(output_schema={
        "type": "object",
        "properties": {
            "x": {
                "type": "number",
                "minimum": 0
            },
            "y": {
                "type": "number",
                "minimum": 0
            },
            "z": {"type": "number"}
        },
        "required": ["x", "y", "z"]
    })
    def get(self, mac):
        mac = mac.replace('-', ':').lower()
        end   = Time()
        start = Time(end.millis - 30 * 1000)

        # measures = self.ap_data_dao.stats_group_by_mac_and_signal_for_range(start, end)

        apdatas = self.ap_data_dao.get_for_time_range(start, end, asc=False)
        grouped = {}
        for ap_data in apdatas:
            if ap_data.router_mac.mac not in grouped:
                grouped[ap_data.router_mac.mac] = ap_data.rssis

        en = Engine(chain='permutations', params={
            'ap_data_dao': self.ap_data_dao,
            'sample_stamp_dao': self.sample_stamp_dao,
            'measures': grouped
        })

        res = en.calculate()

        publisher = Publisher("positions.{}".format(mac.replace(':', '_')))
        publisher.publish(res.to_db_object())
        publisher.destroy()

        return {"x": res.x, "y": res.y, "z": 0}
