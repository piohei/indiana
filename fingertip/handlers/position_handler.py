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
        start = Time(end.millis - 15 * 1000)

        # Start and end time for sample with location (5, 2, -2)
        # start = Time(1472826203859)
        # end   = Time(1472826392960)

        measures = self.ap_data_dao.stats_group_by_mac_and_signal_for_range(start, end)

        # measures = location_5_2_minus_2 = {
        #     Mac("F8:E7:1E:29:05:00"): {
        #         Signal(band="2.4", channel=2): {
        #             "1": { "avg": RSSI(-64) },
        #         }
        #     },
        #     Mac("94:F6:65:04:E6:10"): {
        #         Signal(band="2.4", channel=2): {
        #             "1": { "avg": RSSI(-110) },
        #         }
        #     },
        #     Mac("2C:5D:93:0C:8A:60"): {
        #         Signal(band="2.4", channel=2): {
        #             "1": { "avg": RSSI(-95) },
        #         }
        #     },
        #     Mac("94:F6:65:05:C0:D0"): {
        #         Signal(band="2.4", channel=2): {
        #             "1": { "avg": RSSI(-75) },
        #         }
        #     },
        #     Mac("94:F6:65:04:FF:D0"): {
        #         Signal(band="2.4", channel=2): {
        #             "1": { "avg": RSSI(-66) },
        #         }
        #     },
        #     Mac("94:F6:65:04:F9:40"): {
        #         Signal(band="2.4", channel=2): {
        #             "1": { "avg": RSSI(-71) },
        #         }
        #     },
        #     Mac("94:F6:65:08:7B:60"): {
        #         Signal(band="2.4", channel=2): {}
        #     },
        #     Mac("F8:E7:1E:29:0E:E0"): {
        #         Signal(band="2.4", channel=2): {
        #             "1": { "avg": RSSI(-82) },
        #         }
        #     },
        #     Mac("F8:E7:1E:29:08:F0"): {
        #         Signal(band="2.4", channel=2): {
        #             "1": { "avg": RSSI(-110) },
        #         }
        #     }
        # }

        en = Engine(chain='beta', params={
            'ap_data_dao': self.ap_data_dao,
            'sample_stamp_dao': self.sample_stamp_dao,
            'measures': measures
        })

        res = en.calculate()

        publisher = Publisher("positions.{}".format(mac.replace(':', '_')))
        publisher.publish(res.to_db_object())
        publisher.destroy()

        return {"x": res.x, "y": res.y, "z": 0}
