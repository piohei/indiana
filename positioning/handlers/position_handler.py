# -*- coding: utf-8 -*-
import time
from tornado_json import schema
from tornado_json.requesthandlers import APIHandler

from models import Time
from positioning.engine import Engine

from herald import Publisher


class PositionHandler(APIHandler):
    def initialize(self, ap_data_dao, engine):
        super().initialize()
        self.ap_data_dao = ap_data_dao
        self.engine = engine

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with, content-type')
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS, DELETE')

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
        end = Time()
        start = Time(end.millis - 30 * 1000)

        # measures = self.ap_data_dao.stats_group_by_mac_and_signal_for_range(start, end)

        apdatas = self.ap_data_dao.get_for_time_range(start, end, asc=False)
        grouped = {}
        for ap_data in apdatas:
            if ap_data.router_mac.mac not in grouped:
                grouped[ap_data.router_mac.mac] = ap_data.rssis

        start = time.perf_counter()
        res = self.engine.localise(grouped)
        end = time.perf_counter()
        print("engine localised {} in {}s", mac, end-start)

        publisher = Publisher("positions.{}".format(mac.replace(':', '_')))
        publisher.publish(res.to_db_object())
        publisher.destroy()

        return {"x": res.x, "y": res.y, "z": 0}

    def options(self):
        self.set_status(204)
        self.finish()
