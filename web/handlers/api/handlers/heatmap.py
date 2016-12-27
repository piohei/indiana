# -*- coding: utf-8 -*-

import json

from matplotlib.pyplot import get_cmap
from tornado import web
from shapely.geometry import Polygon
import numpy as np
from config import config


def clamp(x):
    return int(max(0, min(x, 255)))


def to_hex(r, g, b, *args):
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r*255), clamp(g*255), clamp(b*255))


def xy(x, y):
    return {"x": x, "y": y}


class HeatmapHandler(web.RequestHandler):
    def initialize(self, access_point_dao, position_dao, map_data):
        self.map_data = map_data
        self.access_point_dao = access_point_dao
        self.position_dao = position_dao
        self.step = config["heatmap"]["granularity"]
        xmax = 33
        ymax = 12
        self.mesh = [(x, y) for x in np.arange(0, xmax, self.step) for y in np.arange(0, ymax, self.step)]
        cmap = get_cmap(config["heatmap"]["cmap"])
        cmap._init()
        self.cmap = [to_hex(*color) for color in cmap._lut]

    def get(self):
        floor = list(map(
                lambda l: (l.x, l.y),
                self.map_data.floor
        ))

        walls = list(map(
                lambda l: [{'x': l[0].x, 'y': l[0].y}, {'x': l[1].x, 'y': l[1].y}],
                self.map_data.walls
        ))

        routers = list(map(
                lambda r: {'x': r.location.x, 'y': r.location.y},
                self.access_point_dao.active()
        ))

        heatmap = self.create_heatmap()

        result = {
            'levels': {
                '1': {
                    'floor': self.to_compound_floor(heatmap, floor),
                    'walls': walls,
                    'routers': routers,
                    'cmap': self.cmap
                }
            }
        }

        self.write(json.dumps(result))

    def create_heatmap(self):
        mesh_with_counts = [(top_left, self.position_dao.count_in_rectangle(top_left, self.step)) for top_left in
                            self.mesh]
        counts = [t[1] for t in mesh_with_counts if t[1] > 0]
        max_count = max(counts)
        min_count = min(counts)
        bin_size = (max_count - 0) / len(self.cmap)
        return [self.to_heatmap_el(top_left_with_count, bin_size, min_count) for top_left_with_count in mesh_with_counts]

    def to_heatmap_el(self, top_left_with_count, bin_size, min_count):
        (x, y), count = top_left_with_count
        polygon = Polygon([(x, y), (x + self.step, y), (x+self.step, y+self.step), (x, y+self.step)])
        bin_no = int(min(255, (count - min_count) / bin_size))
        color = self.cmap[bin_no] if count > 0 else "#ffffff"
        return (polygon, color)

    def to_compound_floor(self, heatmap, floor):
        floor_pl = Polygon(floor)
        intersections = [(floor_pl.intersection(heatmap_el[0]), heatmap_el[1]) for heatmap_el in heatmap]
        positive_intersections = [(list(intersection.exterior.coords)[:-1], color)
                                  for intersection, color in intersections
                                  if type(intersection) == Polygon]

        return [{"polygon": list(map(lambda point: xy(*point), polygon)), "color": color}
                for polygon, color in positive_intersections]


