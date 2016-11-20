# -*- coding: utf-8 -*-

from tornado import web
import json

from models import Map

class MapHandler(web.RequestHandler):
    def initialize(self, access_point_dao, sample_stamp_dao):
        self.access_point_dao = access_point_dao
        self.sample_stamp_dao = sample_stamp_dao

    def get(self):
        map_data = Map('floor_1')

        floor = list(map(
            lambda l: { 'x': l.x, 'y': l.y },
            map_data.floor
        ))

        walls = list(map(
            lambda l: [{ 'x': l[0].x, 'y': l[0].y }, { 'x': l[1].x, 'y': l[1].y }],
            map_data.walls
        ))

        routers = list(map(
            lambda r: { 'x': r.location.x, 'y': r.location.y },
            self.access_point_dao.active()
        ))

        samples = list(map(
            lambda s: { 'x': s.location.x, 'y': s.location.y },
            self.sample_stamp_dao.all()
        ))

        result = {
            'levels': {
                '1': {
                    'floor': floor,
                    'walls': walls,
                    'routers': routers,
                    'samples': samples,
                }
            }
        }

        self.write(json.dumps(result))
