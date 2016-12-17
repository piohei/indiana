# -*- coding: utf-8 -*-

import json

from tornado import web


class ReportMapHandler(web.RequestHandler):
    def initialize(self, access_point_dao, benchmark_report_dao, map_data):
        self.access_point_dao = access_point_dao
        self.benchmark_report_dao = benchmark_report_dao
        self.map_data = map_data

    def generate_color(self, i, n):
        rng = (0.3 * float(0xffffff), 0.7 * float(0xffffff))
        res = float(i) * (rng[1] - rng[0]) / float(n)
        return ("0x%0.6X" % int(res)).replace("0x", "#")

    def get(self, num):
        floor = list(map(
            lambda l: { 'x': l.x, 'y': l.y },
            self.map_data.floor
        ))

        walls = list(map(
            lambda l: [{ 'x': l[0].x, 'y': l[0].y }, { 'x': l[1].x, 'y': l[1].y }],
            self.map_data.walls
        ))

        routers = list(map(
            lambda r: { 'x': r.location.x, 'y': r.location.y },
            self.access_point_dao.active()
        ))

        report = self.benchmark_report_dao.all()[int(num)]

        points = len(report["partial_reports"])
        samples = []
        calculated = []
        for i in range(points):
            real_location = report["partial_reports"][i]["real_location"]
            engine_positions = report["partial_reports"][i]["engine_positions"]
            color = self.generate_color(i, points)

            samples.append({ 'x': real_location["x"], 'y': real_location["y"], 'color': color })
            for position in engine_positions:
                calculated.append({ 'x': position["x"], 'y': position["y"], 'color': color })

        result = {
            'levels': {
                '1': {
                    'floor': floor,
                    'walls': walls,
                    'routers': routers,
                    'samples': samples,
                    'calculated': calculated
                }
            }
        }

        self.write(json.dumps(result))
