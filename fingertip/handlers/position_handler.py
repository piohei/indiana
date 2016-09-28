# -*- coding: utf-8 -*-

from tornado_json import schema
from tornado_json.requesthandlers import APIHandler


class PositionHandler(APIHandler):
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
        return {"x": 1, "y": 2, "z": 0}
