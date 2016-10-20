# -*- coding: utf-8 -*-

from tornado_json import schema
from tornado_json.requesthandlers import APIHandler
from collections import defaultdict

from models import Time
from positioning.engine import Engine


class PositionHandler(APIHandler):
    def initialize(self, ap_data_dao, sample_stamp_dao, rssi_measure_dao):
        super().initialize()
        self.ap_data_dao = ap_data_dao
        self.sample_stamp_dao = sample_stamp_dao
        self.rssi_measure_dao = rssi_measure_dao

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
        start = Time(end.millis - 15 * 1000)

        data = self.ap_data_dao.grouped_rssi_stats(start, end)
        measures = {}
        for band in data.keys():
            measures[band] = defaultdict(lambda: { "rssi1": None })
            for mac in data[band].keys():
                measures[band][mac]["rssi1"] = data[band][mac]["rssi1"]["avg"]

        en = Engine(chain='beta', params={
            'ap_data_dao': self.ap_data_dao,
            'sample_stamp_dao': self.sample_stamp_dao,
            'rssi_measure_dao': self.rssi_measure_dao,
            'measures': measures
        })

        res = en.calculate()

        publisher = Publisher("positions.{}".format(mac))
        publisher.publish(loc.to_db_object())
        publisher.destroy()

        return {"x": res.x, "y": res.y, "z": 0}
